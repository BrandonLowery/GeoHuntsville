mapboxgl.accessToken = 'pk.eyJ1IjoidGhlY2t3b2xmIiwiYSI6ImNpemx5MjNvdDAxcG0zM283eGUyaWd1bDkifQ.AtiIZ0g0yx0PmrcWWPsYTg';
var rest = require('rest');
var data;
rest('http://localhost:8080/api/query?x1=-2000&y1=-20000&x2=10000&y2=10000').then(function(response) {
    console.log('response: ', JSON.stringify(response));
    data = response;
});

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
    map.addLayer(data);
});


