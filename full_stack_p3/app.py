# Framework modules
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask import session as login_session
from flask import make_response
from flask.ext.seasurf import SeaSurf
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string
import requests
import copy

# Custom modules
from db.setup import Base, User, Category, Item

# Instantiate a new Flask application
app = Flask(__name__)

# Instantiate cross-site request forgery protection
csrf = SeaSurf(app)

# Connect to Database and create database session
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Routes
# -- Frontpage


@app.route('/')
def index():
    items = getRecestItems(6)
    return render_template('frontpage.html', items=items)

# -- Login System


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Disconnect based on provider


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('index'))
    else:
        flash("You were not logged in")
        return redirect(url_for('index'))


@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():

    CLIENT_ID = json.loads(
        open('/var/www/html/full_stack_p3/secrets/google.json', 'r').read())['web']['client_id']

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/var/www/html/full_stack_p3/secrets/google.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@csrf.exempt
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('/var/www/html/full_stack_p3/secrets/facebook.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('/var/www/html/full_stack_p3/secrets/facebook.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in our
    # token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# -- Categories
# Show all categories


@app.route('/categories/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Item).order_by(desc(Item.id)).all()
    return render_template('categories.html', categories=categories, category_id=-1, items=items)

# -- Items
# Show all items from a category


@app.route('/categories/<int:category_id>/items/')
def showItems(category_id):
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('categories.html', categories=categories, category_id=category_id, items=items)

# Create a new item


@app.route('/categories/items/new/', methods=['GET', 'POST'])
def newItem():
    # Check if the user made login
    # If not redirect him to the login page
    if 'username' not in login_session:
        return redirect('/login')

    categories = session.query(Category).order_by(asc(Category.name)).all()
    if request.method == 'POST':
        newItem = Item(title=request.form['item_title'],
                       description=request.form['item_description'],
                       price=request.form['item_price'],
                       picture=request.form['item_picture'],
                       category_id=request.form['item_category'],
                       user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Item \'%s\' Successfully Created' % (newItem.title))
        return redirect(url_for('showCategories'))
    else:
        return render_template('newItem.html', categories=categories)

# Edit an item


@app.route('/categories/<int:category_id>/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    categories = session.query(Category).order_by(asc(Category.name)).all()
    item = session.query(Item).filter_by(id=item_id).one()

    # Check if the user made login
    # If not redirect him to the login page
    if 'username' not in login_session:
        return redirect('/login')

    # Check if the user own the item
    # If not, dont give him permission to edit it
    if item.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['item_title']:
            item.title = request.form['item_title']
        if request.form['item_description']:
            item.description = request.form['item_description']
        if request.form['item_price']:
            item.price = request.form['item_price']
        if request.form['item_picture']:
            item.picture = request.form['item_picture']
        if request.form['item_category']:
            item.category_id = request.form['item_category']
        session.add(item)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showItems', category_id=item.category_id))
    else:
        return render_template('editItem.html', categories=categories, item=item)

# Delete an item


@app.route('/categories/<int:category_id>/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()

    # Check if the user made login
    # If not redirect him to the login page
    if 'username' not in login_session:
        return redirect('/login')

    # Check if the user own the item
    # If not, dont give him permission to delete it
    if item.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this item. Please create your own item in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showItems', category_id=item.category_id))
    else:
        return render_template('deleteItem.html', category_id=category_id, item=item)

# JSON APIs to view Categories and Games information

# Show all categories and the respective items in JSON format


@app.route('/categories/JSON/')
def allCategoriesJSON():
    categories = session.query(Category).all()
    jsonF = {}
    # Get all categories and from each one get the respective items
    # Build a json formated string with the list of categories and the items
    # inside each one
    for c in categories:
        jsonF[c.name] = c.serialize
        items = session.query(Item).filter_by(category_id=c.id).all()
        jsonF[c.name]['Items'] = [i.serialize for i in items]
    return jsonify(jsonF)

# Show all items in JSON format


@app.route('/items/JSON/')
def allItemsJSON():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])


# Show information of an item in JSON format


@app.route('/items/<int:item_id>/JSON/')
def itemJSON(item_id):
    item = session.query(Item).filter_by(
        id=item_id).one()
    return jsonify(Item=item.serialize)

# XML APIs to view Categories and Games information

# Show all categories and the respective items in XML format


@app.route('/categories/XML/')
def allCategoriesXML():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    template = render_template(
        'categories.xml', categories=categories, items=items)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

# Show all items in XML format


@app.route('/items/XML/')
def allItemsXML():
    items = session.query(Item).all()
    template = render_template('items.xml', items=items)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response


# Show information of an item in XML format


@app.route('/items/<int:item_id>/XML/')
def itemXML(item_id):
    item = session.query(Item).filter_by(
        id=item_id).one()
    template = render_template('item.xml', item=item)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

# Helpful functions

# Get an array of n items order by id descending (latests items created)


def getRecestItems(total=5):
    items = session.query(Item).order_by(desc(Item.id)).limit(total)
    return items

# Create a new user for the application


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'], role='user')
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Get all information of an user


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Get an user ID using his email to search


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Start the application server
if __name__ == '__main__':
    app.secret_key = 'cd48e1c22de0961d5d1bfb14f8a66e006cfb1cfbf3f0c0f3'
    app.debug = False
    app.run()
