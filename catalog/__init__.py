import os

from flask import Flask, render_template, url_for, request
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
    categories = Category.query.all()
    return render_template('category.html', categories=categories)


@app.route('/categories/<int:category_id>')
def show_category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    return category.items


@app.route('/items/new', methods=['GET','POST'])
def new_item():
    if request.method = 'POST':

    else:
        return render_tempplate('newitem.html')

if __name__ == '__main__':
    app.run()
