import json
import logging

from geohuntsville.geodb import GeoDb

logger = logging.getLogger(__name__)

def load_test_db():
    db = GeoDb()
    with open('data/coordinates.json') as fp:
        x = json.load(fp)
        logger.info("loading")
        for data in x:
            logger.debug(data)
            db.insert(data['coordinate'][0], data['coordinate'][1], data['data'])
    return db
