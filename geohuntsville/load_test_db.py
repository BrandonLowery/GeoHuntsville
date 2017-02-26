import json
import logging

logger = logging.getLogger(__name__)


def load_test_db(db, name):
    with open(name) as fp:
        for data in json.load(fp):
            try:
                db.insert(data['coordinate'][0], data['coordinate'][1], data['data'])
            except Exception as e:
                logger.error(e)
    return db
