from urllib2 import urlopen
import tornado.ioloop
import tornado.web
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print 'get'
        self.sns()
        self.write(self.request.body.decode('utf-8'))

    def post(self):
        print 'post'
        self.sns()
        self.write(self.request.body.decode('utf-8'))

    def sns(self):
        headers = self.request.headers
        print ('HEADER: {}'.format(headers))
        arn = headers.get('x-amz-sns-subscription-arn')
        obj = json.loads(self.request.body.decode())

        if headers.get('x-amz-sns-message-type') == 'SubscriptionConfirmation':
            print('REQUEST: {}'.format(self.request))
            subscribe_url = obj[u'SubscribeURL']
            print ('URL:{}'.format(subscribe_url))
            res = urlopen(subscribe_url)

        elif headers.get('x-amz-sns-message-type') == 'UnsubscribeConfirmation':
            print 'Unsubscription'

        elif headers.get('x-amz-sns-message-type') == 'Notification':

            print 'Unsubscription'

        return '', 200


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()



