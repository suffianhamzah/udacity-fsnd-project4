# Flask config
import os
from binascii import hexlify

class Config(object):
    DEBUG = False
    SECRET_KEY = hexlify(os.urandom(24))
    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_CREDENTIALS = {
        'google': {
            'id': '192814586375-tpg625ou2gelldahk4efhrp87bnqa8gs.apps.googleusercontent.com',
            'secret': 'DH2f9iOqfFu_pd07p2Hx0TPt',
            'authorization_base_url':'https://accounts.google.com/o/oauth2/v2/auth',
            'token_url': 'https://www.googleapis.com/oauth2/v4/token'
        }
    }

class DevConfig(Config):
    DEBUG = True


config = {
    'default': DevConfig,
    'production' : ''
}