import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
	"""docstring for User"""
	__tablename__ = 'users'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	picture = Column(String(250))
	role = Column(String(5))

class Category(Base):
	"""docstring for Category"""
	__tablename__ = 'category'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)

	@property
	def serialize(self):
	    return {
	    	'id': self.id,
	    	'name': self.name
	    }
		

class Item(Base):
	"""docstring for Item"""
	__tablename__ = 'item'

	id = Column(Integer, primary_key = True)
	title = Column(String(250), nullable = False)
	description = Column(String())
	picture = Column(String(250))
	price = Column(String(10))	

	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)

	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship(User)

	@property
	def serialize(self):
	    return {
	    	'id': self.id,
	    	'title': self.title,
	    	'description': self.description,
	    	'picture': self.picture,
	    	'category_id': self.category_id
	    }
	


engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.create_all(engine)
