# Mapbox GL JS Reference

## Table of Contents
1. [Setup & Initialization](#setup)
2. [Styles & Layers](#styles)
3. [Markers & Popups](#markers)
4. [Clustering with Mapbox](#clustering)
5. [Sources & Data](#sources)
6. [Expressions & Data-Driven Styling](#expressions)
7. [Directions & Routing](#routing)
8. [3D Terrain & Buildings](#3d)
9. [Events & Interaction](#events)
10. [Performance](#performance)

---

## Setup {#setup}

### npm
```bash
npm install mapbox-gl
```

### CDN
```html
<link href="https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.css" rel="stylesheet" />
<script src="https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.js"></script>
```

### Basic Initialization

**CRITICAL: Mapbox GL uses `[lng, lat]` order — opposite to Leaflet/Google Maps.**

```javascript
mapboxgl.accessToken = 'YOUR_TOKEN';

const map = new mapboxgl.Map({
  container: 'map',                // HTML element ID or element reference
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [-57.5759, -25.2637],   // [lng, lat] — Asunción
  zoom: 12,
  pitch: 0,                        // Tilt angle (0-85)
  bearing: 0,                      // Rotation
  maxZoom: 20,
  minZoom: 2,
  attributionControl: true,
  cooperativeGestures: true         // Require ctrl+scroll to zoom (good for embedded)
});

// Add controls
map.addControl(new mapboxgl.NavigationControl(), 'top-right');
map.addControl(new mapboxgl.ScaleControl({ unit: 'metric' }), 'bottom-left');
map.addControl(new mapboxgl.FullscreenControl(), 'top-right');
map.addControl(new mapboxgl.GeolocateControl({
  positionOptions: { enableHighAccuracy: true },
  trackUserLocation: true
}));
```

### Available Styles
```
mapbox://styles/mapbox/streets-v12
mapbox://styles/mapbox/outdoors-v12
mapbox://styles/mapbox/light-v11
mapbox://styles/mapbox/dark-v11
mapbox://styles/mapbox/satellite-v9
mapbox://styles/mapbox/satellite-streets-v12
mapbox://styles/mapbox/navigation-day-v1
mapbox://styles/mapbox/navigation-night-v1
```

---

## Markers & Popups {#markers}

### Default Marker
```javascript
const marker = new mapboxgl.Marker()
  .setLngLat([-57.5759, -25.2637])
  .setPopup(new mapboxgl.Popup().setHTML('<h3>Asunción</h3>'))
  .addTo(map);
```

### Custom HTML Marker
```javascript
const el = document.createElement('div');
el.className = 'custom-marker';
el.style.cssText = 'width:32px;height:32px;background:url(pin.png) center/cover;cursor:pointer;';

const marker = new mapboxgl.Marker({ element: el, anchor: 'bottom' })
  .setLngLat([-57.5759, -25.2637])
  .setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML('<p>Custom marker</p>'))
  .addTo(map);
```

### Symbol Layer (GPU-accelerated, for many markers)
```javascript
// Use symbol layers instead of DOM markers for 100+ points
map.on('load', () => {
  // Load custom icon
  map.loadImage('marker.png', (error, image) => {
    if (error) throw error;
    map.addImage('custom-pin', image);

    map.addSource('points', {
      type: 'geojson',
      data: {
        type: 'FeatureCollection',
        features: points.map(p => ({
          type: 'Feature',
          geometry: { type: 'Point', coordinates: [p.lng, p.lat] },
          properties: { name: p.name, category: p.category }
        }))
      }
    });

    map.addLayer({
      id: 'points-layer',
      type: 'symbol',
      source: 'points',
      layout: {
        'icon-image': 'custom-pin',
        'icon-size': 0.5,
        'icon-allow-overlap': false,
        'text-field': ['get', 'name'],
        'text-offset': [0, 1.5],
        'text-anchor': 'top',
        'text-size': 12
      }
    });
  });
});
```

---

## Clustering with Mapbox {#clustering}

Mapbox has native clustering support via GeoJSON sources — no plugins needed.

```javascript
map.on('load', () => {
  map.addSource('locations', {
    type: 'geojson',
    data: geojsonData,
    cluster: true,
    clusterMaxZoom: 14,
    clusterRadius: 50,
    clusterProperties: {
      // Aggregate properties across cluster
      'sum_value': ['+', ['get', 'value']]
    }
  });

  // Cluster circles
  map.addLayer({
    id: 'clusters',
    type: 'circle',
    source: 'locations',
    filter: ['has', 'point_count'],
    paint: {
      'circle-color': [
        'step', ['get', 'point_count'],
        '#51bbd6',    // < 10
        10, '#f1f075', // 10-50
        50, '#f28cb1'  // 50+
      ],
      'circle-radius': [
        'step', ['get', 'point_count'],
        20,           // < 10: 20px
        10, 30,       // 10-50: 30px
        50, 40        // 50+: 40px
      ]
    }
  });

  // Cluster count labels
  map.addLayer({
    id: 'cluster-count',
    type: 'symbol',
    source: 'locations',
    filter: ['has', 'point_count'],
    layout: {
      'text-field': ['get', 'point_count_abbreviated'],
      'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
      'text-size': 12
    }
  });

  // Individual points
  map.addLayer({
    id: 'unclustered-point',
    type: 'circle',
    source: 'locations',
    filter: ['!', ['has', 'point_count']],
    paint: {
      'circle-color': '#11b4da',
      'circle-radius': 6,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#fff'
    }
  });

  // Click cluster to zoom in
  map.on('click', 'clusters', async (e) => {
    const features = map.queryRenderedFeatures(e.point, { layers: ['clusters'] });
    const clusterId = features[0].properties.cluster_id;
    const zoom = await map.getSource('locations').getClusterExpansionZoom(clusterId);
    map.easeTo({ center: features[0].geometry.coordinates, zoom });
  });

  // Click individual point
  map.on('click', 'unclustered-point', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
      .setLngLat(e.features[0].geometry.coordinates)
      .setHTML(`<h3>${props.name}</h3>`)
      .addTo(map);
  });

  // Cursor pointer on hover
  map.on('mouseenter', 'clusters', () => map.getCanvas().style.cursor = 'pointer');
  map.on('mouseleave', 'clusters', () => map.getCanvas().style.cursor = '');
});
```

---

## Sources & Data {#sources}

```javascript
// GeoJSON source (inline or URL)
map.addSource('areas', {
  type: 'geojson',
  data: 'https://api.example.com/areas.geojson'  // or inline object
});

// Vector tiles
map.addSource('custom-tiles', {
  type: 'vector',
  url: 'mapbox://username.tileset-id'
});

// Raster tiles (e.g., weather overlay)
map.addSource('radar', {
  type: 'raster',
  tiles: ['https://mesonet.agron.iastate.edu/cache/tile.py/1.0.0/nexrad-n0q-900913/{z}/{x}/{y}.png'],
  tileSize: 256
});

// Update GeoJSON source dynamically
map.getSource('areas').setData(newGeojsonData);
```

### Layer Types
```javascript
// Fill (polygons)
map.addLayer({ id: 'fill', type: 'fill', source: 'areas',
  paint: { 'fill-color': '#088', 'fill-opacity': 0.5 } });

// Line
map.addLayer({ id: 'route', type: 'line', source: 'route',
  paint: { 'line-color': '#0066ff', 'line-width': 4 },
  layout: { 'line-cap': 'round', 'line-join': 'round' } });

// Circle (points)
map.addLayer({ id: 'points', type: 'circle', source: 'points',
  paint: { 'circle-radius': 6, 'circle-color': '#ff0000' } });

// Heatmap
map.addLayer({ id: 'heat', type: 'heatmap', source: 'points',
  paint: {
    'heatmap-weight': ['get', 'intensity'],
    'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 15, 3],
    'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 2, 15, 20],
    'heatmap-color': [
      'interpolate', ['linear'], ['heatmap-density'],
      0, 'rgba(0,0,255,0)', 0.2, 'blue', 0.4, 'cyan',
      0.6, 'lime', 0.8, 'yellow', 1, 'red'
    ]
  }
});

// Extrusion (3D buildings)
map.addLayer({ id: 'buildings', type: 'fill-extrusion', source: 'composite',
  'source-layer': 'building',
  paint: {
    'fill-extrusion-color': '#aaa',
    'fill-extrusion-height': ['get', 'height'],
    'fill-extrusion-base': ['get', 'min_height'],
    'fill-extrusion-opacity': 0.6
  }
});
```

---

## Expressions & Data-Driven Styling {#expressions}

```javascript
// Color by category
'circle-color': ['match', ['get', 'category'],
  'restaurant', '#ff0000',
  'shop', '#00ff00',
  'office', '#0000ff',
  '#888888'  // default
]

// Size by value
'circle-radius': ['interpolate', ['linear'], ['get', 'value'],
  0, 4,
  100, 20
]

// Filter
map.setFilter('points-layer', ['==', ['get', 'category'], 'restaurant']);
map.setFilter('points-layer', ['all',
  ['>=', ['get', 'value'], 50],
  ['==', ['get', 'active'], true]
]);
```

---

## Directions & Routing {#routing}

### Mapbox Directions API
```javascript
async function getRoute(start, end) {
  const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${start[0]},${start[1]};${end[0]},${end[1]}?geometries=geojson&overview=full&steps=true&access_token=${mapboxgl.accessToken}`;

  const res = await fetch(url);
  const data = await res.json();
  const route = data.routes[0];

  // Add route to map
  if (map.getSource('route')) {
    map.getSource('route').setData(route.geometry);
  } else {
    map.addSource('route', { type: 'geojson', data: route.geometry });
    map.addLayer({
      id: 'route',
      type: 'line',
      source: 'route',
      layout: { 'line-join': 'round', 'line-cap': 'round' },
      paint: { 'line-color': '#3887be', 'line-width': 5, 'line-opacity': 0.75 }
    });
  }

  return {
    distance: route.distance,
    duration: route.duration,
    steps: route.legs[0].steps
  };
}
```

### Mapbox GL Directions Plugin
```bash
npm install @mapbox/mapbox-gl-directions
```

```javascript
import MapboxDirections from '@mapbox/mapbox-gl-directions/dist/mapbox-gl-directions';
import '@mapbox/mapbox-gl-directions/dist/mapbox-gl-directions.css';

map.addControl(new MapboxDirections({
  accessToken: mapboxgl.accessToken,
  unit: 'metric',
  profile: 'mapbox/driving'
}), 'top-left');
```

---

## 3D Terrain & Buildings {#3d}

```javascript
map.on('load', () => {
  // 3D terrain
  map.addSource('mapbox-dem', {
    type: 'raster-dem',
    url: 'mapbox://mapbox.mapbox-terrain-dem-v1',
    tileSize: 512
  });
  map.setTerrain({ source: 'mapbox-dem', exaggeration: 1.5 });

  // Sky layer
  map.addLayer({
    id: 'sky',
    type: 'sky',
    paint: {
      'sky-type': 'atmosphere',
      'sky-atmosphere-sun': [0.0, 0.0],
      'sky-atmosphere-sun-intensity': 15
    }
  });
});
```

---

## Performance Tips {#performance}

1. **Use symbol/circle layers** instead of DOM markers for 100+ points — they're GPU-rendered
2. **Native clustering** is fast — use `cluster: true` on GeoJSON sources
3. **Filter layers** with `map.setFilter()` instead of removing/re-adding
4. **Update sources** with `setData()` instead of removing/re-adding source + layers
5. **Use `queryRenderedFeatures`** for hit testing — faster than iterating all features
6. **Limit `maxzoom`** on sources to reduce tile requests
7. **Debounce data updates** — `setData()` triggers full re-render
8. **Use `promoteId`** on sources for faster feature state updates
