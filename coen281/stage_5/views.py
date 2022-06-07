from django.shortcuts import render
from stage_1.models import Tweets
from stage_2.models import Authors
from utils.ChartManager import ChartManager


# Create your views here.
def index(request):
    authors = Authors.objects.filter(l1_done=True, l2_done=True, l3_done=True).order_by("-neg_count")[0:10]
    author_list = []
    for idx, author in enumerate(authors):
        author_list.append(
            {
                "author_id": author.author_id,
                "name": "Author " + str(idx+1)
            }
        )

    context = {
        'authors': author_list
    }

    return render(request, 'home.html', context)


def overall(request):
    chart_man = ChartManager()

    # sentiment chart
    neg_count = Tweets.objects.filter(sentiment_score=0).count()
    neu_count = Tweets.objects.filter(sentiment_score=1).count()
    pos_count = Tweets.objects.filter(sentiment_score=2).count()

    x = ("Negative", "Neutral", "Positive")
    y = (neg_count, neu_count, pos_count)

    chart_sent = chart_man.get_bar_graph(x, y)

    # emotion chart
    anger_count = Tweets.objects.filter(emotion=0).count()
    joy_count = Tweets.objects.filter(emotion=1).count()
    opt_count = Tweets.objects.filter(emotion=2).count()
    sad_count = Tweets.objects.filter(emotion=3).count()

    x = ("Anger", "Joy", "Optimism", "Sadness")
    y = (anger_count, joy_count, opt_count, sad_count)

    chart_emo = chart_man.get_bar_graph(x, y)

    # harvest chart
    l1_auth_count = Authors.objects.filter(l1=True, l1_done=True, l2=False, l3=False).count()
    l2_auth_count = Authors.objects.filter(l2=True, l2_done=True, l3=False).count()
    l3_auth_count = Authors.objects.filter(l3=True, l3_done=True).count()
    rem_auth_count = Authors.objects.filter(l1=False).count()

    x = (l1_auth_count, l2_auth_count, l3_auth_count, rem_auth_count)
    lbl = ("Level 1", "Level 2", "Level 3", "Uninteresting")
    exp = (1, 2, 3, 4)

    chart_harvest = chart_man.get_pie_chart(x, lbl, exp)

    # numbers
    tot_twt_count = Tweets.objects.all().count()
    tot_auth_count = Authors.objects.all().count()

    numbers = {
        "tweets": tot_twt_count,
        "authors": tot_auth_count,
        "est_tweets": tot_auth_count*100,
        "l1": l1_auth_count,
        "l2": l2_auth_count,
        "l3": l3_auth_count,
        "rem": rem_auth_count
    }

    context = {
        'chart_sent': chart_sent,
        'chart_emo': chart_emo,
        'chart_harvest': chart_harvest,
        'numbers': numbers
    }
    return render(request, 'overall.html', context)


def author_det(request, a_id):
    chart_man = ChartManager()

    # sentiment chart
    neg_count = Tweets.objects.filter(author_id=a_id, sentiment_score=0).count()
    neu_count = Tweets.objects.filter(author_id=a_id, sentiment_score=1).count()
    pos_count = Tweets.objects.filter(author_id=a_id, sentiment_score=2).count()

    x = ("Negative", "Neutral", "Positive")
    y = (neg_count, neu_count, pos_count)

    chart_sent = chart_man.get_bar_graph(x, y)

    # emotion chart
    anger_count = Tweets.objects.filter(author_id=a_id, emotion=0).count()
    joy_count = Tweets.objects.filter(author_id=a_id, emotion=1).count()
    opt_count = Tweets.objects.filter(author_id=a_id, emotion=2).count()
    sad_count = Tweets.objects.filter(author_id=a_id, emotion=3).count()

    x = ("Anger", "Joy", "Optimism", "Sadness")
    y = (anger_count, joy_count, opt_count, sad_count)

    chart_emo = chart_man.get_bar_graph(x, y)

    # numbers
    tot_twt_count = Tweets.objects.filter(author_id=a_id).count()

    numbers = {
        "tweets": tot_twt_count
    }

    context = {
        'chart_sent': chart_sent,
        'chart_emo': chart_emo,
        'numbers': numbers
    }

    return render(request, 'author.html', context)
