import sys
import tweepy



consumer_key = "rkH0NIP5aB1b9GHtYRrCWsqiA"
consumer_secret = "kII4RFh3BqzYFuILOkW6GsFh0bW7oRFuTUe4NSh2giTDhYHERX"
access_key = "835721764642689025-e1M8kqmOFEumeqHbm6Kz0Si2yLR5qDp"
access_secret = "toDR8GtW0JlIRZgoB1NSGcWhTIMkVSH7A55m1HASGX6qk"



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    #def __init__(self):
       # pass
    def on_status(self, status):
        #print status
       # print "tweet recieved"
        text = str(status)
        self.parse(text)


    def parse(self, text):

        find = "=u"
        find2 = "is_quote_status=True"
        find3= "is_quote_status=False"
        #first = text.rfind(find) #get begin of tweet element
        #second = text.rfind(find2, first+1) #get end of tweet element
        first = text.find(find)
        second = text.find(find2)
        third = text.find(find3)
        if second>5: #if-elif block to test for 2  dif ending keyword possibilities
            end = second
            text2 = text[first:]  # cut first bit up to tweet off
            text3 = text2[2:]  # clean beginning a bit
            text4 = text3[:second]  # cut end off

        elif third>5:
            end = third
            text2 = text[first:]  # cut first bit up to tweet off
            text3 = text2[2:]  # clean beginning a bit
            text4 = text3[:third]  # cut end off

        print text4


    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code ', status_code
        return True  #continue string

    def on_timeout(self):
        print >> sys.stderr, 'Timeout'
        return True # continue stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())

#sapi.filter(locations=[-74.734497, 40.454001,73.317261,41.663423]) #NYC for testing
sapi.filter(locations=[-86.886063, 34.51561, -86.211777, 34.906205]) #need import from geodb.py huntsville

