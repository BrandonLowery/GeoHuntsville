import logging
import sys
import tweepy

logger = logging.getLogger(__name__)

consumer_key = "rkH0NIP5aB1b9GHtYRrCWsqiA"
consumer_secret = "kII4RFh3BqzYFuILOkW6GsFh0bW7oRFuTUe4NSh2giTDhYHERX"
access_key = "835721764642689025-e1M8kqmOFEumeqHbm6Kz0Si2yLR5qDp"
access_secret = "toDR8GtW0JlIRZgoB1NSGcWhTIMkVSH7A55m1HASGX6qk"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, db):
        super(CustomStreamListener, self).__init__()
        self.db = db

    def on_status(self, status):
        if status.coordinates is not None:
            logger.debug(status)
            data = self.format_tweet(status)
            self.db.insert(data['coordinate'][0], data['coordinate'][1], data['data'])

    def on_error(self, status_code):
        logger.error('Encountered error with status code {}'.format(status_code))
        return True

    def on_timeout(self):
        logger.error('Timeout')
        return True

    @staticmethod
    def format_tweet(tweet):
        return {
            "data": {
                "icon": "",
                "title": "tweet",
                "description": tweet.text
            },
            "coordinate": tweet.coordinates['coordinates'] if tweet.coordinates is not None else [0, 0]
        }


def start_daemon(db):
    import threading

    def collector():
        logger.debug('Starting tweet collector')
        sapi = tweepy.streaming.Stream(auth, CustomStreamListener(db))
        sapi.filter(locations=[-86.886063, 34.51561, -86.211777, 34.906205]) #need import from geodb.py huntsville

    t = threading.Thread(target=collector)
    t.daemon = True
    t.start()
