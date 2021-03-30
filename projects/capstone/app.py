#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import *

db = SQLAlchemy()

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def index():
    return "Hello World"

@app.route('/actors')
@requires_auth('get:actors')
def get_actors(payload):

    try:
        actors = actor.query.all()
        formatted_actors = [data.format() for data in actors]
        return jsonify({
            'success': True,
            'actors': formatted_actors
        }), 200
    except BaseException:
        abort(404)

@app.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(payload, actor_id):
    actor = actor.query.filter(actor.id == actor_id).one_or_none()

    if actor is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'actors': actor.format()
        }), 200

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_actors(payload):

    body = request.get_json()
    name = body.get('name')
    age = int(body.get('age'))
    gender = body.get('gender')
    try:
        actor = actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'success': True,
            'message': 'added Successfully',
            'actors': actor.format()
        }), 200
    except BaseException:
        abort(422)

@ app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def edit_actors(payload, actor_id):
    actor = actor.query.filter(actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    else:
        body = request.get_json()
        name = body.get('name')
        age = int(body.get('age'))
        gender = body.get('gender')

        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender

            actor.update()

            return jsonify({
                'success': True,
                'message': 'Updated Successfully',
                'actor': actor.format()
            }), 200

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, actor_id):

    actor = actor.query.filter(actor.id == actor_id).one_or_none()

    if actor is None:
        abort(404)
    else:
        actor.delete()
        return jsonify({
            'success': True,
            'message': 'Deleted Successfully',
            'actor': actor.name
        }), 200

@app.route('/movies')
@requires_auth('get:movies')
def get_movies(payload):
    try:
        movies  = movie.query.all()
        formatted_movies  = [data.format() for data in movies]
        return jsonify({
            'success': True,
            'movies': formatted_movies
        }), 200
    except BaseException as e:
        print(e)
        abort(404)

@app.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(payload, movie_id):
    movie = movie.query.filter(movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'movies': movie.format()
        }), 200

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movies(payload):

    body = request.get_json()
    title = body.get('title')
    genres = body.get('genres')
    year = body.get('year')
    try:
        movie = movie(title=title, genres=genres, year=year)
        movie.insert()
        return jsonify({
            'success': True,
            'message': 'added Successfully',
            'movie': movie.format()
        }), 200
    except BaseException:
        abort(422)

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def edit_movies(payload, movie_id):

    movie = movie.query.filter(movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)
    else:
        body = request.get_json()
        title = body.get('title')
        genres = body.get('genres')
        year = body.get('year')

    if title:
        movie.title = title
    if genres:
        movie.genres = genres
    if year:
        movie.year = year
    movie.update()
    return jsonify({
        'success': True,
        'message': 'Updated Successfully',
        'movie': movie.format()
    }), 200

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, movie_id):

    movie = movie.query.filter(movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)
    else:
        movie.delete()
        return jsonify({
            'success': True,
            'message': 'Deleted Successfully',
            'movie': movie.title
        }), 200



#----------------------------------------------------------------------------#
# Error handler
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

#----------------------------------------------------------------------------#
# Error handler for AuthError
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
