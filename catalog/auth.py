from flask import current_app, session, url_for, request
from requests_oauthlib import OAuth2Session


class OauthSignIn(object):
    """A base Oauth sign in class
    A base class for an oauth2session for different oauth providers
    Based on
    https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
    Instead of using Rauth, this is implemented using requests-oauthlib
    https://requests-oauthlib.readthedocs.io

    Attributes:

    """
    providers = None

    def __init__(self, provider_name):
        """Initializes the class"""
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.client_id = credentials['id']
        self.client_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        """Class method to fetch a child sign-in class e.g. Google

        Instatiates all child classes, stores them into a dict(providers)
        and returns a child instance based on provider_name

        Params:
            provider_name (str): Name of Oauth provider
        """
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                print(provider_class)
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class GoogleSignIn(OauthSignIn):
    """Google oauth class inherited from oauthsignin
    Implements

    """

    def __init__(self):
        """Init and overriding the provider_name using super"""
        super().__init__('google')
        self.auth_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        self.token_url = 'https://www.googleapis.com/oauth2/v4/token'
        self.base_url = 'https://www.googleapis.com/auth/'
        self.scope = [self.base_url + 'userinfo.email',
                      self.base_url + 'userinfo.profile']
        self.auth_session = OAuth2Session(self.client_id,
                                          scope=self.scope,
                                          redirect_uri=self.get_callback_url())

    def authorize(self):
        """Returns a STATE token for preventing CSRF"""
        # auth_session =
        authorization_url, state = (self.auth_session.authorization_url(
                                    self.auth_base_url,
                                    access_type='offline',
                                    approval_prompt='force'))
        session['oauth_state'] = state
        return authorization_url

    def callback(self):
        """Retrieves access token from provider


        """
        access_token = (self.auth_session.fetch_token(
                        self.token_url,
                        client_secret=self.client_secret,
                        authorization_response=request.url))
        session['auth_token'] = access_token

        # fetches the info
        resp = self.auth_session.get('https://www.googleapis.com/oauth2/v1/userinfo')
        userinfo = resp.json()
        print(userinfo)
        return userinfo


#class FacebookSignIn(OauthSignIn):
 #   def __init__(self):
 #       super().__init__('facebook')
