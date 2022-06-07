import json
import tweepy


class TSCManager:
    class TweetPrinter(tweepy.StreamingClient):
        processed_counter = 0
        tweets = dict()
        max_count = 1

        def __init__(self, bearer_token, count, **kwargs):
            super().__init__(bearer_token, **kwargs)
            self.max_count = count

        def on_data(self, raw_data):
            if self.processed_counter != self.max_count:
                data = json.loads(raw_data)
                data = data["data"]
                if data["lang"] == "en":
                    self.processed_counter += 1
                    self.tweets[data["id"]] = {
                        "author_id": data["author_id"],
                        "text": data["text"]
                    }
                    # print(f"Processed {self.processed_counter} Tweets")
                return True
            else:
                self.disconnect()
                return False

    def get_tweet_printer_instance(self, token, count):
        return self.TweetPrinter(token, count=count)
