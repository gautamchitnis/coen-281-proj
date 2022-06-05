from django.db import models


# Create your models here.
class Authors(models.Model):
    author_id = models.BigIntegerField(primary_key=True)
