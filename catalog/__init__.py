import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# base_dir = os.path.abspath()
app = Flask(__name__)

# app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'Hello'

@app.route('/categories')
def show_categories():


@app.route('/categories/<int:category_id>')
def show_category(category_id):
    pass

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9000)
