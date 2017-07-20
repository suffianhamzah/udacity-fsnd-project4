import os

from flask import Flask, render_template, url_for, request, flash, redirect
from .forms import itemForm
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
    return render_template('categories.html', categories=categories)


@app.route('/categories/<int:category_id>')
def show_category(category_id):
    category = Category.query.get(category_id)
    return render_template('category.html', category=category)


@app.route('/item/<int:item_id>')
def show_item(item_id):
    item = Item.query.filter_by(id=item_id).first_or_404()
    return render_template('item.html', item=item)


@app.route('/item/new', methods=['GET', 'POST'])
def new_item():
    form = itemForm()
    category_choices = [(category.id, category.name)
                        for category in Category.query.all()]
    form.category.choices = category_choices
    print(category_choices)
    if form.validate_on_submit():
        category = Category.query.get(form.category.data)
        item = Item(form.name.data, form.description.data, category)
        db.session.add(item)
        db.session.commit()
        flash('{0} has been created!'.format(item.name))
        return redirect(url_for('show_item', item_id=item.id))
    else:
        return render_template('newitem.html', form=form)


@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """Edits an existing item's fields

    With reference from: https://goonan.io/flask-wtf-tricks/

    """
    item = Item.query.get_or_404(item_id)
    form = itemForm(obj=item)  # Prepulate form
    category_choices = [(category.id, category.name)
                        for category in Category.query.all()]
    form.category.choices = category_choices

    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        category = Category.query.get(form.category.data)
        item.category = category
        db.session.add(item)
        db.session.commit()
        flash('{} has been edited'.format(item.name))
        return redirect(url_for('show_item', item_id=item.id))

    form.name.data = item.name
    form.description.data = item.description
    form.category.data = item.category.id

    return render_template('edititem.html', form=form, item=item)


@app.route('/item/delete/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('{} has been deleted :('.format(item.name))
        return redirect(url_for('index'))
    return render_template('deleteitem.html', item = item)


if __name__ == '__main__':
    app.run()
