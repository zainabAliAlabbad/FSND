#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
# TODO: connect to a local postgresql database
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, db.Sequence('venue_id',start=4, increment=1), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    venueShow = db.relationship('Show', backref = 'Venue' , lazy = True)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, db.Sequence('artist_id',start=4, increment=1), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    artistShow = db.relationship('Show', backref = 'Artist' , lazy = True)

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, db.Sequence('show_id',start=6, increment=1), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id') ,nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id') ,nullable = False)
    start_time = db.Column(db.DateTime)

db.create_all()


#----------------------------------------------------------------------------#
# Create real data for db
#----------------------------------------------------------------------------#

#  Venue data ---------------------------------------------------------------#
try:
 venue1 = Venue(id = 1 ,name='The Musical Hop',city='San Francisco',state='CA',address='1015 Folsom Street',phone='123-123-1234'
 ,image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
 ,facebook_link='https://www.facebook.com/TheMusicalHop')

 venue2 = Venue(id = 2 ,name='The Dueling Pianos Bar',city='New York',state='NY',address='335 Delancey Street',phone='914-003-1132'
 ,image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
 ,facebook_link='https://www.facebook.com/theduelingpianos')

 venue3 = Venue(id = 3 ,name='Park Square Live Music & Coffee',city='San Francisco',state='CA',address='San Francisco',phone='415-000-1234'
 ,image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
 ,facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee')

 db.session.add_all([venue1,venue2,venue3])
 db.session.commit()
except:
 db.session.rollback()
 error=True
 print(sys.exc_info())
finally:
 db.session.close()

#  Artist data ---------------------------------------------------------------#
try:
 artist1 = Artist(id = 1 ,name=' Guns N Petals',city='San Francisco',state='CA',phone='326-123-5000',genres='Rock , Roll'
 ,image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
 ,facebook_link='https://www.facebook.com/GunsNPetals')

 artist2 = Artist(id = 2 ,name='Matt Quevedo',city='New York',state='NY',phone='300-400-5000',genres='Jazz'
 ,image_link='https:///images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
 ,facebook_link='https://www.facebook.com/mattquevedo923251523')

 artist3 = Artist(id = 3 ,name='The Wild Sax Band',city='San Francisco',state='CA',phone='567-234-1132',genres='Jazz , Classical'
 ,image_link='https:///images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
 ,facebook_link='https://www.facebook.com/WildSaxBand')

 db.session.add_all([artist1,artist2,artist3])
 db.session.commit()
except:
 db.session.rollback()
 error=True
 print(sys.exc_info())
finally:
 db.session.close()

#  Show data -----------------------------------------------------------------#
try:
 show1 = Show(id = 1 ,artist_id= 1 ,venue_id= 1 ,start_time='2019-05-21T21:30:00.000Z')
 show2 = Show(id = 2 ,artist_id= 2 ,venue_id= 3 ,start_time='2019-06-15T23:00:00.000Z')
 show3 = Show(id = 3 ,artist_id= 3 ,venue_id= 3 ,start_time='2035-04-01T20:00:00.000Z')
 show4 = Show(id = 4 ,artist_id= 3 ,venue_id= 3 ,start_time='2035-04-08T20:00:00.000Z')
 show5 = Show(id = 5 ,artist_id= 3 ,venue_id= 3 ,start_time='2035-04-15T20:00:00.000Z')

 db.session.add_all([show1,show2,show3,show4,show5])
 db.session.commit()
except:
 db.session.rollback()
 error=True
 print(sys.exc_info())
finally:
 db.session.close()
