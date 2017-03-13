from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

try:
    import json
except ImportError:
    import simplejson as json

from elasticsearch import Elasticsearch

es = Elasticsearch(['https://search-mapify-tweets-pcgkfb5ccbz3zi2ptcnkmsiqfi.us-east-1.es.amazonaws.com/'])

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