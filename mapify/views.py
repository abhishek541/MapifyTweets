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

# tweet_count = 100
# for tweet in iterator:
#     tweet_count -= 1
#     tw = json.dumps(tweet)
#     try:
#         es.index(index="idx_twp", doc_type="twitter_twp", id=1, body=tw)
#     except Exception:
#         pass
#     print (tw)
#     if tweet_count <= 0:
#         break

# print(res)

# res = es.search(index="idx_twp", doc_type="twitter_twp", q='text:"a"')
# print(res)

def getTweets(request):
    try:
        keyword = request.POST['keyword']
    except:
        keyword = ""
    print("keyword: "+keyword)
    res = es.search(index="idx_twp", doc_type="twitter_twp", q='text:"'+keyword+'"', scroll='60s', search_type='query_then_fetch')
    scroll_size = res['hits']['total']
    tweetJson = []
    while (scroll_size > 0):
        try:
            scroll_id = res['_scroll_id']
            res = es.scroll(scroll_id=scroll_id, scroll='60s')
            tweetJson += res['hits']['hits']
            scroll_size = len(res['hits']['hits'])
        except:
            break
    coordinatesList = []
    for r in tweetJson:
        if (r['_source']['coordinates']):
            coordinatesList.append(r['_source']['coordinates'])
    #print("result: "+json.dumps(coordinatesList))
    return render(request, 'mapify/index.html', {'tweetCoord': json.dumps(coordinatesList)})