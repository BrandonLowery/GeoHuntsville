import json
import logging

import bottle

from geohuntsville.load_test_db import load_test_db
from geohuntsville.geodb import GeoDb
from geohuntsville import twitter_streaming

logger = logging.getLogger(__name__)
db = GeoDb()


@bottle.get('/')
def index():
    return bottle.static_file('index.html', 'web')


@bottle.get('/static/<name>')
def static_file(name):
    return bottle.static_file(name, 'web/static')


@bottle.get('/api/query')
def query():
    bottle.response.content_type = 'application/json'
    query = bottle.request.query
    (x1, y1, x2, y2) = [float(query[p]) for p in ['x1', 'y1', 'x2', 'y2']]
    logger.debug("Query {}, {} {}, {}".format(x1, y1, x2, y2))
    return db.query(x1, y1, x2, y2)


@bottle.post('/api/waypoint')
def add_waypoint():
    waypoint = json.loads(bottle.request.body.read())
    lon = waypoint['lon']
    lat = waypoint['lat']
    data = waypoint['data']
    logger.debug("Add waypoint at {}, {}: {}".format(lon, lat, data))
    db.insert(lon, lat, data)


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout,
                        format='[%(asctime)s][%(filename)s:%(lineno)s][%(levelname)s] %(message)s')
    load_test_db(db, 'data/historical_tweets.json')
    load_test_db(db, 'data/coordinates.json')

    twitter_streaming.start_daemon(db)
    bottle.run(host='localhost', port=8080)