import json
import logging

from geohuntsville.geodb import GeoDb

logger = logging.getLogger(__name__)


def load_test_db():
    db = GeoDb()
    with open('data/coordinates.json') as fp:
        for data in json.load(fp):
            db.insert(data['coordinate'][0], data['coordinate'][1], data['data'])
    return db
