import os

from flask import Flask, render_template
from .models import db

# base_dir = os.path.abspath()
app = Flask(__name__)

# app configuration
app.config.from_pyfile('config.py')

# db initialization
db.init_app(app)


@app.route('/')
def index():
    return 'Hello'

@app.route('/categories')
def show_categories():
    pass

@app.route('/categories/<int:category_id>')
def show_category(category_id):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
