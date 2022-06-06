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

        NEG_THRESH = 5

        auth = Auth()
        auth.set_auth_keys()
        client = auth.get_client()

        tweet_cleaner = TweetCleaner()

        while True:
            authors_l2 = Authors.objects.filter(l2=True, l1_done=True)

            if not authors_l2:
                pass

            else:
                for author in authors_l2:
                    # fetch tweets of each author
                    tweets_response = client.get_users_tweets(id=author.author_id, max_results=100)
                    # tweets_response[0] tweets list
                    # tweets_response[3] tweets prev next info
                    tweets = tweets_response[0]

                    for tweet in tweets:
                        clean_tweet = tweet_cleaner.clean(tweet['data']['text'])

                        # run sent anal
                        sentiment = 0

                        # add tweets to db
                        tweet = Tweets(
                            tweet_id=int(tweet['data']['id']),
                            author_id=author.author_id,
                            tweet_text=tweet['data']['text'],
                            tweet_clean=",".join(clean_tweet),
                            sentiment_score=sentiment,
                            sentiment_done=True
                        )
                        tweet.save()

                        if sentiment == 0:
                            author.neg_count += 1

                    author.l2_done = True
                    # TODO: Calc % of neg tweets out of total tweets fetched for author and modify condition as such
                    if author.neg_count >= NEG_THRESH:
                        author.l3 = True
                    author.save()

            # TODO: Add Sleep
