import logging

import bottle

from geohuntsville.load_test_db import load_test_db

logger = logging.getLogger(__name__)
db = load_test_db()

@bottle.get('/')
def index():
    return bottle.static_file('index.html', 'web')

@bottle.get('/api/query')
def query():
    bottle.response.content_type = 'application/json'
    query = bottle.request.query
    (x1, x2, y1, y2) = [float(query[p]) for p in ['x1', 'y1', 'x2', 'y2']]
    logger.debug("Query {}, {} {}, {}".format(x1, y1, x2, y2))
    return db.query(x1, y1, x2, y2)

if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout,
                        format='[%(asctime)s][%(filename)s:%(lineno)s][%(levelname)s] %(message)s')
    bottle.run(host='localhost', port=8080)