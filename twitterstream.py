try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
import tweepy
from elasticsearch import Elasticsearch
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

CONSUMER_KEY="jw6AtHQRo9gCcaQs6OzTzeNRT"
CONSUMER_SECRET="8oTz45vr3E63O0CP0bqmJf1vCVB8cwrwazRx4uh5jfbnjCM55p"

ACCESS_TOKEN="158373112-Yh9wdWSMxEXVAMAqJFabDbezzDucgctnRaoIx3nb"
ACCESS_SECRET="HMd4PNldTgLxcukctoc2Jp8DMtibxDGa7LhtzxFf7kS5I"

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

es = Elasticsearch(['https://search-mapify-tweets-pcgkfb5ccbz3zi2ptcnkmsiqfi.us-east-1.es.amazonaws.com/'])

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            #json_data = status._json
            tweet = json.loads(data)
            #print (tweet)
            if tweet['coordinates']:
                print (tweet['coordinates'])
            es.index(index="idx_twp", doc_type="twitter_twp", id=tweet["id"], body=tweet)
        except Exception as e:
            #print("exception: "+e)
            pass

        def on_error(self, status):
            print(status)
            return True

def start_stream():
    while True:
        try:
            twitter_stream = Stream(auth, MyListener())
            twitter_stream.filter(locations=[-180,-90,180,90])
        except:
            continue

start_stream()