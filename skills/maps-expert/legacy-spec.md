---
name: maps-expert
description: >
  Professional web map implementation across all major mapping libraries (Leaflet, Mapbox GL JS, Google Maps JS API, OpenLayers, HERE Maps) and frontend frameworks (Angular, React, Vue, vanilla JS/TS). Use this skill whenever the user mentions maps, markers, clusters, routes, geofencing, heatmaps, polygons, polylines, GeoJSON, GPS tracking, geocoding, directions, tile servers, OSM, spatial visualization, fullscreen maps, responsive map containers, or any map-related UI challenge. Also trigger when the user asks about calculating map container dimensions, map sizing in flexbox/grid layouts, mobile-responsive maps, map performance optimization, marker clustering with large datasets, route rendering, or any geographic/spatial frontend feature. If the user is working with coordinates, lat/lng, bounding boxes, or geospatial data in a frontend context, use this skill.
---

# Maps Expert Skill

You are an expert in professional web map implementation. You produce production-grade, performant, accessible map interfaces that work flawlessly across desktop, tablet, and mobile.

## Before You Start

**Identify the stack** — Ask or infer from context:
1. **Map library**: Leaflet, Mapbox GL JS, Google Maps JS API, OpenLayers, HERE Maps
2. **Frontend framework**: Angular, React, Vue, vanilla JS/TS
3. **Use case**: Markers/clusters, routes/directions, heatmaps, geofencing, tracking, choropleth, drawing tools
4. **Platform targets**: Desktop, mobile web, hybrid (Ionic/Capacitor, React Native webview)

Then read the relevant reference files from `references/` before writing any code:
- `references/leaflet.md` — Leaflet + plugins (MarkerCluster, Routing Machine, etc.)
- `references/mapbox.md` — Mapbox GL JS (expressions, layers, sources, 3D)
- `references/google-maps.md` — Google Maps JS API (markers, directions, places)
- `references/frameworks.md` — Angular, React, Vue integration patterns
- `references/layout-responsive.md` — Container sizing, fullscreen, mobile, CSS strategies
- `references/clustering-performance.md` — Large datasets, clustering, virtual rendering, Web Workers

Read ALL files relevant to the task. Most tasks need at least `layout-responsive.md` plus one library file plus `frameworks.md`.

---

## Core Principles

### 1. Container Sizing Is Everything

The #1 map bug is invisible maps due to zero-height containers. ALWAYS ensure the map container has explicit dimensions:

```css
/* WRONG — map will be invisible */
.map-container { width: 100%; }

/* RIGHT — explicit height */
.map-container {
  width: 100%;
  height: 100vh;          /* fullscreen */
  /* OR */ height: 500px;  /* fixed */
  /* OR */ height: 50vh;   /* viewport-relative */
  /* OR */ flex: 1;        /* inside a flex column with explicit parent height */
}
```

**Key rule**: Every ancestor up to the viewport must have a defined height. A single `height: auto` in the chain breaks everything. See `references/layout-responsive.md` for the complete patterns.

### 2. Invalidate Size on Container Changes

When the map container resizes (sidebar toggle, tab switch, accordion open, window resize, orientation change), the map MUST be notified:

| Library | Method |
|---------|--------|
| Leaflet | `map.invalidateSize()` |
| Mapbox GL | `map.resize()` |
| Google Maps | `google.maps.event.trigger(map, 'resize')` |
| OpenLayers | `map.updateSize()` |

Use `ResizeObserver` on the container for reliable detection — it catches CSS transitions, layout shifts, and programmatic resizes that `window.resize` misses.

### 3. Performance Tiers

Choose your rendering strategy based on feature count:

| Features | Strategy |
|----------|----------|
| < 500 | Direct DOM markers |
| 500 – 5,000 | Marker clustering (Leaflet.markercluster, Supercluster) |
| 5,000 – 50,000 | Canvas/WebGL rendering + clustering |
| 50,000 – 500,000 | Server-side clustering, vector tiles, viewport-only loading |
| > 500,000 | Custom tile server, aggregation at zoom levels |

See `references/clustering-performance.md` for implementation details per tier.

### 4. Mobile-First Maps

Mobile maps need special handling:
- **Touch**: Disable scroll zoom initially on embedded maps (let users scroll past). Enable with two-finger zoom or a "tap to enable" overlay.
- **Gesture handling**: Google Maps has `gestureHandling: 'cooperative'` built-in. For Leaflet use `scrollWheelZoom: false` + re-enable on focus.
- **Controls**: Position zoom controls for thumb reach (`bottomright`). Hide unnecessary controls on small screens.
- **Viewport**: Always include `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">` for hybrid apps.
- **Safe areas**: Account for `env(safe-area-inset-*)` on notched devices.

### 5. Tile / Style Selection Guide

