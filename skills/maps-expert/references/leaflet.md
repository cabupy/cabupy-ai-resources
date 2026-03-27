# Leaflet Reference

## Table of Contents
1. [Setup & Initialization](#setup)
2. [Tile Providers](#tiles)
3. [Markers & Icons](#markers)
4. [Marker Clustering](#clustering)
5. [GeoJSON & Vector Layers](#geojson)
6. [Routing](#routing)
7. [Drawing & Editing](#drawing)
8. [Events & Interaction](#events)
9. [Plugins Ecosystem](#plugins)
10. [Performance Tips](#performance)

---

## Setup {#setup}

### CDN (vanilla JS)
```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
```

### npm
```bash
npm install leaflet
npm install -D @types/leaflet  # TypeScript
```

### Basic Initialization
```javascript
const map = L.map('map', {
  center: [-25.2637, -57.5759],  // Asunción
  zoom: 13,
  zoomControl: true,
  attributionControl: true,
  maxZoom: 19,
  minZoom: 3
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
```

### Important: Leaflet uses `[lat, lng]` order everywhere.

---

## Tile Providers {#tiles}

```javascript
// OpenStreetMap (default, free)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap contributors'
});

// Mapbox (via Leaflet raster tiles)
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  id: 'mapbox/streets-v12',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: 'YOUR_TOKEN'
});

// Stadia Maps
L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
  maxZoom: 20,
  attribution: '© Stadia Maps, © OpenMapTiles, © OpenStreetMap'
});

// CartoDB
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  maxZoom: 20,
  attribution: '© CARTO'
});

// Layer switching
const baseMaps = {
  'Streets': osmLayer,
  'Satellite': satelliteLayer,
  'Terrain': terrainLayer
};
L.control.layers(baseMaps).addTo(map);
```

---

## Markers & Icons {#markers}

### Default Marker
```javascript
const marker = L.marker([-25.2637, -57.5759])
  .addTo(map)
  .bindPopup('<strong>Asunción</strong><br>Capital de Paraguay');
```

### Custom Icon
```javascript
const customIcon = L.icon({
  iconUrl: 'marker-icon.png',
  iconRetinaUrl: 'marker-icon-2x.png',
  shadowUrl: 'marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],    // Point of the icon that corresponds to marker's location
  popupAnchor: [1, -34],   // Point from which the popup opens relative to iconAnchor
  shadowSize: [41, 41]
});
L.marker([-25.2637, -57.5759], { icon: customIcon }).addTo(map);
```

### DivIcon (HTML/CSS markers — better for custom designs)
```javascript
const divIcon = L.divIcon({
  className: 'custom-marker',  // Your CSS class
  html: `<div class="marker-pin">
           <span class="marker-label">42</span>
         </div>`,
  iconSize: [30, 42],
  iconAnchor: [15, 42],
  popupAnchor: [0, -42]
});
```

### Circle Markers (Canvas-rendered, much faster for many points)
```javascript
L.circleMarker([-25.2637, -57.5759], {
  radius: 8,
  fillColor: '#ff7800',
  color: '#000',
  weight: 1,
  opacity: 1,
  fillOpacity: 0.8
}).addTo(map);
```

---

## Marker Clustering {#clustering}

### Leaflet.markercluster
```bash
npm install leaflet.markercluster
```

```javascript
import 'leaflet.markercluster';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';

const clusterGroup = L.markerClusterGroup({
  chunkedLoading: true,          // Load markers in chunks (prevents UI freeze)
  chunkInterval: 200,
  chunkDelay: 50,
  maxClusterRadius: 80,          // Pixel radius to cluster within
  spiderfyOnMaxZoom: true,
  showCoverageOnHover: false,
  zoomToBoundsOnClick: true,
  disableClusteringAtZoom: 18,   // Show individual markers at this zoom

  // Custom cluster icon
  iconCreateFunction: (cluster) => {
    const count = cluster.getChildCount();
    let size = 'small';
    if (count > 100) size = 'large';
    else if (count > 10) size = 'medium';

    return L.divIcon({
      html: `<div class="cluster-${size}"><span>${count}</span></div>`,
      className: 'marker-cluster',
      iconSize: L.point(40, 40)
    });
  }
});

// Add markers in bulk
const markers = data.map(point =>
  L.marker([point.lat, point.lng])
   .bindPopup(point.name)
);
clusterGroup.addLayers(markers);  // addLayers (plural) is much faster than individual addLayer
map.addLayer(clusterGroup);

// Update data
clusterGroup.clearLayers();
clusterGroup.addLayers(newMarkers);
```

### Custom Cluster CSS
```css
.marker-cluster {
  background-clip: padding-box;
  border-radius: 50%;
}
.cluster-small {
  background: rgba(181, 226, 140, 0.8);
  width: 30px; height: 30px;
  line-height: 30px;
  text-align: center;
  font-weight: bold;
}
.cluster-medium {
  background: rgba(241, 211, 87, 0.8);
  width: 40px; height: 40px;
  line-height: 40px;
  text-align: center;
  font-weight: bold;
}
.cluster-large {
  background: rgba(253, 156, 115, 0.8);
  width: 50px; height: 50px;
  line-height: 50px;
  text-align: center;
  font-weight: bold;
}
```

---

## GeoJSON & Vector Layers {#geojson}

### Loading GeoJSON
```javascript
const geoLayer = L.geoJSON(geojsonData, {
  style: (feature) => ({
    color: feature.properties.color || '#3388ff',
    weight: 2,
    opacity: 0.8,
    fillOpacity: 0.3
  }),

  pointToLayer: (feature, latlng) => {
    // Use circleMarkers instead of default markers for points
    return L.circleMarker(latlng, { radius: 6 });
  },

  onEachFeature: (feature, layer) => {
    layer.bindPopup(`
      <h3>${feature.properties.name}</h3>
      <p>${feature.properties.description || ''}</p>
    `);
    layer.on('click', (e) => handleFeatureClick(feature));
  },

  filter: (feature) => {
    return feature.properties.active !== false;
  }
}).addTo(map);

// Fit to GeoJSON bounds
map.fitBounds(geoLayer.getBounds());
```

### Polygons, Circles, Polylines
```javascript
// Polygon (geofence)
const polygon = L.polygon([
  [-25.260, -57.580],
  [-25.260, -57.570],
  [-25.270, -57.570],
  [-25.270, -57.580]
], {
  color: '#ff0000',
  fillColor: '#ff0000',
  fillOpacity: 0.2,
  weight: 2
}).addTo(map);

// Circle (geofence radius)
const circle = L.circle([-25.2637, -57.5759], {
  radius: 200,  // meters
  color: '#3388ff',
  fillOpacity: 0.1
}).addTo(map);

// Polyline (route)
const route = L.polyline(coordinates, {
  color: '#0066ff',
  weight: 4,
  opacity: 0.8,
  smoothFactor: 1
}).addTo(map);

// Animated route (using leaflet-ant-path)
// npm install leaflet-ant-path
import { antPath } from 'leaflet-ant-path';
const animatedRoute = antPath(coordinates, {
  color: '#0066ff',
  pulseColor: '#ffffff',
  delay: 800,
  dashArray: [10, 20]
}).addTo(map);
```

---

## Routing {#routing}

### Leaflet Routing Machine (LRM) + OSRM
```bash
npm install leaflet-routing-machine
```

```javascript
import 'leaflet-routing-machine';

const routeControl = L.Routing.control({
  waypoints: [
    L.latLng(-25.2637, -57.5759),
    L.latLng(-25.2867, -57.6174)
  ],
  routeWhileDragging: true,
  show: true,                    // Show turn-by-turn instructions
  addWaypoints: true,            // Allow adding waypoints by clicking
  fitSelectedRoutes: true,
  lineOptions: {
    styles: [{ color: '#0066ff', weight: 5, opacity: 0.7 }],
    extendToWaypoints: true,
    missingRouteTolerance: 0
  },
  // OSRM demo server (for development only, not production)
  router: L.Routing.osrmv1({
    serviceUrl: 'https://router.project-osrm.org/route/v1'
  })
}).addTo(map);

// Listen for route events
routeControl.on('routesfound', (e) => {
  const route = e.routes[0];
  console.log('Distance:', route.summary.totalDistance, 'meters');
  console.log('Time:', route.summary.totalTime, 'seconds');
});
```

### Direct OSRM API (without LRM)
```javascript
async function getRoute(waypoints) {
  const coords = waypoints.map(w => `${w.lng},${w.lat}`).join(';');
  const url = `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson&steps=true`;

  const res = await fetch(url);
  const data = await res.json();

  if (data.code === 'Ok') {
    const route = data.routes[0];
    L.geoJSON(route.geometry, {
      style: { color: '#0066ff', weight: 4 }
    }).addTo(map);

    return {
      distance: route.distance,  // meters
      duration: route.duration,  // seconds
      steps: route.legs[0].steps
    };
  }
}
```

---

## Drawing & Editing {#drawing}

### Leaflet.draw
```bash
npm install leaflet-draw
```

```javascript
import 'leaflet-draw';
import 'leaflet-draw/dist/leaflet.draw.css';

const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

const drawControl = new L.Control.Draw({
  edit: { featureGroup: drawnItems },
  draw: {
    polygon: true,
    polyline: true,
    rectangle: true,
    circle: true,
    circlemarker: false,
    marker: true
  }
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, (e) => {
  const layer = e.layer;
  drawnItems.addLayer(layer);
  const geojson = layer.toGeoJSON();
  console.log('Created:', geojson);
});

map.on(L.Draw.Event.EDITED, (e) => {
  e.layers.eachLayer((layer) => {
    console.log('Edited:', layer.toGeoJSON());
  });
});
```

---

## Events & Interaction {#events}

```javascript
// Map events
map.on('click', (e) => console.log('Clicked at:', e.latlng));
map.on('zoomend', () => console.log('Zoom:', map.getZoom()));
map.on('moveend', () => console.log('Center:', map.getCenter()));
map.on('moveend', () => loadMarkersInBounds(map.getBounds()));

// Get visible bounds for viewport loading
function loadMarkersInBounds(bounds) {
  const ne = bounds.getNorthEast();
  const sw = bounds.getSouthWest();
  fetch(`/api/markers?north=${ne.lat}&south=${sw.lat}&east=${ne.lng}&west=${sw.lng}`)
    .then(res => res.json())
    .then(data => updateMarkers(data));
}
```

---

## Key Plugins {#plugins}

| Plugin | Use Case |
|--------|----------|
| `leaflet.markercluster` | Marker clustering |
| `leaflet-routing-machine` | Routing with UI |
| `leaflet-draw` | Drawing/editing shapes |
| `leaflet-ant-path` | Animated polylines |
| `leaflet.heat` | Heatmaps |
| `leaflet-realtime` | Real-time GeoJSON updates |
| `leaflet-fullscreen` | Fullscreen toggle button |
| `leaflet.locatecontrol` | "Find my location" button |
| `leaflet-easybutton` | Quick custom controls |
| `leaflet-sidebar-v2` | Responsive sidebar |
| `leaflet.pm` | Modern alternative to leaflet-draw |

---

## Performance Tips {#performance}

1. **Use `Canvas` renderer** for 1000+ markers: `L.map('map', { preferCanvas: true })`
2. **Use `addLayers()`** (plural) on cluster groups — 10x faster than looping `addLayer()`
3. **`chunkedLoading: true`** on cluster groups prevents UI freeze during large loads
4. **Viewport loading**: Only fetch/render markers within `map.getBounds()`, reload on `moveend`
5. **Debounce** `moveend` handler: users pan quickly, don't fetch on every pixel
6. **Avoid heavy popups**: Lazy-load popup content on click, not on marker creation
7. **Remove layers** when switching views: `map.removeLayer(layer)` and null the reference
8. **Reuse icons**: Create icon instances once, share across markers — don't create new `L.icon()` per marker
