# Framework Integration Patterns

## Table of Contents
1. [Angular](#angular)
2. [React](#react)
3. [Vue](#vue)
4. [Ionic/Capacitor Specifics](#ionic)
5. [Common Patterns](#common)

---

## Angular {#angular}

### Leaflet + Angular

```bash
npm install leaflet
npm install -D @types/leaflet
```

Add to `angular.json` styles:
```json
"styles": [
  "node_modules/leaflet/dist/leaflet.css"
]
```

```typescript
// map.component.ts
import { Component, OnInit, OnDestroy, AfterViewInit, ElementRef, ViewChild, NgZone, Input } from '@angular/core';
import * as L from 'leaflet';

@Component({
  selector: 'app-map',
  standalone: true,
  template: `<div #mapContainer class="map-container"></div>`,
  styles: [`
    :host { display: block; width: 100%; height: 100%; }
    .map-container { width: 100%; height: 100%; }
  `]
})
export class MapComponent implements AfterViewInit, OnDestroy {
  @ViewChild('mapContainer') mapContainer!: ElementRef;
  @Input() center: L.LatLngExpression = [-25.2637, -57.5759];
  @Input() zoom = 13;

  private map!: L.Map;
  private resizeObserver!: ResizeObserver;

  constructor(private ngZone: NgZone) {}

  ngAfterViewInit(): void {
    // Initialize outside Angular zone to prevent change detection on every map event
    this.ngZone.runOutsideAngular(() => {
      this.initMap();
    });
  }

  private initMap(): void {
    this.map = L.map(this.mapContainer.nativeElement, {
      center: this.center,
      zoom: this.zoom,
      zoomControl: true
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.map);

    // Fix Leaflet icon paths (Angular CLI breaks default paths)
    this.fixIconPaths();

    // ResizeObserver for container changes
    this.resizeObserver = new ResizeObserver(() => {
      this.map.invalidateSize();
    });
    this.resizeObserver.observe(this.mapContainer.nativeElement);
  }

  private fixIconPaths(): void {
    const iconRetinaUrl = 'assets/leaflet/marker-icon-2x.png';
    const iconUrl = 'assets/leaflet/marker-icon.png';
    const shadowUrl = 'assets/leaflet/marker-shadow.png';

    L.Marker.prototype.options.icon = L.icon({
      iconRetinaUrl, iconUrl, shadowUrl,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
  }

  // Public API for parent components
  addMarker(lat: number, lng: number, popup?: string): L.Marker {
    const marker = L.marker([lat, lng]).addTo(this.map);
    if (popup) marker.bindPopup(popup);
    return marker;
  }

  fitBounds(bounds: L.LatLngBoundsExpression): void {
    this.map.fitBounds(bounds);
  }

  getMap(): L.Map {
    return this.map;
  }

  ngOnDestroy(): void {
    this.resizeObserver?.disconnect();
    this.map?.remove();
  }
}
```

### Critical Angular + Leaflet Notes

1. **Zone.js**: Initialize map in `runOutsideAngular()` — Leaflet fires hundreds of events during pan/zoom that trigger unnecessary change detection.

2. **Icon paths**: Angular CLI's build system breaks Leaflet's default icon URL resolution. Either:
   - Copy marker icons to `src/assets/leaflet/` and set paths manually (shown above)
   - Or use `leaflet-defaulticon-compatibility` package

3. **Lifecycle**: Use `AfterViewInit`, not `OnInit` — the DOM element must exist.

4. **CSS encapsulation**: Leaflet popup styles won't penetrate Angular's ViewEncapsulation. Use:
   ```typescript
   // Option A: ViewEncapsulation.None on the component
   encapsulation: ViewEncapsulation.None

   // Option B: ::ng-deep (deprecated but works)
   ::ng-deep .leaflet-popup-content { ... }

   // Option C (recommended): Global styles in styles.css
   ```

5. **Memory leaks**: Always `map.remove()` in `ngOnDestroy`.

### Google Maps + Angular (@angular/google-maps)

```bash
npm install @angular/google-maps
```

```typescript
// app.config.ts or module
import { provideGoogleMaps } from '@angular/google-maps';

export const appConfig = {
  providers: [
    provideGoogleMaps({ apiKey: 'YOUR_API_KEY' })
  ]
};
```

```typescript
// map.component.ts
import { Component, ViewChild } from '@angular/core';
import { GoogleMap, MapMarker, MapMarkerClusterer, MapInfoWindow } from '@angular/google-maps';

@Component({
  selector: 'app-google-map',
  standalone: true,
  imports: [GoogleMap, MapMarker, MapMarkerClusterer, MapInfoWindow],
  template: `
    <google-map
      [center]="center"
      [zoom]="zoom"
      [options]="mapOptions"
      width="100%"
      height="100%"
      (mapClick)="onMapClick($event)"
    >
      <map-marker-clusterer [imagePath]="clusterImagePath">
        @for (point of points; track point.id) {
          <map-marker
            [position]="point.position"
            [title]="point.title"
            (mapClick)="openInfoWindow(marker, point)"
            #marker="mapMarker"
          />
        }
      </map-marker-clusterer>

      <map-info-window>
        <div>{{ selectedPoint?.title }}</div>
      </map-info-window>
    </google-map>
  `,
  styles: [`:host { display: block; width: 100%; height: 100%; }`]
})
export class GoogleMapComponent {
  @ViewChild(MapInfoWindow) infoWindow!: MapInfoWindow;

  center = { lat: -25.2637, lng: -57.5759 };
  zoom = 13;
  selectedPoint: any = null;

  mapOptions: google.maps.MapOptions = {
    gestureHandling: 'cooperative',
    mapId: 'YOUR_MAP_ID'
  };

  points = [
    { id: 1, position: { lat: -25.26, lng: -57.57 }, title: 'Point A' },
    { id: 2, position: { lat: -25.27, lng: -57.58 }, title: 'Point B' }
  ];

  openInfoWindow(markerRef: MapMarker, point: any) {
    this.selectedPoint = point;
    this.infoWindow.open(markerRef);
  }

  onMapClick(event: google.maps.MapMouseEvent) {
    console.log('Clicked:', event.latLng?.toJSON());
  }
}
```

### Mapbox GL + Angular

```bash
npm install mapbox-gl
npm install -D @types/mapbox-gl
```

Add to `angular.json` styles:
```json
"styles": [
  "node_modules/mapbox-gl/dist/mapbox-gl.css"
]
```

```typescript
import { Component, AfterViewInit, OnDestroy, ElementRef, ViewChild, NgZone } from '@angular/core';
import mapboxgl from 'mapbox-gl';

@Component({
  selector: 'app-mapbox',
  standalone: true,
  template: `<div #mapContainer class="map-container"></div>`,
  styles: [`:host { display: block; width: 100%; height: 100%; }
            .map-container { width: 100%; height: 100%; }`]
})
export class MapboxComponent implements AfterViewInit, OnDestroy {
  @ViewChild('mapContainer') mapContainer!: ElementRef;
  private map!: mapboxgl.Map;
  private resizeObserver!: ResizeObserver;

  constructor(private ngZone: NgZone) {}

  ngAfterViewInit(): void {
    this.ngZone.runOutsideAngular(() => {
      mapboxgl.accessToken = 'YOUR_TOKEN';
      this.map = new mapboxgl.Map({
        container: this.mapContainer.nativeElement,
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [-57.5759, -25.2637],  // [lng, lat]
        zoom: 12
      });

      this.map.addControl(new mapboxgl.NavigationControl());

      this.resizeObserver = new ResizeObserver(() => this.map.resize());
      this.resizeObserver.observe(this.mapContainer.nativeElement);
    });
  }

  ngOnDestroy(): void {
    this.resizeObserver?.disconnect();
    this.map?.remove();
  }
}
```

---

## React {#react}

### react-leaflet
```bash
npm install react-leaflet leaflet
npm install -D @types/leaflet
```

```tsx
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix icon paths in bundlers (Vite, webpack)
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';
L.Icon.Default.mergeOptions({ iconUrl, iconRetinaUrl, shadowUrl });

// Resize handler component
function ResizeHandler() {
  const map = useMap();
  useEffect(() => {
    const observer = new ResizeObserver(() => map.invalidateSize());
    observer.observe(map.getContainer());
    return () => observer.disconnect();
  }, [map]);
  return null;
}

// Fit bounds component
function FitBounds({ bounds }: { bounds: L.LatLngBoundsExpression }) {
  const map = useMap();
  useEffect(() => {
    map.fitBounds(bounds, { padding: [20, 20] });
  }, [map, bounds]);
  return null;
}

function MapView({ points }: { points: Array<{ lat: number; lng: number; name: string }> }) {
  return (
    <MapContainer
      center={[-25.2637, -57.5759]}
      zoom={13}
      style={{ width: '100%', height: '100%' }}
      scrollWheelZoom={true}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
        maxZoom={19}
      />
      <ResizeHandler />

      {points.map((point, i) => (
        <Marker key={i} position={[point.lat, point.lng]}>
          <Popup>{point.name}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
```

### react-map-gl (Mapbox)
```bash
npm install react-map-gl mapbox-gl
```

```tsx
import Map, { Marker, Popup, Source, Layer, NavigationControl } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

function MapView({ points }) {
  const [viewState, setViewState] = useState({
    longitude: -57.5759,
    latitude: -25.2637,
    zoom: 12
  });
  const [selectedPoint, setSelectedPoint] = useState(null);

  // Clustering layer config
  const clusterLayer = {
    id: 'clusters',
    type: 'circle',
    source: 'points',
    filter: ['has', 'point_count'],
    paint: {
      'circle-color': ['step', ['get', 'point_count'], '#51bbd6', 10, '#f1f075', 50, '#f28cb1'],
      'circle-radius': ['step', ['get', 'point_count'], 20, 10, 30, 50, 40]
    }
  };

  const geojson = useMemo(() => ({
    type: 'FeatureCollection',
    features: points.map(p => ({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [p.lng, p.lat] },
      properties: { name: p.name }
    }))
  }), [points]);

  return (
    <Map
      {...viewState}
      onMove={evt => setViewState(evt.viewState)}
      mapboxAccessToken="YOUR_TOKEN"
      mapStyle="mapbox://styles/mapbox/streets-v12"
      style={{ width: '100%', height: '100%' }}
      cooperativeGestures={true}
    >
      <NavigationControl position="top-right" />

      <Source id="points" type="geojson" data={geojson} cluster clusterMaxZoom={14} clusterRadius={50}>
        <Layer {...clusterLayer} />
      </Source>
    </Map>
  );
}
```

### @vis.gl/react-google-maps
```bash
npm install @vis.gl/react-google-maps
```

```tsx
import { APIProvider, Map, AdvancedMarker, InfoWindow } from '@vis.gl/react-google-maps';

function GoogleMapView({ points }) {
  const [selected, setSelected] = useState(null);

  return (
    <APIProvider apiKey="YOUR_KEY">
      <Map
        defaultCenter={{ lat: -25.2637, lng: -57.5759 }}
        defaultZoom={13}
        mapId="YOUR_MAP_ID"
        style={{ width: '100%', height: '100%' }}
        gestureHandling="cooperative"
      >
        {points.map(point => (
          <AdvancedMarker
            key={point.id}
            position={{ lat: point.lat, lng: point.lng }}
            onClick={() => setSelected(point)}
          />
        ))}

        {selected && (
          <InfoWindow
            position={{ lat: selected.lat, lng: selected.lng }}
            onCloseClick={() => setSelected(null)}
          >
            <h3>{selected.name}</h3>
          </InfoWindow>
        )}
      </Map>
    </APIProvider>
  );
}
```

---

## Vue {#vue}

### vue-leaflet (Vue 3)
```bash
npm install @vue-leaflet/vue-leaflet leaflet
```

```vue
<template>
  <l-map
    ref="map"
    :zoom="13"
    :center="[-25.2637, -57.5759]"
    style="height: 100%; width: 100%"
    @ready="onMapReady"
  >
    <l-tile-layer
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      attribution="© OpenStreetMap contributors"
    />

    <l-marker
      v-for="point in points"
      :key="point.id"
      :lat-lng="[point.lat, point.lng]"
    >
      <l-popup>{{ point.name }}</l-popup>
    </l-marker>
  </l-map>
</template>

<script setup>
import { ref } from 'vue';
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet';
import 'leaflet/dist/leaflet.css';

const map = ref(null);
const points = ref([
  { id: 1, lat: -25.26, lng: -57.57, name: 'Point A' }
]);

function onMapReady(mapInstance) {
  // Access raw Leaflet map
  const leafletMap = mapInstance;
}
</script>
```

---

## Ionic / Capacitor Specifics {#ionic}

### Critical Issues

1. **Content security**: Add tile domains to CSP in `index.html`:
```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'self' 'unsafe-inline' 'unsafe-eval'
    https://*.tile.openstreetmap.org
    https://api.mapbox.com
    https://maps.googleapis.com
    https://*.google.com
    https://*.gstatic.com
    blob: data:;">
```

2. **Safe areas**: Account for notch and navigation bar:
```css
.map-container {
  width: 100%;
  height: 100%;
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
}
/* OR use the Ionic-specific approach: */
ion-content {
  --padding-top: env(safe-area-inset-top);
}
```

3. **Ionic page lifecycle**: Use `ionViewDidEnter` (not `ngOnInit`) for map init:
```typescript
ionViewDidEnter() {
  this.initMap();
  // Leaflet needs a slight delay in Ionic tabs
  setTimeout(() => this.map.invalidateSize(), 100);
}

ionViewWillLeave() {
  // Clean up event listeners but keep map alive if on a tab
}

ngOnDestroy() {
  this.map?.remove();  // Full cleanup
}
```

4. **Tabs**: Maps inside Ionic tabs lose size when switching. Add `invalidateSize()` in `ionViewDidEnter`.

5. **Keyboard**: When soft keyboard opens on search fields, the map container resizes. Handle with:
```typescript
import { Keyboard } from '@capacitor/keyboard';

Keyboard.addListener('keyboardWillShow', () => {
  // Optionally hide map or adjust layout
});
Keyboard.addListener('keyboardDidHide', () => {
  this.map.invalidateSize();
});
```

6. **Geolocation in Capacitor**:
```typescript
import { Geolocation } from '@capacitor/geolocation';

const position = await Geolocation.getCurrentPosition({
  enableHighAccuracy: true,
  timeout: 10000
});
map.setView([position.coords.latitude, position.coords.longitude], 16);
```

---

## Common Patterns {#common}

### Service Pattern (Angular)
```typescript
@Injectable({ providedIn: 'root' })
export class MapService {
  private map: L.Map | null = null;
  private markers = new Map<string, L.Marker>();

  initMap(element: HTMLElement, options?: L.MapOptions): L.Map {
    this.map = L.map(element, {
      center: [-25.2637, -57.5759],
      zoom: 13,
      ...options
    });
    // Add tile layer...
    return this.map;
  }

  addMarker(id: string, lat: number, lng: number): void {
    if (this.markers.has(id)) this.removeMarker(id);
    const marker = L.marker([lat, lng]).addTo(this.map!);
    this.markers.set(id, marker);
  }

  removeMarker(id: string): void {
    const marker = this.markers.get(id);
    if (marker) {
      marker.remove();
      this.markers.delete(id);
    }
  }

  destroy(): void {
    this.markers.clear();
    this.map?.remove();
    this.map = null;
  }
}
```

### Hook Pattern (React)
```tsx
function useMap(containerRef, options) {
  const mapRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = L.map(containerRef.current, {
      center: options.center || [-25.2637, -57.5759],
      zoom: options.zoom || 13
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19
    }).addTo(map);

    const observer = new ResizeObserver(() => map.invalidateSize());
    observer.observe(containerRef.current);

    mapRef.current = map;

    return () => {
      observer.disconnect();
      map.remove();
      mapRef.current = null;
    };
  }, []);

  return mapRef;
}
```
