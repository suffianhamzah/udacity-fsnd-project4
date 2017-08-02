import os
from binascii import hexlify


class Config(object):
    """Base config object for flask"""
    DEBUG = False
    SECRET_KEY = hexlify(os.urandom(24))
    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_CREDENTIALS = {
        'google': {
            'id': '192814586375-tpg625ou2gelldahk4efhrp87bnqa8gs.apps.googleusercontent.com',
            'secret': os.environ.get('GOOGLE_API'),
            'authorization_base_url':'https://accounts.google.com/o/oauth2/v2/auth',
            'token_url': 'https://www.googleapis.com/oauth2/v4/token'
        }
    }

class DevConfig(Config):
    """Dev Config for the app"""
    DEBUG = True
    OAUTHLIB_INSECURE_TRANSPORT = os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://pc-name:user@localhost:PORT/catalog'


config = {
    'default': DevConfig,
    'production': ProdConfig
}
