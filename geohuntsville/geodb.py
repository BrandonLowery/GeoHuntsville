from collections import namedtuple

PointData = namedtuple('PointData', ['lon', 'lat', 'data'])


def idgen():
    nextpid = 1000
    while True:
        yield nextpid
        nextpid += 1


class GeoDb(object):
    def __init__(self):
        self._idgen = idgen()
        self._points = {}  # id -> PointData

    def query(self, lon1, lat1, lon2, lat2):
        x1 = min(lon1, lon2)
        x2 = max(lon1, lon2)
        y1 = min(lat1, lat2)
        y2 = max(lat1, lat2)
        return self._feature_collection([
            self._feature_point(pid, point)
            for pid, point in self._points.iteritems()
            if self._point_in(point, x1, y1, x2, y2)
        ])

    def insert(self, lon, lat, data):
        pid = self._idgen.next()
        self._points[pid] = PointData(lon, lat, data)
        return pid

    @staticmethod
    def _point_in(point, x1, y1, x2, y2):
        return x1 <= point.lon < x2 and \
               y1 <= point.lat < y2

    @staticmethod
    def _feature_point(pid, point):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point.lon, point.lat]
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