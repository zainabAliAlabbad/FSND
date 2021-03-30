#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import psycopg2
from flask import Flask
from sqlalchemy import (Column, String, Integer, Table, ForeignKey)
from flask_sqlalchemy import SQLAlchemy
import json


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

database_path = 'postgresql://postgres:A1b2c3d4@localhost:5432/capstone-project'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def init_db():
    db.drop_all()
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'genres': self.genres,
            'year': self.year,
        }

#----------------------------------------------------------------------------#

casting = db.Table('casting',db.Column('actor_id',db.Integer,db.ForeignKey('actor.id')),
                   db.Column('movie_id',db.Integer,db.ForeignKey('movie.id'))
                  )

class actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    Role = db.relationship('movie', secondary=casting,backref='movies_list', lazy=True)

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
