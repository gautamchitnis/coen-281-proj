import time

import tweetnlp
from django.core.management.base import BaseCommand, CommandError
from utils.SaveStream import SaveStream
from stage_1.models import Tweets
from stage_2.models import Authors
from utils.TweetCleaner import TweetCleaner
from utils.Auth import Auth


class Command(BaseCommand):
    help = 'Start L2 Exploration'

    # def add_arguments(self, parser):
    #     parser.add_argument('--num_tweets', nargs='?', type=int, default=2)

    def handle(self, *args, **options):
        print("Start L2 Exploration")

        NEG_THRESH = 30

        auth = Auth()
        auth.set_auth_keys()
        client = auth.get_client()

        tweet_cleaner = TweetCleaner()

        model = tweetnlp.load('sentiment')

        while True:
            authors_l2 = Authors.objects.filter(l2=True, l1_done=True, l2_done=False)

            if not authors_l2:
                print("Stage 3.2 sleeping for 180 sec")
                time.sleep(180)

            else:
                for author in authors_l2:
                    # fetch tweets of each author
                    tweets_response = client.get_users_tweets(id=author.author_id, max_results=100)

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

                    author.l2_done = True

                    tot_twt_count = Tweets.objects.filter(author_id=author.author_id).count()

                    if (author.neg_count/tot_twt_count)*100 >= NEG_THRESH:
                        author.l3 = True
                    author.save()
