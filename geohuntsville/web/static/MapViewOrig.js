mapboxgl.accessToken = 'pk.eyJ1IjoidGhlY2t3b2xmIiwiYSI6ImNpemx5MjNvdDAxcG0zM283eGUyaWd1bDkifQ.AtiIZ0g0yx0PmrcWWPsYTg';
const http = require('http');
var reply;
var options = {
  hostname: 'localhost',
  port: 8080,
  path: '/api/query?x1=-2000&y1=-20000&x2=10000&y2=10000',
  method: 'GET'
};
var monument = [-86.601791, 34.738228];
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/outdoors-v9',
    center: monument,
    zoom: 15
});

// create the popup
var popup = new mapboxgl.Popup({offset: 25})
    .setText('Construction on the Washington Monument began in 1848.');

// create DOM element for the marker
var el = document.createElement('div');
el.id = 'marker';

// create the marker

map.on('load', function () {
    var req = http.request(options, function (res) {
        res.on('data', function (d) {
            reply = JSON.parse(d);
            console.log('Response ' , reply);
            map.addLayer({
                "id": "points",
                "type": "symbol",
                "source": {
                    "type": "geojson",
                    "data": reply
                },
                "layout": {
                    "icon-image": "{icon}-15",
                    "text-field": "{title}",
                    "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
                    "text-offset": [0, 0.6],
                    "text-anchor": "top"
                }
            });
            map.on('click', function (e) {
                var features = map.queryRenderedFeatures(e.point, { layers: ['points'] });
                if (features.length > 0) {
                    var feature = features[0];
                    var popup = new mapboxgl.Popup()
                        .setLngLat(feature.geometry.coordinates)
                        .setHTML(feature.properties.description)
                        .addTo(map);
                }
            });
        });
    });
    req.on('error', function (e) {
        console.error(e);
    });
    req.end();


});






