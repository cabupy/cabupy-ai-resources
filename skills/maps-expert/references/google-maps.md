# Google Maps JavaScript API Reference

## Table of Contents
1. [Setup & Initialization](#setup)
2. [Markers (Legacy & Advanced)](#markers)
3. [Marker Clustering](#clustering)
4. [Directions & Routes](#directions)
5. [Drawing & Shapes](#shapes)
6. [Places & Geocoding](#places)
7. [Info Windows & Overlays](#overlays)
8. [Heatmaps](#heatmaps)
9. [Street View](#streetview)
10. [Performance Tips](#performance)

---

## Setup {#setup}

### Script Loading (recommended: Dynamic Library Import)
```html
<script>
  (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",
  q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),
  r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await
  (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)
  e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);
  e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;
  d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));
  a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));
  d[l]?console.warn(p+" only loads once"):d[l]=(f,...n)=>r.add(f)&&u().then(()=>
  d[l](f,...n))})({
    key: "YOUR_API_KEY",
    v: "weekly"
  });
</script>
```

### Modern async/await initialization
```javascript
async function initMap() {
  const { Map } = await google.maps.importLibrary('maps');
  const { AdvancedMarkerElement } = await google.maps.importLibrary('marker');

  const map = new Map(document.getElementById('map'), {
    center: { lat: -25.2637, lng: -57.5759 },  // Asunción
    zoom: 13,
    mapId: 'YOUR_MAP_ID',  // Required for Advanced Markers and Cloud styling
    gestureHandling: 'cooperative',  // ctrl+scroll to zoom (embedded maps)
    zoomControl: true,
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: true
  });

  return map;
}
```

### Google Maps uses `{ lat, lng }` objects or `LatLng(lat, lng)` — lat first.

---

## Markers {#markers}

### Advanced Markers (recommended, requires mapId)
```javascript
const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary('marker');

// Default pin
const marker = new AdvancedMarkerElement({
  map,
  position: { lat: -25.2637, lng: -57.5759 },
  title: 'Asunción'
});

// Custom pin colors
const pin = new PinElement({
  background: '#ff0000',
  borderColor: '#cc0000',
  glyphColor: '#ffffff',
  glyph: '42',     // Text inside pin
  scale: 1.2
});
const colorMarker = new AdvancedMarkerElement({
  map,
  position: { lat: -25.27, lng: -57.58 },
  content: pin.element
});

// Fully custom HTML marker
const content = document.createElement('div');
content.innerHTML = `
  <div class="custom-marker" style="
    background: white; border-radius: 8px; padding: 4px 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3); font-weight: bold;
  ">
    $15,000
  </div>
`;
const htmlMarker = new AdvancedMarkerElement({
  map,
  position: { lat: -25.28, lng: -57.57 },
  content
});

// Click events
marker.addEventListener('gmp-click', () => {
  console.log('Marker clicked');
});
```

### Legacy Markers (no mapId needed)
```javascript
const marker = new google.maps.Marker({
  position: { lat: -25.2637, lng: -57.5759 },
  map,
  title: 'Point',
  icon: {
    url: 'custom-icon.png',
    scaledSize: new google.maps.Size(32, 32),
    anchor: new google.maps.Point(16, 32)
  },
  animation: google.maps.Animation.DROP
});
```

---

## Marker Clustering {#clustering}

### @googlemaps/markerclusterer
```bash
npm install @googlemaps/markerclusterer
```

```javascript
import { MarkerClusterer, SuperClusterAlgorithm } from '@googlemaps/markerclusterer';

// With Advanced Markers
const markers = locations.map(loc => {
  return new AdvancedMarkerElement({
    position: { lat: loc.lat, lng: loc.lng },
    // Don't set map here — the clusterer manages it
  });
});

const clusterer = new MarkerClusterer({
  map,
  markers,
  algorithm: new SuperClusterAlgorithm({ radius: 80, maxZoom: 16 }),

  // Custom cluster renderer
  renderer: {
    render: ({ count, position }) => {
      const color = count > 100 ? '#ff0000' : count > 10 ? '#ff9900' : '#00cc00';
      const size = Math.min(20 + Math.sqrt(count) * 5, 60);

      const svg = `
        <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
          <circle cx="${size/2}" cy="${size/2}" r="${size/2}" fill="${color}" opacity="0.8"/>
          <text x="50%" y="50%" dominant-baseline="central" text-anchor="middle"
                fill="white" font-size="12" font-weight="bold">${count}</text>
        </svg>
      `;

      const el = document.createElement('div');
      el.innerHTML = svg;

      return new AdvancedMarkerElement({
        position,
        content: el,
        zIndex: count
      });
    }
  }
});

// Update markers
clusterer.clearMarkers();
clusterer.addMarkers(newMarkers);
```

---

## Directions & Routes {#directions}

### DirectionsService + DirectionsRenderer
```javascript
const { DirectionsService, DirectionsRenderer } = await google.maps.importLibrary('routes');

const directionsService = new DirectionsService();
const directionsRenderer = new DirectionsRenderer({
  map,
  suppressMarkers: false,
  polylineOptions: {
    strokeColor: '#0066ff',
    strokeWeight: 5,
    strokeOpacity: 0.7
  }
});

async function calcRoute(origin, destination, waypoints = []) {
  const result = await directionsService.route({
    origin,         // { lat, lng } or address string
    destination,
    waypoints: waypoints.map(w => ({ location: w, stopover: true })),
    optimizeWaypoints: true,  // Reorder waypoints for shortest route
    travelMode: google.maps.TravelMode.DRIVING,
    unitSystem: google.maps.UnitSystem.METRIC
  });

  directionsRenderer.setDirections(result);

  const route = result.routes[0];
  const leg = route.legs[0];
  console.log('Distance:', leg.distance.text);
  console.log('Duration:', leg.duration.text);

  return result;
}
```

### Route Polyline (manual, no renderer)
```javascript
const path = google.maps.geometry.encoding.decodePath(encodedPolyline);
const routeLine = new google.maps.Polyline({
  path,
  geodesic: true,
  strokeColor: '#0066ff',
  strokeOpacity: 0.8,
  strokeWeight: 4
});
routeLine.setMap(map);
```

---

## Drawing & Shapes {#shapes}

```javascript
// Polygon (geofence)
const polygon = new google.maps.Polygon({
  paths: [
    { lat: -25.260, lng: -57.580 },
    { lat: -25.260, lng: -57.570 },
    { lat: -25.270, lng: -57.570 },
    { lat: -25.270, lng: -57.580 }
  ],
  strokeColor: '#ff0000',
  strokeWeight: 2,
  fillColor: '#ff0000',
  fillOpacity: 0.15,
  editable: false,
  draggable: false
});
polygon.setMap(map);

// Circle (radius geofence)
const circle = new google.maps.Circle({
  center: { lat: -25.2637, lng: -57.5759 },
  radius: 200,  // meters
  strokeColor: '#3388ff',
  fillColor: '#3388ff',
  fillOpacity: 0.1
});
circle.setMap(map);

// Point in polygon check
function isInsidePolygon(point, polygon) {
  return google.maps.geometry.poly.containsLocation(
    new google.maps.LatLng(point.lat, point.lng),
    polygon
  );
}

// Drawing Manager
const { DrawingManager } = await google.maps.importLibrary('drawing');
const drawingManager = new DrawingManager({
  drawingMode: null,
  drawingControl: true,
  drawingControlOptions: {
    position: google.maps.ControlPosition.TOP_CENTER,
    drawingModes: ['marker', 'circle', 'polygon', 'polyline', 'rectangle']
  }
});
drawingManager.setMap(map);

google.maps.event.addListener(drawingManager, 'overlaycomplete', (event) => {
  console.log('Type:', event.type);
  console.log('Overlay:', event.overlay);
});
```

---

## Places & Geocoding {#places}

### Geocoding
```javascript
const { Geocoder } = await google.maps.importLibrary('geocoding');
const geocoder = new Geocoder();

// Address → coordinates
const result = await geocoder.geocode({ address: 'Palma 500, Asunción, Paraguay' });
const location = result.results[0].geometry.location;
console.log(location.lat(), location.lng());

// Coordinates → address (reverse)
const result = await geocoder.geocode({ location: { lat: -25.2637, lng: -57.5759 } });
console.log(result.results[0].formatted_address);
```

### Places Autocomplete
```javascript
const { Autocomplete } = await google.maps.importLibrary('places');

const autocomplete = new Autocomplete(document.getElementById('search-input'), {
  types: ['establishment'],
  componentRestrictions: { country: 'py' },
  fields: ['place_id', 'geometry', 'name', 'formatted_address']
});

autocomplete.addListener('place_changed', () => {
  const place = autocomplete.getPlace();
  if (place.geometry) {
    map.panTo(place.geometry.location);
    map.setZoom(17);
  }
});
```

---

## Info Windows {#overlays}

```javascript
const infoWindow = new google.maps.InfoWindow({
  content: '<h3>Title</h3><p>Description</p>',
  maxWidth: 300
});

// Open on marker click (single shared InfoWindow = only one open at a time)
marker.addEventListener('gmp-click', () => {
  infoWindow.close();
  infoWindow.setContent(`<h3>${marker.title}</h3>`);
  infoWindow.open({ anchor: marker, map });
});
```

---

## Heatmaps {#heatmaps}

```javascript
const { HeatmapLayer } = await google.maps.importLibrary('visualization');

const heatmap = new HeatmapLayer({
  data: points.map(p => ({
    location: new google.maps.LatLng(p.lat, p.lng),
    weight: p.intensity || 1
  })),
  radius: 30,
  opacity: 0.7,
  gradient: [
    'rgba(0, 255, 255, 0)', 'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)', 'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',  'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',   'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 127, 1)',   'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',  'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
});
heatmap.setMap(map);
```

---

## Performance Tips {#performance}

1. **Use Advanced Markers** — they're significantly faster than legacy markers
2. **Single shared InfoWindow** — open/close the same instance instead of creating per marker
3. **`gestureHandling: 'cooperative'`** — prevents accidental zoom on scroll, essential for embedded
4. **Limit Places fields** — always specify `fields` in Autocomplete/PlaceDetails to reduce cost
5. **Debounce `bounds_changed`** — fires rapidly during pan/zoom
6. **`google.maps.event.trigger(map, 'resize')`** — call after container size changes
7. **Use MarkerClusterer** with SuperClusterAlgorithm for 500+ markers
8. **Map IDs + Cloud Styling** — style the map server-side, avoids runtime re-rendering
9. **Lazy-load libraries** — `importLibrary()` loads only what you need
