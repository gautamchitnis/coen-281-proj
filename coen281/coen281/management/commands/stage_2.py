from django.core.management.base import BaseCommand, CommandError
from utils.SaveStream import SaveStream
from stage_1.models import Tweets
from stage_2.models import Authors
from utils.TweetCleaner import TweetCleaner
import tweetnlp


class Command(BaseCommand):
    help = 'Start Sentiment Analysis'

    # def add_arguments(self, parser):
    #     parser.add_argument('--num_tweets', nargs='?', type=int, default=2)

    def handle(self, *args, **options):
        print("Start Sentiment Analysis")
        model = tweetnlp.load('sentiment')

        while True:
            unprocessed_tweets = Tweets.objects.filter(sentiment_done=False)[0:2]
            if not unprocessed_tweets:
                pass
            else:
                for up_tweet in unprocessed_tweets:
                    tweet_author = Authors.objects.filter(author_id=up_tweet.author_id)
                    if tweet_author.exists():
                        tweet_author = tweet_author.first()
                    else:
                        tweet_author = Authors(
                            author_id=up_tweet.author_id
                        )
                        tweet_author.save()

                    sentiment = model.sentiment(up_tweet.tweet_text)
                    up_tweet.sentiment_done = True

                    if sentiment == 'negative':
                        up_tweet.sentiment_score = 0
                        tweet_author.neg_count += 1
                        tweet_author.l1 = True
                    elif sentiment == 'neutral':
                        up_tweet.sentiment_score = 1
                        tweet_author.neutral_count += 1
                    elif sentiment == 'positive':
                        up_tweet.sentiment_score = 2
                        tweet_author.pos_count += 1

                    up_tweet.save()
                    tweet_author.save()
