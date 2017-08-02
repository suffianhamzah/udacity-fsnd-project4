from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# dbpattern initialization from https://stackoverflow.com/questions/
# 9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User data model"""
    __tablename_ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    picture = db.Column(db.String())

    def __repr__(self):
        return '<User {0}>'.format(self.name)


class Category(db.Model):
    """Category data model"""
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Category {0}>'.format(self.name)


class Item(db.Model):
    """Item data model"""
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False,
                     index=True)  # index makes queries more efficient
    description = db.Column(db.String)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship('Category', backref='items')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    def __repr__(self):
        return ('<Item {0}, category {1}, created by user {2}>'
                .format(self.name, self.category, self.user))
