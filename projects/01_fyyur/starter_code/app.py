#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  ------------------------------------------------------------------------------------------------------------------------------------------------------   #
#  Venues
#  ------------------------------------------------------------------------------------------------------------------------------------------------------  #

@app.route('/venues')
def venues():
    locals = []
    venues = Venue.query.all()
    places = Venue.query.distinct(Venue.city, Venue.state).all()
    for place in places:
        locals.append({
        'city': place.city,
        'state': place.state,
        'venues': [{
            'id': venue.id,
            'name': venue.name,
            } for venue in venues if
            venue.city == place.city and venue.state == place.state]
        })
    return render_template('pages/venues.html', areas=locals);

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    form = VenueForm()
    try:
     newVenue = Venue()
     form.populate_obj(newVenue)
     db.session.add(newVenue)
     db.session.commit()
     flash('Venue ' + form.name.data + ' was successfully listed!')
    except ValueError as e:
     db.session.rollback()
     print(e)
     flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    finally:
     db.session.close()

    return render_template('pages/home.html')

#  Searche Venue
#  ----------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  search_results = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  response = {}
  response['count'] = len(search_results)
  response['data'] = search_results
  return render_template('pages/search_venues.html',results=response,search_term=request.form.get('search_term', ''))

#  Show Venue info
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)
    upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()
    past_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
    upcoming_shows = []
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
        "artist_id": show.artist_id,"artist_name": show.Artist.name,"artist_image_link": show.Artist.image_link
        ,"start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    for show in upcoming_shows_query:
        upcoming_shows.append({"artist_id": show.artist_id,"artist_name": show.Artist.name,"artist_image_link": show.Artist.image_link
        ,"start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    data = {"id": venue.id,"name": venue.name,"address": venue.address,"city": venue.city,"state": venue.state,
    "phone": venue.phone,"facebook_link": venue.facebook_link,"image_link": venue.image_link,"past_shows": past_shows,
    "upcoming_shows": upcoming_shows,"past_shows_count": len(past_shows),"upcoming_shows_count": len(upcoming_shows)}

    return render_template('pages/show_venue.html', venue=data)

#  ------------------------------------------------------------------------------------------------------------------------------------------------------   #
#  Artists
#  ------------------------------------------------------------------------------------------------------------------------------------------------------   #
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all())

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new artist record in the db, instead
    form = ArtistForm()
    try:
     newArtist = Artist()
     form.populate_obj(newArtist)
     db.session.add(newArtist)
     db.session.commit()
     flash('Artist ' + form.name.data + ' was successfully listed!')
    except ValueError as e:
     db.session.rollback()
     print(e)
     flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    finally:
     db.session.close()

    return render_template('pages/home.html')

#  Searche Artist
#  ----------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term')
    search_results = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
    response = {}
    response['count'] = len(search_results)
    response['data'] = search_results
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

#  Show Artist info
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    artist = Artist.query.get(artist_id)
    upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()
    past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
    upcoming_shows = []
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
        "artist_id": show.venue_id,"artist_name": show.Venue.name,"artist_image_link": show.Venue.image_link
        ,"start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    for show in upcoming_shows_query:
        upcoming_shows.append({"artist_id": show.venue_id,"artist_name": show.Venue.name,"artist_image_link": show.Venue.image_link
        ,"start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    data = {"id": artist.id,"name": artist.name,"city": artist.city,"state": artist.state,"genres": artist.genres,
    "phone": artist.phone,"facebook_link": artist.facebook_link,"image_link": artist.image_link,"past_shows": past_shows,
    "upcoming_shows": upcoming_shows,"past_shows_count": len(past_shows),"upcoming_shows_count": len(upcoming_shows)}

    return render_template('pages/show_artist.html', artist=data)


#  -----------------------------------------------------------------------------------------------------------------------------------------------------   #
#  Shows
#  -----------------------------------------------------------------------------------------------------------------------------------------------------   #
@app.route('/shows')
def shows():
    # displays list of shows at /shows
    return render_template('pages/shows.html', shows=Show.query.all())

#  Create Show
#  ----------------------------------------------------------------
@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm()
    try:
        newShow = Show()
        form.populate_obj(newShow)
        db.session.add(newShow)
        db.session.commit()
        flash('Show was successfully listed!')
    except ValueError as e:
        db.session.rollback()
        print(e)
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