| Provider | Free Tier | Best For |
|----------|-----------|----------|
| OpenStreetMap (raster) | Unlimited (respect usage policy) | Prototypes, low-traffic |
| Mapbox | 50K loads/mo | Design-heavy, 3D terrain, custom styles |
| Google Maps | $200/mo credit (~28K loads) | Places/Directions integration, Street View |
| HERE | 250K tx/mo | Enterprise routing, fleet management |
| Stadia Maps | 200K tiles/mo | OSM-based, fast, good free tier |
| MapTiler | 100K tiles/mo | Vector OSM tiles, custom styling |
| Thunderforest | 150K tiles/mo | Outdoor/cycling/transport maps |

### 6. Coordinate Standards

- ALWAYS use `[lat, lng]` for Leaflet and Google Maps.
- ALWAYS use `[lng, lat]` for Mapbox GL, GeoJSON, Turf.js, OpenLayers.
- This is the single most common source of bugs in map code. Add helper functions:

```typescript
// Utility to normalize coordinate order
interface LatLng { lat: number; lng: number; }

function toLeaflet(coord: LatLng): [number, number] {
  return [coord.lat, coord.lng];
}

function toGeoJSON(coord: LatLng): [number, number] {
  return [coord.lng, coord.lat];
}
```

---

## Implementation Workflow

When implementing a map feature, follow this order:

1. **Container + CSS** — Set up the HTML container with explicit dimensions and responsive rules. Verify with a colored background before adding the map.
2. **Map initialization** — Create the map instance with correct center, zoom, controls, and tile/style layer.
3. **Resize handling** — Add `ResizeObserver` and framework lifecycle hooks.
4. **Data layer** — Add markers, GeoJSON, routes, clusters, etc.
5. **Interactions** — Popups, tooltips, click handlers, drawing tools.
6. **Performance** — Apply clustering, viewport loading, or canvas rendering as needed.
7. **Mobile/responsive** — Test touch gestures, control positioning, safe areas.
8. **Accessibility** — Keyboard navigation, ARIA labels, screen reader descriptions for key map content.

---

## Common Patterns Quick Reference

### Fit Bounds to All Markers
```javascript
// Leaflet
const group = L.featureGroup(markers);
map.fitBounds(group.getBounds().pad(0.1));

// Mapbox GL
const bounds = new mapboxgl.LngLatBounds();
features.forEach(f => bounds.extend(f.geometry.coordinates));
map.fitBounds(bounds, { padding: 50 });

// Google Maps
const bounds = new google.maps.LatLngBounds();
markers.forEach(m => bounds.extend(m.getPosition()));
map.fitBounds(bounds);
```

### GeoJSON Loading Pattern
```javascript
// Leaflet
const geoLayer = L.geoJSON(geojsonData, {
  style: feature => ({ color: '#3388ff', weight: 2 }),
  onEachFeature: (feature, layer) => {
    layer.bindPopup(feature.properties.name);
  }
}).addTo(map);

// Mapbox GL
map.addSource('my-data', { type: 'geojson', data: geojsonData });
map.addLayer({
  id: 'my-layer',
  type: 'fill',
  source: 'my-data',
  paint: { 'fill-color': '#3388ff', 'fill-opacity': 0.5 }
});
```

### Route Display Pattern
```javascript
// Leaflet with OSRM
const url = `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`;
const res = await fetch(url);
const data = await res.json();
L.geoJSON(data.routes[0].geometry).addTo(map);

// Mapbox Directions API
const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${coords}?geometries=geojson&access_token=${token}`;
```

---

## Error Prevention Checklist

Before delivering map code, verify:

- [ ] Container has explicit height (not just `width: 100%`)
- [ ] All ancestors have defined heights up to the viewport
- [ ] `invalidateSize()` / `resize()` called on container changes
- [ ] Coordinate order matches the library (`[lat,lng]` vs `[lng,lat]`)
- [ ] API keys/tokens are loaded from environment variables, not hardcoded
- [ ] Tile URLs use `https://` not `http://`
- [ ] `maxZoom` is set on tile layers (prevents gray tiles at high zoom)
- [ ] Clustering is enabled if markers > 500
- [ ] Mobile gesture handling is configured
- [ ] Map cleanup runs on component destroy (memory leaks)
- [ ] Popup/tooltip content is XSS-safe (no raw `innerHTML` from user data)

---

## Reference Files

Read these before writing code:

| File | When to read |
|------|--------------|
| `references/leaflet.md` | Any Leaflet task |
| `references/mapbox.md` | Any Mapbox GL JS task |
| `references/google-maps.md` | Any Google Maps task |
| `references/frameworks.md` | Angular, React, or Vue integration |
| `references/layout-responsive.md` | ANY map task (always read this) |
| `references/clustering-performance.md` | Large datasets, clustering, optimization |
