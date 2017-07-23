"""
Implementation of Oauth Class ()
Heavily inspired by https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
Using Requests oauth
"""

from flask import current_app
from requests_oauthlib import OAuth2Session


class OauthSignIn(object):
    """A base Oauth sign in class
    A base class for an oauth2session for different oauth providers
    This is based on https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
    Instead of using Rauth, this is implemented using requests-oauthlib

    Attributes:

    """
    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.client_id = credentials['id']
        self.client_secret = credentials['secret']

    def authorize(self):
        """This function will call"""
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)


class GoogleSignIn(OauthSignIn):
    def __init__(self, provider_name):
        """Init and overriding the provider_name using super"""
        super().__init__('google')
        self.auth_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        self.token_url = 'https://www.googleapis.com/oauth2/v4/token'
        self.base_url = 'https://www.googleapis.com/auth/'
        self.auth_session = OAuth2Session(
            self.client_id,
            scope=[
                self.base_url + 'userinfo.email',
                self.base_url + 'userinfo.profile'],
            redirect_uri=self.get_callback_url())

    def authorize(self):
        return (self.auth_session
                    .authorization_url(self.auth_base_url,
                                       access_type='offline',
                                       approval_prompt='force'))
