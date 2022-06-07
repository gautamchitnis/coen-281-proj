import time

import tweetnlp
from django.core.management.base import BaseCommand, CommandError
from utils.SaveStream import SaveStream
from stage_1.models import Tweets
from stage_2.models import Authors
from utils.TweetCleaner import TweetCleaner
from utils.Auth import Auth


class Command(BaseCommand):
    help = 'Start L3 Exploration'

    # def add_arguments(self, parser):
    #     parser.add_argument('--num_tweets', nargs='?', type=int, default=2)

    def handle(self, *args, **options):
        print("Start L3 Exploration")
        e_model = tweetnlp.load('emotion')

        while True:
            authors_l3 = Authors.objects.filter(l3=True, l1_done=True, l2_done=True, l3_done=False)

            if not authors_l3:
                print("Stage 4 sleeping for 240 sec")
                time.sleep(240)

            else:
                for author in authors_l3:
                    # fetch tweets of each author
                    tweets = Tweets.objects.filter(author_id=author.author_id)
                    for tweet in tweets:
                        tweet_text = tweet.tweet_text
                        clean_tweet = tweet.tweet_clean

                        # run ensemble
                        emotion = e_model.emotion(tweet_text)

                        if emotion == 'anger':
                            tweet.emotion = 0
                            author.anger_count += 1
                        elif emotion == 'joy':
                            tweet.emotion = 1
                            author.joy_count += 1
                        elif emotion == 'optimism':
                            tweet.emotion = 2
                            author.optimism_count += 1
                        elif emotion == 'sadness':
                            tweet.emotion = 3
                            author.sadness_count += 1

                        tweet.save()

                    author.l3_done = True
                    author.save()

            # TODO: Add Sleep
