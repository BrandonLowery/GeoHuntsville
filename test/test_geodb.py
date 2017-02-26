import unittest

from geohuntsville.geodb import GeoDb


class TestGeoDb(unittest.TestCase):
    def test_query_empty_result(self):
        db = GeoDb()
        self.assertEqual(db.query(0, 0, 1, 1), {
            "type": "FeatureCollection",
            "features": []
        })

    def test_query_filters_points(self):
        db = GeoDb()
        db.insert(0, 0, {"c": "0,0"})
        db.insert(5, 0, {"c": "5,0"})
        db.insert(0, 5, {"c": "0,5"})
        self.assertEqual(db.query(4, 0, 6, 1), {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [5, 0]
                    },
                    "properties": {
                        "id": 1001,
                        "c": "5,0"
                    }
                }
            ]
        })

if __name__ == '__main__':
    unittest.main()