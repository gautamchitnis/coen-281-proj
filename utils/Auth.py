import tweepy


class Auth:

    class Keys:
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""

    def get_auth(self):
        keys = self.get_auth_keys()

        auth = tweepy.OAuth1UserHandler(
            keys.consumer_key, keys.consumer_secret, keys.access_token, keys.access_token_secret
        )

        api = tweepy.API(auth)
        return api

    def get_auth_keys(self):
        keys = self.Keys()

        keys.consumer_key = ""
        keys.consumer_secret = ""
        keys.access_token = ""
        keys.access_token_secret = ""

        return keys
