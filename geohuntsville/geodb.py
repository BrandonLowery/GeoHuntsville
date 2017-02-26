from collections import namedtuple

PointData = namedtuple('PointData', ['lat', 'lon', 'data'])


def idgen():
    nextpid = 1000
    while True:
        yield nextpid
        nextpid += 1


class GeoDb(object):
    def __init__(self):
        self._idgen = idgen()
        self._points = {}  # id -> PointData

    def query(self, lat1, lon1, lat2, lon2):
        return self._feature_collection([
            self._feature_point(pid, point)
            for pid, point in self._points.iteritems()
            if self._point_in(point, lat1, lon1, lat2, lon2)
        ])

    def insert(self, lat, lon, data):
        pid = self._idgen.next()
        self._points[pid] = PointData(lat, lon, data)
        return pid

    @staticmethod
    def _point_in(point, lat1, lon1, lat2, lon2):
        return lat1 <= point.lat < lat2 and\
               lon1 <= point.lon < lon2

    @staticmethod
    def _feature_point(pid, point):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point.lat, point.lon]
            },
            "properties": {
                "id": pid,
                "data": point.data
            }
        }

    @staticmethod
    def _feature_collection(features):
        return {
            "type": "FeatureCollection",
            "features": features
        }