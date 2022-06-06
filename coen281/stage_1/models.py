from django.db import models


# Create your models here.
class Tweets(models.Model):
    tweet_id = models.BigIntegerField(primary_key=True)
    author_id = models.BigIntegerField()
    tweet_text = models.CharField(max_length=1000)
    tweet_clean = models.CharField(max_length=1000, default="")
    sentiment_done = models.BooleanField(default=False)
    sentiment_score = models.FloatField(default=0)
    ens1_score = models.FloatField(default=0)
