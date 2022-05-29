from django.db import models


# Create your models here.
class Tweets(models.Model):
    tweet_id = models.BigIntegerField(primary_key=True)
    author_id = models.BigIntegerField()
    tweet_text = models.CharField(max_length=1000)
