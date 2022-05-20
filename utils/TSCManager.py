import json
import tweepy


class TSCManager:
    class TweetPrinter(tweepy.StreamingClient):
        counter = 0
        tweets = dict()

        def on_data(self, raw_data):
            if self.counter != 50 :
                data = json.loads(raw_data)
                data = data["data"]
                if data["lang"] == "en":
                    self.counter += 1
                    self.tweets[data["id"]] = {
                        "author_id": data["author_id"],
                        "text": data["text"]
                    }
                return True
            else:
                self.disconnect()
                return False

    def get_tweet_printer_instance(self, token):
        return self.TweetPrinter(token)
