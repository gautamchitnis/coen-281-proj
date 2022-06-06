import tweepy
from decouple import config


class Auth:

    class Keys:
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""
        bearer_token = ""

    def __init__(self):
        self.keys = self.Keys()

    def get_auth(self):
        keys = self.keys

        auth = tweepy.OAuth1UserHandler(
            keys.consumer_key, keys.consumer_secret, keys.access_token, keys.access_token_secret
        )

        api = tweepy.API(auth)
        return api

    def get_client(self):
        keys = self.keys

        client = tweepy.Client(
            bearer_token=keys.bearer_token,
            consumer_key=keys.consumer_key,
            consumer_secret=keys.consumer_secret,
            access_token=keys.access_token,
            access_token_secret=keys.access_token_secret
        )

        return client

    def set_auth_keys(self, keys=None):
        if keys is None:
            self.keys.consumer_key = config('TWITTER_CONSUMER_KEY')
            self.keys.consumer_secret = config('TWITTER_CONSUMER_SECRET')
            self.keys.access_token = config('TWITTER_ACCESS_TOKEN')
            self.keys.access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET')
            self.keys.bearer_token = config('TWITTER_BEARER_TOKEN')
        else:
            self.keys.consumer_key = keys.consumer_key
            self.keys.consumer_secret = keys.consumer_secret
            self.keys.access_token = keys.access_token
            self.keys.access_token_secret = keys.access_token_secret
            self.keys.bearer_token = keys.bearer_token

    def get_auth_keys(self):
        return self.keys
