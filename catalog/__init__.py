from flask import (Flask, render_template, url_for, request,
                   flash, redirect, session, request, make_response)
from flask_login import LoginManager, login_user, logout_user, current_user
from flask.json import jsonify
from .forms import itemForm
from .models import db, Item, Category, User
from .config import config
from .auth import OauthSignIn
# base_dir = os.path.abspath()
app = Flask(__name__)

# app configuration
app.config.from_object(config['default'])
# app.config.from_pyfile('config.py')

# db initialization
db.init_app(app)

# Login Manager from Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_managerlogin_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

############################# AUTH #####################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    # TO DO
    """
    add login page
    login endpoint should check if there's a user token available
    Using https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask/page/0#comments
    implement User model, should be finished by friday
    Friday - finish auth, implement auth and make sure everything's working
    add some style to app
    # Extras! Write tests, if possible for some of the things
    # Extras! Implement different configs for DEV vs PROD
    """
    print(session.get('auth_token') is None)
    print(session.get('auth_token') is not None)
    print(session.get('auth_token'))
    if not current_user.is_anonymous:
        flash('You are logged in already.')
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/authorize/<provider>')
def authorize(provider):
    """Instantiates"""
    print(provider)
    oauth = OauthSignIn.get_provider(provider)
    return redirect(oauth.authorize())


@app.route('/callback/<provider>')
def callback(provider):
    print(request.args)
    if 'error' in request.args:
        return request.args.get('error')
    print('test1')

    no_code = 'code' not in request.args
    not_state = request.args.get('state') != session.get('oauth_state')
    if no_code and not_state:
        return 'Invalid State and no auth code!'
    print(provider)
    oauth = OauthSignIn.get_provider(provider)
    print(oauth)
    try:
        stuff = oauth.callback()
    except Exception as e:
        print(e)
        return make_response(jsonify(error=e), 401)
    #login_user(user, True)
    user = User.query.filter_by(unique_id=stuff['id']).first()
    if not user:
        user = User(unique_id=stuff['id'],
                    name=stuff['name'],
                    email=stuff['email'],
                    picture=stuff['picture'])
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    flash('You Are logged in')
    return redirect(url_for('index'))


@app.route('/logout/<provider>')
def logout(provider):
    token = session.get('auth_token')
    if token is None:
        response = make_response(jsonify(status='User not connected'), 401)
        return response
    del session['auth_token']
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
