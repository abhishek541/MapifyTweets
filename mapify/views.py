from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

try:
    import json
except ImportError:
    import simplejson as json

from elasticsearch import Elasticsearch

es = Elasticsearch(['https://search-trends-fxlmyom7rqfue7wr4oho5oh2nq.us-east-1.es.amazonaws.com/'])

def getTweets(request):
    #headers = request.headers
    print (request)
    try:
        keyword = request.POST['keyword']
    except:
        keyword = ""
    print("keyword: "+keyword)
    res = es.search(index="trends", doc_type="twitter_twp", q='text:"'+keyword+'"', scroll='60s', search_type='query_then_fetch')
    print("result: " + json.dumps(res))
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

    tweetList = []
    tweetList.append(keyword)
    for r in tweetJson:
        if (r['_source']['coordinates']):
            tweetList.append({'coordinates': r['_source']['coordinates'], 'sentiment': r['_source']['sentiment']})
    #print("result: "+json.dumps(tweetList))
    return render(request, 'mapify/index.html', {'tweetCoord': json.dumps(tweetList)})