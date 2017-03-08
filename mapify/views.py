from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

try:
    import json
except ImportError:
    import simplejson as json

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from elasticsearch import Elasticsearch

CONSUMER_KEY="jw6AtHQRo9gCcaQs6OzTzeNRT"
CONSUMER_SECRET="8oTz45vr3E63O0CP0bqmJf1vCVB8cwrwazRx4uh5jfbnjCM55p"

ACCESS_TOKEN="158373112-Yh9wdWSMxEXVAMAqJFabDbezzDucgctnRaoIx3nb"
ACCESS_SECRET="HMd4PNldTgLxcukctoc2Jp8DMtibxDGa7LhtzxFf7kS5I"

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = TwitterStream(auth=oauth)

es = Elasticsearch(['https://search-mapify-tweets-pcgkfb5ccbz3zi2ptcnkmsiqfi.us-east-1.es.amazonaws.com/'])
#Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

tweet_count = 1000
for tweet in iterator:
    tweet_count -= 1
    tw = json.dumps(tweet)
    try:
        es.index(index="idx_twp", doc_type="twitter_twp", id=tw['id'], body=tw)
    except Exception:
        pass
    #print (type(tw))
    if tweet_count <= 0:
        break

res = es.search(index="idx_twp", doc_type="twitter_twp", q = 'text:"dormir"')
# print(res)

class LandingView(generic.ListView):
    template_name = 'teamupapp/index.html'
    context_object_name = 'category_list'


def myApplications(request, userId):
    myAppsList = ()
    return render(request, 'teamupapp/myapps.html', {'myAppslist': myAppsList})