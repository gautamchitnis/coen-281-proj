from utils.Auth import Auth
from utils.TSCManager import TSCManager


class SaveStream:

    def get_recent_stream(self, count):
        auth = Auth()
        auth.set_auth_keys()
        keys = auth.get_auth_keys()
        tsc_man = TSCManager()
        t_printer = tsc_man.get_tweet_printer_instance(keys.bearer_token, count=count)
        print("Start Twitter Stream Processing")

        t_printer.sample(expansions="author_id", tweet_fields="lang")

        print("End Twitter Stream Processing")
        return t_printer.tweets
