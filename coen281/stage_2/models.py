from django.db import models


# Create your models here.
class Authors(models.Model):
    author_id = models.BigIntegerField(primary_key=True)
    l1 = models.BooleanField(default=False)
    l1_done = models.BooleanField(default=False)
    l2 = models.BooleanField(default=False)
    l2_done = models.BooleanField(default=False)
    l3 = models.BooleanField(default=False)
    l3_done = models.BooleanField(default=False)
    neutral_count = models.IntegerField(default=0)
    pos_count = models.IntegerField(default=0)
    neg_count = models.IntegerField(default=0)
    anger_count = models.IntegerField(default=0)
    joy_count = models.IntegerField(default=0)
    optimism_count = models.IntegerField(default=0)
    sadness_count = models.IntegerField(default=0)
