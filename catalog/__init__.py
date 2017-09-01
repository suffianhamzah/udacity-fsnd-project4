import os

from flask import (Flask, render_template, url_for, abort, flash, redirect,
                   session, request)
from flask.json import jsonify
from flask_login import (LoginManager, login_user, logout_user,
                         current_user, login_required)


# Relative imports
from .forms import itemForm
from .models import db, Item, Category, User
from .config import config
from .auth import OauthSignIn

app = Flask(__name__)

# app configuration
app.config.from_object(config[os.environ.get('SERVER_SETTING')])


# db initialization
db.init_app(app)

# Login Manager from Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """Sets current_user object"""
    return User.query.get(int(user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handling"""
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden_access(e):
    """Custom 403 error handling"""
    return render_template('403.html'), 403


@app.errorhandler(401)
def authentication_failed(e):
    """Custom 401 error handling"""
    return render_template('401.html'), 401


@app.route('/')
def index():
    """Main view for the app"""
    items = Item.query.all()
    categories = Category.query.all()
    print([item.name for item in items])
    return render_template('index.html', items=items, categories=categories)


@app.route('/categories/<int:category_id>/items')
def show_category(category_id):
    """View for showing all items of one category"""
    category = Category.query.get(category_id)
    categories = Category.query.all()
    return render_template('category.html',
                           selected_category=category,
                           categories=categories)


@app.route('/item/<int:item_id>')
def show_item(item_id):
    """View for showing an item's details"""
    item = Item.query.filter_by(id=item_id).first_or_404()
    return render_template('item.html', item=item)


@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    """View for creating a new item"""
    form = itemForm()
    category_choices = [(category.id, category.name)
                        for category in Category.query.all()]
    form.category.choices = category_choices
    print(category_choices)
    if form.validate_on_submit():
        item = Item(name=form.name.data,
                    description=form.description.data,
                    category_id=form.category.data,
                    user_id=current_user.get_id())
        db.session.add(item)
        db.session.commit()
        flash('{0} has been created!'.format(item.name))
        return redirect(url_for('show_item', item_id=item.id))
    else:
        return render_template('newitem.html', form=form)


@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """Edits an existing item's information"""
    item = Item.query.get_or_404(item_id)

    form = itemForm(obj=item)  # Prepulate form
    category_choices = [(category.id, category.name)
                        for category in Category.query.all()]
    form.category.choices = category_choices

    id_check = current_user.id is not item.user.id

    if id_check:
        abort(403)

    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.category_id = form.category.data
        db.session.add(item)
        db.session.commit()
        flash('{} has been edited'.format(item.name))
        return redirect(url_for('show_item', item_id=item.id))

    form.name.data = item.name
    form.description.data = item.description
    form.category.data = item.category.id

    return render_template('edititem.html', form=form, item=item)


@app.route('/item/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    """View for deleting an item"""
    item = Item.query.get_or_404(item_id)

    id_check = current_user.id is not item.user.id

    if id_check:
        abort(403)

    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('{} has been deleted :('.format(item.name))
        return redirect(url_for('index'))
    return render_template('deleteitem.html', item=item)


@app.route('/login')
def login():
    """
    Shows the login page to an unathenticated user,
    redirects otherwise.

    We store the redirect url(next) in a session so that
    we can retrieve the url once a user successfully logs in
    through their respective oauth provider
    """
    if current_user.is_authenticated:
        flash('You are logged in already.')
        return redirect(url_for('index'))

    session['next'] = request.args.get('next')
    print(session['next'])
    return render_template('login.html')


@app.route('/authorize/<provider>')
def authorize(provider):
    """Instantiates"""
    print(provider)
    oauth = OauthSignIn.get_provider(provider)
    return redirect(oauth.authorize())


@app.route('/callback/<provider>')
def callback(provider):
    """The route that an oauth provider would call once the user
    has or has not granted authentication to our website

    """
    print(request.args)
    if 'error' in request.args:
        flash(request.args.get('error'))
        abort(401)

    no_code = 'code' not in request.args
    not_state = request.args.get('state') != session.get('oauth_state')

    if no_code and not_state:
        flash('Invalid state and no auth code!')
        abort(401)
    oauth = OauthSignIn.get_provider(provider)

    try:
        data = oauth.callback()
    except Exception as e:
        abort(401)

    user = User.query.filter_by(unique_id=data['id']).first()
    if not user:
        user = User(unique_id=data['id'],
                    name=data['name'],
                    email=data['email'],
                    picture=data['picture'])
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    flash('You Are logged in')
    if session.get('next'):
        return redirect(session['next'])
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Logging out from the website"""
    token = session.get('auth_token')
    if token is None:
        flash('You are not connected')
        return redirect(url_for('index'))
    del session['auth_token']
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))


@app.route('/catalog/JSON')
@login_required
def get_json():
    """Provides a JSON object of all items in the catalog"""
    categories = Category.query.all()
    return jsonify(categories=[category.serialize for category in categories])


if __name__ == '__main__':
    app.run()
