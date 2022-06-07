from django.core.management.base import BaseCommand, CommandError
from utils.SaveStream import SaveStream
from stage_1.models import Tweets
from utils.TweetCleaner import TweetCleaner
import time


class Command(BaseCommand):
    help = 'Start Data Stream'

    def add_arguments(self, parser):
        parser.add_argument('--num_tweets', nargs='?', type=int, default=2)

    def handle(self, *args, **options):
        print("Start Data Generation")

        save_stream = SaveStream()
        tweet_cleaner = TweetCleaner()

        num_tweets = options['num_tweets']

        while True:
            data = save_stream.get_recent_stream(
                count=num_tweets
            )
            count = 0

            for tweet_id in data:
                count += 1
                clean_tweet = tweet_cleaner.clean(data[tweet_id]['text'])

                tweet = Tweets(
                    tweet_id=int(tweet_id),
                    author_id=int(data[tweet_id]["author_id"]),
                    tweet_text=data[tweet_id]['text'],
                    tweet_clean=",". join(clean_tweet)
                )

                tweet.save()

            print(f"Processed {count} Tweets")
            print("Stage 1 Sleeping for 60 Seconds")

            time.sleep(60)
