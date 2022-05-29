import json
import mysql.connector

from django.http import HttpResponse
from django.shortcuts import render
from utils.SaveStream import SaveStream
from .models import Tweets


# Create your views here.
def index(request):
    # print("Start Data Generation")
    # save_stream = SaveStream()
    #
    # data = save_stream.get_recent_stream(count=5)
    #
    # for tweet_id in data:
    #     tweet = Tweets(
    #         tweet_id=int(tweet_id),
    #         author_id=int(data[tweet_id]["author_id"]),
    #         tweet_text=data[tweet_id]['text']
    #     )
    #     tweet.save()

    return HttpResponse("Done.")
