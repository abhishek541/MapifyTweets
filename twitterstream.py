try:
    import json
except ImportError:
    import simplejson as json

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from kafka import KafkaConsumer, KafkaProducer
import sys
import os
sys.path.append(os.path.join(os.getcwd(),'..'))
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features


ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)



class MyListener(StreamListener):
    def on_data(self, data):
        try:
            #json_data = status._json
            tweet = json.loads(data)
            textdata=tweet['text']
            # print textdata
            if tweet['coordinates']:
                print tweet['coordinates']
            #response = queue.send_message(MessageBody=tweet['text'])
            # print (tweet)
            producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send('fizzbuzz', textdata)


            consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                      auto_offset_reset='earliest')

            consumer.subscribe(['fizzbuzz'])
            for message in consumer:
                 print (message)

            nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                                        username='ak6210@nyu.edu',
                                                                        password='Cloud@12345')
            nlu.analyze(text=textdata,features=[features.Sentiment()])










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
            twitter_stream.filter(locations=[-180,-90,180,90],languages=['en'])
        except:
            continue

start_stream()





