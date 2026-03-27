# Clustering & Performance

## Table of Contents
1. [Performance Tiers](#tiers)
2. [Client-Side Clustering Libraries](#client-clustering)
3. [Supercluster (Universal)](#supercluster)
4. [Web Workers for Clustering](#workers)
5. [Viewport Loading (Load on Demand)](#viewport)
6. [Canvas & WebGL Rendering](#canvas)
7. [Server-Side Clustering](#server)
8. [Heatmaps vs Clusters](#heatmaps)
9. [Benchmarking & Profiling](#profiling)
10. [Memory Management](#memory)

---

## Performance Tiers {#tiers}

| Feature Count | Strategy | Expected FPS |
|---------------|----------|--------------|
| < 200 | DOM markers (default) | 60 |
| 200 – 1,000 | CircleMarkers (Canvas) or clustering | 60 |
| 1,000 – 5,000 | Marker clustering + Canvas renderer | 50-60 |
| 5,000 – 20,000 | Supercluster + Web Worker + Canvas/WebGL | 50-60 |
| 20,000 – 100,000 | Viewport-only loading + server pagination + Supercluster | 40-60 |
| 100,000+ | Server-side clustering + vector tiles + viewport queries | 60 |

The key insight: DOM markers (regular HTML/SVG elements) are expensive because each one participates in browser layout. Canvas/WebGL markers bypass DOM entirely.

---

## Client-Side Clustering Libraries {#client-clustering}

### Leaflet.markercluster
Best for: Leaflet projects with < 10,000 markers

```javascript
import 'leaflet.markercluster';

const cluster = L.markerClusterGroup({
  chunkedLoading: true,           // Non-blocking loading
  chunkInterval: 200,             // ms between chunks
  chunkDelay: 50,                 // ms delay per chunk
  chunkProgress: (processed, total) => {
    console.log(`Loading: ${Math.round(processed/total*100)}%`);
  },
  maxClusterRadius: 80,           // Cluster radius in pixels
  disableClusteringAtZoom: 18,    // Show individual markers at this zoom
  spiderfyOnMaxZoom: true,
  animateAddingMarkers: false,    // Disable for better performance with large sets
  removeOutsideVisibleBounds: true // Only render visible clusters
});

// IMPORTANT: Use addLayers (plural) — 10x faster than individual addLayer
const markers = data.map(d => L.marker([d.lat, d.lng]));
cluster.addLayers(markers);
map.addLayer(cluster);
```

### @googlemaps/markerclusterer
Best for: Google Maps projects

```javascript
import { MarkerClusterer, SuperClusterAlgorithm, GridAlgorithm } from '@googlemaps/markerclusterer';

// SuperClusterAlgorithm (recommended — uses supercluster internally)
const clusterer = new MarkerClusterer({
  map,
  markers,
  algorithm: new SuperClusterAlgorithm({
    radius: 80,
    maxZoom: 16,
    minPoints: 3
  })
});

// GridAlgorithm (simpler, faster for uniform distributions)
const clusterer = new MarkerClusterer({
  map,
  markers,
  algorithm: new GridAlgorithm({ gridSize: 60 })
});
```

### Mapbox Native Clustering
Best for: Mapbox GL projects (zero plugins, GPU-rendered)

```javascript
map.addSource('points', {
  type: 'geojson',
  data: geojson,
  cluster: true,
  clusterMaxZoom: 14,
  clusterRadius: 50,
  clusterMinPoints: 3,
  clusterProperties: {
    'total_value': ['+', ['get', 'value']],
    'has_alert': ['any', ['get', 'alert']]
  }
});
```

Mapbox clustering is the fastest option because it runs in a Web Worker automatically and renders via WebGL. Choose Mapbox if performance is the primary concern.

---

## Supercluster (Universal) {#supercluster}

Supercluster works with ANY map library. It's the fastest JS clustering algorithm.

```bash
npm install supercluster
```

```javascript
import Supercluster from 'supercluster';

// Create index
const index = new Supercluster({
  radius: 60,         // Cluster radius in pixels
  maxZoom: 16,         // Max zoom to cluster at
  minZoom: 0,
  minPoints: 2,        // Min points to form a cluster
  extent: 256,         // Tile extent
  nodeSize: 64,        // Internal KD-tree node size (higher = faster build, slower query)

  // Aggregate properties across clusters
  map: (props) => ({ sum: props.value }),
  reduce: (accumulated, props) => { accumulated.sum += props.sum; }
});

// Load data (GeoJSON features with [lng, lat] coordinates)
index.load(geojsonFeatures);

// Get clusters for current viewport
function getClusters(map) {
  const bounds = map.getBounds();
  const zoom = Math.floor(map.getZoom());

  const clusters = index.getClusters(
    [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()],
    zoom
  );

  return clusters;
  // Returns GeoJSON features where:
  //   cluster === true → it's a cluster (has point_count, cluster_id)
  //   cluster === undefined → it's an individual point
}

// Get zoom level to expand a cluster
const expansionZoom = index.getClusterExpansionZoom(clusterId);

// Get children of a cluster
const children = index.getChildren(clusterId);

// Get all leaves (original points) of a cluster
const leaves = index.getLeaves(clusterId, Infinity);  // Infinity = all leaves
```

### Supercluster + Leaflet
```javascript
const index = new Supercluster({ radius: 60, maxZoom: 16 });
index.load(geojsonPoints);

const markersLayer = L.geoJSON(null, {
  pointToLayer: (feature, latlng) => {
    if (feature.properties.cluster) {
      const count = feature.properties.point_count;
      const size = count < 10 ? 30 : count < 100 ? 40 : 50;

      return L.marker(latlng, {
        icon: L.divIcon({
          html: `<div class="cluster" style="width:${size}px;height:${size}px;line-height:${size}px">${count}</div>`,
          className: '',
          iconSize: [size, size]
        })
      }).on('click', () => {
        const zoom = index.getClusterExpansionZoom(feature.properties.cluster_id);
        map.setView(latlng, zoom);
      });
    }

    return L.circleMarker(latlng, { radius: 6, fillColor: '#3388ff', fillOpacity: 0.8 });
  }
});

function updateClusters() {
  const bounds = map.getBounds();
  const zoom = Math.floor(map.getZoom());
  const clusters = index.getClusters(
    [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()],
    zoom
  );
  markersLayer.clearLayers();
  markersLayer.addData({ type: 'FeatureCollection', features: clusters });
}

map.on('moveend', updateClusters);
markersLayer.addTo(map);
updateClusters();
```

---

## Web Workers for Clustering {#workers}

For datasets > 10,000 points, move Supercluster to a Web Worker to avoid blocking the UI:

### worker.js
```javascript
import Supercluster from 'supercluster';

let index;

self.onmessage = (e) => {
  const { type, data } = e.data;

  switch (type) {
    case 'load':
      index = new Supercluster({
        radius: data.options.radius || 60,
        maxZoom: data.options.maxZoom || 16,
        map: (props) => ({ sum: props.value || 0 }),
        reduce: (acc, props) => { acc.sum += props.sum; }
      });
      index.load(data.features);
      self.postMessage({ type: 'loaded', count: data.features.length });
      break;

    case 'getClusters':
      const clusters = index.getClusters(data.bbox, data.zoom);
      self.postMessage({ type: 'clusters', clusters });
      break;

    case 'getExpansionZoom':
      const zoom = index.getClusterExpansionZoom(data.clusterId);
      self.postMessage({ type: 'expansionZoom', zoom, clusterId: data.clusterId });
      break;
  }
};
```

### Main thread
```javascript
const worker = new Worker(new URL('./cluster.worker.js', import.meta.url), { type: 'module' });

// Load data
worker.postMessage({
  type: 'load',
  data: { features: geojsonFeatures, options: { radius: 60, maxZoom: 16 } }
});

// Request clusters for current view
function requestClusters() {
  const bounds = map.getBounds();
  worker.postMessage({
    type: 'getClusters',
    data: {
      bbox: [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()],
      zoom: Math.floor(map.getZoom())
    }
  });
}

// Receive clusters
worker.onmessage = (e) => {
  if (e.data.type === 'clusters') {
    renderClusters(e.data.clusters);
  }
};

map.on('moveend', debounce(requestClusters, 200));
```

---

## Viewport Loading {#viewport}

Only load data visible in the current viewport. Essential for 20,000+ points.

### API Pattern
```javascript
// Backend endpoint
// GET /api/markers?north=-25.20&south=-25.35&east=-57.50&west=-57.65&zoom=13

async function loadVisibleMarkers() {
  const bounds = map.getBounds();
  const zoom = Math.floor(map.getZoom());

  const params = new URLSearchParams({
    north: bounds.getNorth(),
    south: bounds.getSouth(),
    east: bounds.getEast(),
    west: bounds.getWest(),
    zoom: zoom
  });

  const res = await fetch(`/api/markers?${params}`);
  const data = await res.json();
  updateMapMarkers(data.features);
}

// Debounce to avoid flooding the API during pan/zoom
const debouncedLoad = debounce(loadVisibleMarkers, 300);
map.on('moveend', debouncedLoad);
```

### With Caching (avoid re-fetching known areas)
```javascript
class ViewportLoader {
  constructor(map, fetchFn) {
    this.map = map;
    this.fetchFn = fetchFn;
    this.cache = new Map();  // tile-key → features
    this.tileSize = 0.01;    // ~1km grid cells
  }

  getTileKey(lat, lng) {
    const tLat = Math.floor(lat / this.tileSize) * this.tileSize;
    const tLng = Math.floor(lng / this.tileSize) * this.tileSize;
    return `${tLat.toFixed(4)},${tLng.toFixed(4)}`;
  }

  async loadViewport() {
    const bounds = this.map.getBounds();
    const neededTiles = this.getTilesInBounds(bounds);
    const missing = neededTiles.filter(t => !this.cache.has(t));

    if (missing.length === 0) return;

    const data = await this.fetchFn(bounds);
    // Cache by tile
    data.forEach(feature => {
      const key = this.getTileKey(feature.lat, feature.lng);
      if (!this.cache.has(key)) this.cache.set(key, []);
      this.cache.get(key).push(feature);
    });
  }
}
```

---

## Canvas & WebGL Rendering {#canvas}

### Leaflet Canvas Renderer
```javascript
// Enable globally
const map = L.map('map', { preferCanvas: true });

// Or per-layer
const circleMarkers = L.layerGroup();
data.forEach(d => {
  L.circleMarker([d.lat, d.lng], {
    renderer: L.canvas(),  // Explicit canvas renderer
    radius: 5,
    fillColor: d.color,
    fillOpacity: 0.8,
    weight: 1
  }).addTo(circleMarkers);
});
circleMarkers.addTo(map);
```

### Leaflet.glify (WebGL points)
For 100,000+ points:
```bash
npm install leaflet.glify
```

```javascript
import * as L from 'leaflet';
import 'leaflet.glify';

L.glify.points({
  map,
  data: geojsonFeatureCollection,
  size: 8,
  color: (index, feature) => {
    return { r: 0.2, g: 0.6, b: 1 };  // RGB 0-1
  },
  click: (e, feature) => {
    L.popup()
      .setLatLng(e.latlng)
      .setContent(feature.properties.name)
      .openOn(map);
  }
});
```

### deck.gl (Framework-agnostic WebGL)
For the most demanding visualizations:
```bash
npm install deck.gl
```

```javascript
import { Deck } from '@deck.gl/core';
import { ScatterplotLayer, HeatmapLayer, TripsLayer } from 'deck.gl';

// With Mapbox
import { MapboxOverlay } from '@deck.gl/mapbox';

const overlay = new MapboxOverlay({
  layers: [
    new ScatterplotLayer({
      id: 'scatter',
      data: points,
      getPosition: d => [d.lng, d.lat],
      getRadius: 50,
      getFillColor: [0, 128, 255],
      radiusMinPixels: 2,
      pickable: true,
      onClick: info => console.log(info.object)
    })
  ]
});

map.addControl(overlay);
```

---

## Server-Side Clustering {#server}

For truly massive datasets (100K+), cluster on the server and send pre-clustered GeoJSON.

### PostGIS Clustering
```sql
-- Grid-based clustering
SELECT
  ST_AsGeoJSON(ST_Centroid(ST_Collect(geom))) as center,
  COUNT(*) as point_count,
  SUM(value) as total_value,
  ST_AsGeoJSON(ST_Envelope(ST_Collect(geom))) as bounds
FROM locations
WHERE geom && ST_MakeEnvelope($west, $south, $east, $north, 4326)
GROUP BY
  ST_SnapToGrid(geom, $grid_size)  -- grid_size depends on zoom level
HAVING COUNT(*) >= 1;
```

### Zoom-to-Grid-Size Mapping
```javascript
function getGridSize(zoom) {
  // Approximate grid sizes in degrees
  const gridSizes = {
    0: 45, 1: 22.5, 2: 11.25, 3: 5.6, 4: 2.8,
    5: 1.4, 6: 0.7, 7: 0.35, 8: 0.18, 9: 0.09,
    10: 0.045, 11: 0.022, 12: 0.011, 13: 0.005,
    14: 0.003, 15: 0.001, 16: 0.0005, 17: 0.0003, 18: 0
  };
  return gridSizes[zoom] || 0;  // 0 = no clustering
}
```

### Node.js API Endpoint
```javascript
app.get('/api/clusters', async (req, res) => {
  const { north, south, east, west, zoom } = req.query;
  const gridSize = getGridSize(parseInt(zoom));

  if (gridSize === 0) {
    // Return individual points
    const points = await db.query(
      `SELECT id, ST_Y(geom) as lat, ST_X(geom) as lng, name, value
       FROM locations
       WHERE geom && ST_MakeEnvelope($1, $2, $3, $4, 4326)
       LIMIT 5000`,
      [west, south, east, north]
    );
    return res.json(toGeoJSON(points.rows));
  }

  // Return clusters
  const clusters = await db.query(
    `SELECT
       ST_Y(ST_Centroid(ST_Collect(geom))) as lat,
       ST_X(ST_Centroid(ST_Collect(geom))) as lng,
       COUNT(*) as point_count,
       SUM(value) as total_value
     FROM locations
     WHERE geom && ST_MakeEnvelope($1, $2, $3, $4, 4326)
     GROUP BY ST_SnapToGrid(geom, $5)`,
    [west, south, east, north, gridSize]
  );

  return res.json(toClusterGeoJSON(clusters.rows));
});
```

---

## Heatmaps vs Clusters {#heatmaps}

Use **heatmaps** when:
- Showing density patterns (where are the hotspots?)
- Individual points don't matter
- Dataset is large and uniform

Use **clusters** when:
- Users need to drill down to individual items
- Each point has meaningful metadata
- Interactive selection/filtering is needed

You can combine both: show heatmap at low zoom, switch to clusters at higher zoom.

```javascript
// Mapbox: zoom-dependent visibility
map.addLayer({
  id: 'heat',
  type: 'heatmap',
  source: 'points',
  maxzoom: 12,  // Hide heatmap above zoom 12
  paint: { /* ... */ }
});

map.addLayer({
  id: 'clusters',
  type: 'circle',
  source: 'points',
  minzoom: 12,  // Show clusters from zoom 12
  paint: { /* ... */ }
});
```

---

## Benchmarking & Profiling {#profiling}

```javascript
// Measure render time
console.time('render-markers');
clusterGroup.addLayers(markers);
console.timeEnd('render-markers');

// Monitor frame rate
let frames = 0;
let lastTime = performance.now();
function checkFPS() {
  frames++;
  const now = performance.now();
  if (now - lastTime >= 1000) {
    console.log(`FPS: ${frames}`);
    frames = 0;
    lastTime = now;
  }
  requestAnimationFrame(checkFPS);
}
checkFPS();

// Memory usage
console.log('Memory:', performance.memory?.usedJSHeapSize / 1024 / 1024, 'MB');
```

---

## Memory Management {#memory}

```javascript
// Always clean up on component destroy
function destroyMap() {
  // Remove all event listeners
  map.off();

  // Remove all layers
  map.eachLayer(layer => map.removeLayer(layer));

  // Remove the map instance
  map.remove();

  // Disconnect observers
  resizeObserver?.disconnect();

  // Terminate web workers
  clusterWorker?.terminate();

  // Null references
  map = null;
}

// For SPAs: watch for route changes
// Angular: ngOnDestroy
// React: useEffect cleanup
// Vue: onUnmounted
```
