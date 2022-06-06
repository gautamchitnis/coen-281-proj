from django.core.management.base import BaseCommand, CommandError
from utils.SaveStream import SaveStream
from stage_1.models import Tweets
from stage_2.models import Authors
from utils.TweetCleaner import TweetCleaner


class Command(BaseCommand):
    help = 'Start Sentiment Analysis'

    # def add_arguments(self, parser):
    #     parser.add_argument('--num_tweets', nargs='?', type=int, default=2)

    def handle(self, *args, **options):
        print("Start Sentiment Analysis")

        while True:
            unprocessed_tweets = Tweets.objects.filter(sentiment_done=False)[0:2]
            if not unprocessed_tweets:
                pass
            else:
                for up_tweet in unprocessed_tweets:
                    tweet_author = Authors.objects.filter(author_id=up_tweet.author_id)
                    if not tweet_author:
                        tweet_author = Authors(
                            author_id=up_tweet.author_id
                        )
                        tweet_author.save()
                    # TODO: perf sent anal
                    sentiment = 0
                    up_tweet.sentiment_done = True
                    up_tweet.sentiment_score = sentiment
                    up_tweet.save()
                    if sentiment == 0:
                        tweet_author.neg_count += 1
                        tweet_author.l1 = True
                        tweet_author.save()

            # TODO: Add Sleep
