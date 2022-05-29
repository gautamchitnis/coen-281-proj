from django.core.management.base import BaseCommand, CommandError
from utils.SaveStream import SaveStream
from stage_1.models import Tweets


class Command(BaseCommand):
    help = 'Start Data Stream'

    def add_arguments(self, parser):
        parser.add_argument('--num_tweets', nargs='?', type=int, default=2)

    def handle(self, *args, **options):
        print("Start Data Generation")

        save_stream = SaveStream()

        num_tweets = options['num_tweets']

        while True:
            data = save_stream.get_recent_stream(
                count=num_tweets
            )

            for tweet_id in data:
                tweet = Tweets(
                    tweet_id=int(tweet_id),
                    author_id=int(data[tweet_id]["author_id"]),
                    tweet_text=data[tweet_id]['text']
                )
                tweet.save()
