#!/usr/bin/python3

from flask_script import Server, Manager, Shell
from catalog import app, db, Item, Category, User


def make_shell_context():
    """Creates an instance where manager knows which app to load in CLI"""
    return dict(app=app, db=db, Item=Item, Category=Category)


"""Initializes all the objects for commands"""
manager = Manager(app)
shell = Shell(make_context=make_shell_context, use_ipython=True)
server = Server(host="0.0.0.0", port=9000)


@manager.command
def createdb():
    db.create_all()
    """ Creates some objects in the db

    Soccer = Category(name='Soccer')
    Baseball = Category(name='Baseball')
    boot = Item(name='Boots', description='Boots worn during playing',
                category=Soccer)
    bat = Item(name='Bat', description='Test', category=Baseball)
    ball= Item(name='Soccer Ball', description='Testa', category=Soccer)
    db.session.add(Soccer)
    db.session.add(Baseball)
    db.session.add(boot)
    db.session.add(bat)
    db.session.add(ball)
    db.session.commit()
    """
    print('created db instance!')


@manager.command
def destroydb():
    db.drop_all()
    print('dropped db tables')


manager.add_command('shell', server)
manager.add_command('runserver', server)


if __name__ == '__main__':
    manager.run()
