#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import collections
import dateutil.parser
import sys
import os
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
collections.Callable = collections.abc.Callable
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app,db)

# TODO: connect to a local postgresql database

# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:awa@localhost/mike'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------



# class Venue(db.Model):
#     __tablename__ = 'Venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     website_link = db.Column(db.String(120))
#     seeking_talent = db.Column(db.Boolean())
#     seeking_descript = db.Column(db.String(120))
#     shows = db.relationship('Show', backref='venue', lazy=True, passive_deletes=True)

#     def __repr__(self):
#       return f'<Venue{self.id} {self.name}>'
# #\
#     # TODO: implement any missing fields, as a database migration using Flask-Migrate



#     def __repr__(self):
#       return f'<Venue{self.id} {self.name}>'

# class Artist(db.Model):
#     __tablename__ = 'Artist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     website_link = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     seeking_venue = db.Column(db.Boolean())
#     seeking_description= db.Column(db.String(120))
#     shows = db.relationship('Show', backref='artist', lazy=True, passive_deletes=True)

#     def __repr__(self):
#       return f'<Show{self.id} {self.name}>'

# class Show(db.Model):
#     __tablename__ = 'Show'

#     id = db.Column(db.Integer, primary_key=True)
#     artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
#     venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
#     def __repr__(self):
#       return f'<Show{self.id} {self.start_time}>'

# db.create_all()

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.order_by('id').all()
  
  return render_template('pages/venues.html', venues=venues);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  results = Venue.query.filter(Venue.name.ilike(search)).all()
  count = Venue.query.filter(Venue.name.ilike(search)).count()
  
  return render_template('pages/search_venues.html', results=results, search_term=search_term, count=count)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #venue = Venue.query.filter_by(id=venue_id).first()
  time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  shows = db.session.query(Show).join(Venue).filter_by(id=venue_id).first()
  upcoming_shows = db.session.query(Show).join(Venue).filter_by(id=venue_id).filter(Show.start_time > time).all()
  old_shows = db.session.query(Show).join(Venue).filter_by(id=venue_id).filter(Show.start_time < time).all()
  venue = Venue.query.filter_by(id=venue_id).first()

  gen_data = []
  
  if shows:
    past_shows = [{
    "venue_id": shows.venue.id,
    "venue_name": shows.venue.name,
    "venue_image_link": shows.venue.image_link,
    "start_time": format_datetime(str(shows.start_time))
    }]
  else:
    past_shows= []
  print(venue.genres)

  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link":venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_descript": venue.seeking_descript,
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": past_shows,
    "past_shows_count": len(old_shows),
    "upcoming_shows_count": len(upcoming_shows)}

  
  return render_template('pages/show_venue.html', venue=data)

  
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
      form = VenueForm()

      name=form.name.data
      city=form.city.data
      state=form.state.data
      address=form.address.data 
      phone=form.phone.data
      image_link=form.image_link.data
      facebook_link=form.facebook_link.data
      website_link=form.website_link.data
      seeking_descript=form.seeking_descript.data
      seeking_talent= form.seeking_talent.data
      genres= form.genres.data

      print(genres)

      venue = Venue(name=name, 
      state=state,
      city=city,
      address=address,
      phone=phone,
      image_link=image_link,
      facebook_link=facebook_link,
      website_link=website_link,
      genres= genres,
      seeking_descript=seeking_descript,
      seeking_talent=seeking_talent)

      db.session.add(venue)
      db.session.commit()

      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      

    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())

    finally:
      db.session.close()
    if not error:
      return redirect(url_for('index'))


    
 
    
      
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # # TODO: on unsuccessful db insert, flash an error instead.
  #   if error:
  #     flash('An error occured'+ 'Venue' + request.form['name'] 'could not be listed')
  # # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/', methods=['POST'])
