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
    ens1_count = models.IntegerField(default=0)
