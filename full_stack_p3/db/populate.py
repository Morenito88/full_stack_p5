from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setup import Base, User, Category, Item

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy users
User1 = User(name="Hugo Santos", email="hugofcs@gmail.com",
             picture='https://scontent-mrs1-1.xx.fbcdn.net/hphotos-ash2/v/t1.0-9/1236029_592323727472948_1910831729_n.jpg?oh=bdedc7bb8db69cc85e6a39c1103f4606&oe=566D32AA', role='admin')
session.add(User1)
session.commit()

# Create dummy categories and items

# Items for Action
category1 = Category(name="Action")
session.add(category1)
session.commit()

item1 = Item(title="Counter-Strike: Global Ofensive", 
              description="Counter-Strike: Global Offensive (CS: GO) will expand upon the team-based action gameplay that it pioneered when it was launched 14 years ago. CS: GO features new maps, characters, and weapons and delivers updated versions of the classic CS content (de_dust, etc.).",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg?t=1440086526",
              price='$10.99', 
              category=category1, 
              user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="Satellite Reign", 
              description="Satellite Reign is a real-time, class-based strategy game, set in an open-world cyberpunk city. You command a group of 4 agents through rain-soaked, neon-lit streets, where the law is the will of mega-corporations.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/268870/header.jpg?t=1440745532",
              price='$22.39', 
              category=category1, 
              user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="ARK: Survival Evolved", 
              description="As a man or woman stranded naked, freezing & starving on a mysterious island, you must hunt, harvest, craft items, grow crops, & build shelters to survive. Use skill and cunning to kill or tame & ride the Dinosaurs & primeval creatures roaming the land, & team up with hundreds of players or play locally!",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/346110/header.jpg?t=1440705133",
              price='$27.99', 
              category=category1, 
              user_id=1)

session.add(item3)
session.commit()

# Items for Adventure
category2 = Category(name="Adventure")
session.add(category2)
session.commit()

item1 = Item(title="Pillars of Eternity", 
              description="Prepare to be enchanted by a world where the choices you make and the paths you choose shape your destiny. Obsidian Entertainment, the developer of Fallout: New Vegas and South Park: The Stick of Truth, together with Paradox Interactive is proud to present Pillars of Eternity.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/291650/header.jpg?t=1434054333",
              price='$41.99', 
              category=category2, 
              user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="Mount & Blade: Warband", 
              description="In a land torn asunder by incessant warfare, it is time to assemble your own band of hardened warriors and enter the fray. Lead your men into battle, expand your realm, and claim the ultimate prize: the throne of Calradia!",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/48700/header.jpg?t=1440696051",
              price='$6.79', 
              category=category2, 
              user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="Starbound", 
              description="In Starbound, you take on the role of a character who's just fled from their home planet, only to crash-land on another. From there you'll embark on a quest to survive, discover, explore and fight your way across an infinite universe!",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/211820/header.jpg?t=1440698464",
              price='$11.89', 
              category=category2, 
              user_id=1)

session.add(item3)
session.commit()

# Items for Casual
category3 = Category(name="Casual")
session.add(category3)
session.commit()

item1 = Item(title="Universe Sandbox 2", 
              description="Create & destroy on an unimaginable scale... with a space simulator that merges real-time gravity, climate, collision, and material interactions to reveal the beauty of our universe and the fragility of our planet.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/230290/header.jpg?t=1440658364",
              price='$22.99', 
              category=category3, 
              user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="Besiege", 
              description="Besiege is a physics based building game in which you construct medieval siege engines and lay waste to immense fortresses and peaceful hamlets. Build a machine which can crush windmills, wipe out battalions of brave soldiers and transport valuable resources, defending your creation against cannons.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/346010/header.jpg?t=1440519440",
              price='$6.99', 
              category=category3, 
              user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="Cities: Skylines", 
              description="Cities: Skylines is a modern take on the classic city simulation. The game introduces new game play elements to realize the thrill and hardships of creating and maintaining a real city whilst expanding on some well-established tropes of the city building experience.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/255710/header.jpg?t=1430910532",
              price='$27.99', 
              category=category3, 
              user_id=1)

session.add(item3)
session.commit()

# Items for Multiplayer
category4 = Category(name="Multiplayer")
session.add(category4)
session.commit()

item1 = Item(title="Elite: Dangerous", 
              description="Take control of your own starship in a cutthroat galaxy. Elite: Dangerous brings gaming's original open world adventure into the modern generation with a connected galaxy, evolving narrative and the entirety of the Milky Way re-created at its full galactic proportions.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/359320/header.jpg?t=1433541850",
              price='$37.49', 
              category=category4, 
              user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="The Elder Scrolls Online: Tamriel Unlimited", 
              description="The Elder Scrolls Online: Tamriel Unlimited, the latest chapter of the award-winning series, brings the legendary experience online for the first time. Explore the vast world with friends or embark upon the adventure alone - the choices you will make will shape your destiny. No game subscription required.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/306130/header.jpg?t=1436223118",
              price='$54.99', 
              category=category4, 
              user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="Dead Realm", 
              description="Ghosts prey on the living inside the haunted mansion of a long dead electricity tycoon. Dead Realm is a creepy, multiplayer action game with beautiful, immersive environments. You can play as either a Ghost or a Human character and work with your friends to run, hide, survive... or die.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/352460/header.jpg?t=1438634901",
              price='$14.99', 
              category=category4, 
              user_id=1)

