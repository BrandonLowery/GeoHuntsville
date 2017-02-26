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
    def __init__(self, *args, **kwargs):
        super(CustomStreamListener, self).__init__(*args, **kwargs)
        self.tweets = []

    def on_status(self, status):
        if status.coordinates is not None:
            print status
            try:
                self.tweets.append({
                    "data": {
                        "icon": "",
                        "title": "tweet",
                        "description": str(status.text)
                    },
                    "coordinate": status.coordinates['coordinates']
                })
                import json
                with open("historical_tweets.json", "w+b") as fp:
                    json.dump(self.tweets, fp, indent=4)
            except Exception as e:
                print e

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code ', status_code
        return True  #continue string

    def on_timeout(self):
        print >> sys.stderr, 'Timeout'
        return True # continue stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())

sapi.filter(locations=[-86.886063, 34.51561, -86.211777, 34.906205]) #need import from geodb.py huntsville

