import os

from flask import Flask, render_template, url_for
from .models import db, Item, Category

# base_dir = os.path.abspath()
app = Flask(__name__)

# app configuration
app.config.from_pyfile('config.py')

# db initialization
db.init_app(app)


@app.route('/')
def index():
    items = Item.query.all()
    print([item.name for item in items])
    return render_template('index.html', items=items)

@app.route('/categories')
def show_categories():
    pass


@app.route('/categories/<int:category_id>')
def show_category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    return category.items


@app.route('/items/add', methods=['GET','POST'])
def add_item():
    pass

if __name__ == '__main__':
    app.run()