def delete_venue(venue_id):
  error = False
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted succesfully')
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
    if not error:
      return redirect(url_for('index'))
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  artists=Artist.query.all()

  for artist in artists:
    pass

  # TODO: replace with real data returned from querying the database
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # search_term = request.form.get('search_term', '')
  # search = "%{}%".format(search_term)
  # results = Venue.query.filter(Venue.name.ilike(search)).all()
  # count = Venue.query.filter(Venue.name.ilike(search)).count()
  
  search_term = request.form.get('search_term')
  search_results = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  count = len(search_results)
  data = []
  for result in search_results:
    data.append({
      result.id,
      result.name
})
  response = [{
    "count": count,
    "data": data
  }]
  

    # response = list()
    # data = list()
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''), count=count)
 

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):


  time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  shows = db.session.query(Show).join(Venue).join(Artist).filter_by(id=artist_id).first()
  upcoming_shows = db.session.query(Show).join(Venue).join(Artist).filter_by(id=artist_id).filter(Show.start_time > time).all()
  old_shows = db.session.query(Show).join(Venue).join(Artist).filter_by(id=artist_id).filter(Show.start_time < time).all()
  artist= Artist.query.filter_by(id=artist_id).first()
  

  if shows:
    past_shows = [{
    "venue_id": shows.venue.id,
    "venue_name": shows.venue.name,
    "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "start_time": format_datetime(str(shows.start_time))
    }]
  else:
    past_shows= []
    flash('Artist does not have a show yet!')
    

  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link":artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": past_shows,
    "past_shows_count": len(old_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_artist.html', artist=data)
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  form = ArtistForm()

  artist = Artist.query.get(artist_id)

  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data= artist.phone
  form.image_link.data= artist.image_link
  form.facebook_link.data= artist.facebook_link
  # form.genres.data = artist.genres
  form.website_link.data= artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  try:
    form = ArtistForm()

    artist = Artist.query.get(artist_id)

    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    
    db.session.commit()

  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())

  finally:
    db.session.close()
    if not error:
      return redirect(url_for('show_artist', artist_id=artist_id))

  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()


  venue = Venue.query.get(venue_id)

  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data= venue.phone
  form.address.data = venue.address
  form.image_link.data= venue.image_link
  form.facebook_link.data= venue.facebook_link
  # form.genres.data = artist.genres
  form.website_link.data= venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_descript.data = venue.seeking_descript
 
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
    form = VenueForm()

    venue = Venue.query.get(artist_id)

    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.address= form.address.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_descript = form.seeking_descript.data

    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())

  finally:
    db.session.close()
    if not error:
      return redirect(url_for('show_artist', venue_id=venue_id))
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
      form = ArtistForm()

      name=form.name.data
      city=form.city.data
      state=form.state.data
      phone=form.phone.data
      image_link=form.image_link.data
      facebook_link=form.facebook_link.data
      website_link=form.website_link.data
      seeking_description=form.seeking_description.data
      seeking_venue= form.seeking_venue.data
      genres= form.genres.data

      artist = Artist(name=name, 
      state=state,
      city=city,
      phone=phone,
      image_link=image_link,
      facebook_link=facebook_link,
      website_link=website_link,
      genres=genres,
      seeking_description=seeking_description,
      seeking_venue=seeking_venue)

      db.session.add(artist)
      db.session.commit()

      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      

    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())

    finally:
      db.session.close()
    if not error:
      return redirect(url_for('index'))

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = db.session.query(Show).join(Venue).join(Artist).all()
  data = []
  for show in shows:
    data.append({
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist_id,
    "artist_name": show.artist.name,
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": format_datetime(str(show.start_time))
  })
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  form = ShowForm()

  artist_id=int(form.artist_id.data)
  venue_id=int(form.venue_id.data)
  start_time=form.start_time.data.strftime('%Y-%m-%d')
  

  artist = db.session.query(Show).join(Artist).filter_by(id=artist_id).filter(Show.start_time == start_time).all()

  try:
    if len(artist) == 0:
      show=Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
      flash('Show was succesfully listed!')
    else:
      flash('Artist has already been booked within the period of time you choose please kindly check the artist availability')
      return redirect(url_for('create_show_submission'))
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    return render_template('pages/home.html')

  # return redirect(url_for('create_show_submission'))
   
  



  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

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
