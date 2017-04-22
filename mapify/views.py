from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

try:
    import json
except ImportError:
    import simplejson as json

from elasticsearch import Elasticsearch

#es = Elasticsearch(['https://search-assignment1testdomain-mmaspwfvkwmpvzcydmwkzoa2qa.us-east-1.es.amazonaws.com/'])

def getTweets(request):
    #headers = request.headers
    print (request)
    try:
        keyword = request.POST['keyword']
    except:
        keyword = ""
    print("keyword: "+keyword)
    #res = es.search(index="idx_twp", doc_type="twitter_twp", q='text:"'+keyword+'"', scroll='60s', search_type='query_then_fetch')
    #scroll_size = res['hits']['total']
    scroll_size = 0
    tweetJson = []

    coordinatesList = []
    coordinatesList.append(keyword)
    for r in tweetJson:
        if (r['_source']['coordinates']):
            coordinatesList.append(r['_source']['coordinates'])
    #print("result: "+json.dumps(coordinatesList))
    return render(request, 'mapify/index.html', {'tweetCoord': json.dumps(coordinatesList)})