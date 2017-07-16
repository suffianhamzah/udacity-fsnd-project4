from flask_sqlalchemy import SQLAlchemy

# Instead of Base, use db.Model

# TODO Plan my app first, i have to make a CRUD APP

# flask-sqlalchemy would set auto_increment to true (WOW!)

# dbpattern initialization from https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {0}>'.format(self.name)


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, index=True) # index makes queries more efficient
    description = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    category = db.relationship('Category', backref='items')

    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category

    def __repr__(self):
        return '<Item {0}, category {1}>'.format(self.name, self.category)
