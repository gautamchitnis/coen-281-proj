import json
from utils.Auth import Auth
from utils.TSCManager import TSCManager


class SaveStream:

    def get_recent_stream(self):
        auth = Auth()
        keys = auth.get_auth_keys()
        tsc_man = TSCManager()
        printer = tsc_man.get_tweet_printer_instance(keys.access_token)

        printer.sample(expansions="author_id", tweet_fields="lang")
        try:
            with open('data.json', 'a') as f:
                f.write(json.dumps(printer.tweets, indent=4))
                return True
        except BaseException as e:
            print("Error : %s" % str(e))

        print("exit")