session.add(item3)
session.commit()

# Items for Racing
category5 = Category(name="Racing")
session.add(category5)
session.commit()

item1 = Item(title="Car Mechanic Simulator 2015", 
              description="New cars, new tools, new options, more parts and much more fun in the next version of Car Mechanic Simulator! Take your wrench! Create and expand your auto repairs service empire. Car Mechanic Simulator 2015 will take you behind the scenes of daily routine in car workshop.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/320300/header.jpg?t=1435965916",
              price='$9.99', 
              category=category5, 
              user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="DiRT 3 Complete Edition", 
              description="Get DiRT 3 Complete Edition, the definitive edition of off-road racer DiRT 3 now expanded with extra content and enhanced with Steamworks integration, including Achievements, Leaderboards and Steam Cloud Saves.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/321040/header.jpg?t=1440411989",
              price='$29.99', 
              category=category5, 
              user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="Absolute Drift", 
              description="Absolute Drift is a racing game about becoming a master at the art of drifting.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/320140/header.jpg?t=1438371642",
              price='$11.99', 
              category=category5, 
              user_id=1)

session.add(item3)
session.commit()

# Items for RPG
category6 = Category(name="RPG")
session.add(category6)
session.commit()

item1 = Item(title="Terraria", 
              description="Dig, fight, explore, build! Nothing is impossible in this action-packed adventure game. Four Pack also available!",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/105600/header.jpg?t=1439404386",
              price='$9.99', 
              category=category6, 
              user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="Hand of Fate", 
              description="Deckbuilding comes to life in Hand of Fate! An infinitely replayable series of quests - earn new cards, build your deck, then try to defeat it! In a cabin at the end of the world, the game of life and death is played. Draw your cards, play your hand, and discover your fate.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/266510/header.jpg?t=1437720344",
              price='$11.49', 
              category=category6, 
              user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="7 Days to Die", 
              description="Building on survivalist and horror themes, players in 7 Days to Die can scavenge the abandoned cities of the buildable and destructible voxel world for supplies or explore the wilderness to gather raw materials to build their own tools, weapons, traps, fortifications and shelters.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/251570/header.jpg?t=1436062246",
              price='$22.99', 
              category=category6, 
              user_id=1)

session.add(item3)
session.commit()

# Items for Sports
category7 = Category(name="Sports")
session.add(category7)
session.commit()

item1 = Item(title="Football Manager 2015", 
              description="Football Manager 2015, the latest in the award-winning and record-breaking series, is coming to PC, Macintosh and Linux computers in November 2014. Football Manager is the most realistic, in-depth and immersive simulation of football management available.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/295270/header.jpg?t=1433503204",
              price='$49.99', 
              category=category7, 
              user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="Robot Roller-Derby Disco Dodgeball", 
              description="100% bouncy projectile warfare on roller skates. Neon laser lights, alley-oops, jetpacks, and EMP blasts - just like the dodgeball you remember. Jam-packed with singleplayer and multiplayer ridiculousness.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/270450/header.jpg?t=1438646721",
              price='$14.99', 
              category=category7, 
              user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="Poker Night 2", 
              description="The chips are down and the ante is up in this sentence already bursting with poker cliches! Take the fifth seat in Poker Night 2, at a table featuring Claptrap (Borderlands 2), Brock Samson (The Venture Bros.), Ash (Army of Darkness) and Sam (Sam and Max series).",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/234710/header.jpg?t=1373561383",
              price='$4.99', 
              category=category7, 
              user_id=1)

session.add(item3)
session.commit()

# Items for Strategy
category8 = Category(name="Strategy")
session.add(category8)
session.commit()

item1 = Item(title="Big Pharma", 
              description="What if you had it in your power to rid the world of disease, to improve the lives of millions, to ease suffering and cure the sick... and earn a tidy profit? As the head of your own Pharmaceutical Conglomerate you have this power resting in your hands. Will you use it for good?",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/344850/header.jpg?t=1440754865",
              price='$18.39', 
              category=category8, 
              user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="Company of Heroes 2", 
              description="Experience the ultimate WWII RTS platform with the original COH2 and its standalone expansions: The Western Front Armies (multiplayer), Ardennes Assault (single-player) and The British Forces (multi-player). Multiplayer standalones allow you to play on any map against anyone owning any COH2 product.",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/231430/header.jpg?t=1440695776",
              price='$8.74', 
              category=category8, 
              user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="Planetary Annihilation: TITANS", 
              description="Wage war across entire solar systems with massive armies at your command. Annihilate enemy forces with world-shattering TITAN-class units, and demolish planets with massive super weapons!",
              picture="http://cdn.akamai.steamstatic.com/steam/apps/386070/header.jpg?t=1440546578",
              price='$36.99', 
              category=category8, 
              user_id=1)

session.add(item3)
session.commit()


print "added all items!"
