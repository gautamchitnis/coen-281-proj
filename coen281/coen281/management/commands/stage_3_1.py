import time

from django.core.management.base import BaseCommand, CommandError
from utils.SaveStream import SaveStream
from stage_1.models import Tweets
from stage_2.models import Authors
from utils.TweetCleaner import TweetCleaner
from utils.Auth import Auth
import tweetnlp


class Command(BaseCommand):
    help = 'Start L1 Exploration'

    # def add_arguments(self, parser):
    #     parser.add_argument('--num_tweets', nargs='?', type=int, default=2)

    def handle(self, *args, **options):
        print("Start L1 Exploration")

        NEG_THRESH = 3

        auth = Auth()
        auth.set_auth_keys()
        client = auth.get_client()

        tweet_cleaner = TweetCleaner()

        model = tweetnlp.load('sentiment')

        while True:
            authors_l1 = Authors.objects.filter(l1=True, l1_done=False)

            if not authors_l1:
                print("Stage 3.1 sleeping for 120 sec")
                time.sleep(120)

            else:
                for author in authors_l1:
                    # fetch tweets of each author
                    tweets_response = client.get_users_tweets(id=author.author_id)

                    tweets = tweets_response[0]

                    for tweet in tweets:
                        clean_tweet = tweet_cleaner.clean(tweet['data']['text'])

                        # add tweets to db
                        tweet = Tweets(
                            tweet_id=int(tweet['data']['id']),
                            author_id=author.author_id,
                            tweet_text=tweet['data']['text'],
                            tweet_clean=",".join(clean_tweet),
                            sentiment_done=True
                        )
                        # run sent anal
                        sentiment = model.sentiment(tweet.tweet_text)

                        if sentiment == 'negative':
                            tweet.sentiment_score = 0
                            author.neg_count += 1
                        elif sentiment == 'neutral':
                            tweet.sentiment_score = 1
                            author.neutral_count += 1
                        elif sentiment == 'positive':
                            tweet.sentiment_score = 2
                            author.pos_count += 1

                        tweet.save()

                    author.l1_done = True
                    if author.neg_count >= NEG_THRESH:
                        author.l2 = True
                    author.save()
