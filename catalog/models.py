from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, declarative_base

from flask_sqlalchemy import SQLAlchemy
from flask import flask

app = Flask(__name__)

db = SQLAlchemy(app)

# Instead of Base, use db.Model

# TODO Plan my app first, i have to make a CRUD APP

# flask-sqlalchemy would set auto_increment to true (WOW!)
class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, index=True)
    description = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('catalog.id'), nullable=False)


class Catalog(db.Model):
    __tablename__ = 'catalog'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # One to many relationship with items
    items = db.relationship('item', backref='person', lazy=dynamic)


class User(db.Model):
    __tablename__ = 'user'
    pass