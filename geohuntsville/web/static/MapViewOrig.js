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

map.on('click', function (e) {
    var features = map.queryRenderedFeatures(e.point, { layers: ['points'] });
    var html = (features.length > 0) ?
        features[0].properties.description :
        '<form id="waypointEdit" method="dialog">' +
            '<h3>Add New Intel</h3>' +
            'Description:<br>' +
            '<input type="description" name="description"><br>' +
            'Type:<br>' +
            '<select name="title">' +
                '<option>Fire</option>' +
                '<option>Flooding</option>' +
                '<option>Injuries</option>' +
                '</select>' +
            '</section>' +
            '<menu>' +
                '<button onClick="submitWaypoint(' + e.lngLat.lng + ', ' + e.lngLat.lat + ')" type="submit">Save</button>' +
            '</menu>' +
        '</form>';
    var lngLat = (features.length > 0) ? features[0].geometry.coordinates : [e.lngLat.lng, e.lngLat.lat];
    var popup = new mapboxgl.Popup()
        .setLngLat(lngLat)
        .setHTML(html)
        .addTo(map)
        .on("close", function(){
            //refreshWaypoints();
        });
});

// create the popup
var popup = new mapboxgl.Popup({offset: 25})
    .setText('Construction on the Washington Monument began in 1848.');

// create DOM element for the marker
var el = document.createElement('div');
el.id = 'marker';

window.submitWaypoint = function(lng, lat) {
    var form = new FormData(document.querySelector('#waypointEdit'));
    var data = {
      "lon": lng,
      "lat": lat,
      "data": {
        "title": form.get("title"),
        "description": form.get("description")
      }
    }
    console.log(data);
    var req = http.request({
      hostname: 'localhost',
      port: 8080,
      path: '/api/waypoint',
      method: 'POST'
    });
    req.write(JSON.stringify(data))
    req.end();
}

// create the marker

map.on('load', function () {
    var options = {
      hostname: 'localhost',
      port: 8080,
      path: '/api/query?x1=-2000&y1=-20000&x2=10000&y2=10000',
      method: 'GET'
    };
    var req = http.request(options, function (res) {
        res.on('data', function (d) {
            var reply = JSON.parse(d);
            var geojson = {
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
            };
            map.addLayer(geojson);

            reply.features.forEach(function(marker) {
                if (marker.properties.iconSize && marker.properties.icon) {
                    // create a DOM element for the marker
                    var el = document.createElement('div');
                    el.className = 'marker';
                    var url = 'url(' + marker.properties.icon + ')';
                    el.style.backgroundImage = url;
                    el.style.width = marker.properties.iconSize[0] + 'px';
                    el.style.height = marker.properties.iconSize[1] + 'px';

                    new mapboxgl.Marker(el, {offset: [-marker.properties.iconSize[0] / 2, -marker.properties.iconSize[1] / 2]})
                                .setLngLat(marker.geometry.coordinates)
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





