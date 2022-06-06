from django.core.management.base import BaseCommand, CommandError
from utils.SaveStream import SaveStream
from stage_1.models import Tweets
from stage_2.models import Authors
from utils.TweetCleaner import TweetCleaner
from utils.Auth import Auth


class Command(BaseCommand):
    help = 'Start User Extraction'

    # def add_arguments(self, parser):
    #     parser.add_argument('--num_tweets', nargs='?', type=int, default=2)

    def handle(self, *args, **options):
        print("Start User Extraction")

        while True:
            authors_l3 = Authors.objects.filter(l3=True, l2_done=True)

            if not authors_l3:
                pass

            else:
                for author in authors_l3:
                    # fetch tweets of each author
                    tweets = Tweets.objects.filter(author_id=author.author_id)
                    for tweet in tweets:
                        tweet_text = tweet.tweet_text
                        clean_tweet = tweet.tweet_clean

                        # run ensemble anal
                        ens = 0
                        tweet.ens1_score = ens
                        tweet.save()

                        if ens == 0:
                            author.ens1_count += 1

                    author.l3_done = True
                    author.save()

            # TODO: Add Sleep
