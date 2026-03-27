# Layout & Responsive Map Containers

## Table of Contents
1. [The Golden Rule](#golden-rule)
2. [Fullscreen Maps](#fullscreen)
3. [Map + Sidebar](#sidebar)
4. [Map in Cards / Panels](#panels)
5. [Ionic / Capacitor Layout](#ionic)
6. [Mobile Responsive](#mobile)
7. [ResizeObserver Pattern](#resize)
8. [CSS Grid & Flexbox Patterns](#grid-flex)
9. [Common Bugs & Fixes](#bugs)

---

## The Golden Rule {#golden-rule}

**Every element from the map container up to `<html>` must have a defined height.**

```css
/* The chain must be unbroken */
html, body { height: 100%; margin: 0; padding: 0; }
#app       { height: 100%; }              /* Framework root */
.layout    { height: 100%; display: flex; } /* Layout wrapper */
.map       { flex: 1; min-height: 0; }     /* Map container */
```

If ANY ancestor has `height: auto` (the default), the map collapses to 0px.

### Quick Diagnostic
If your map is invisible, add this temporarily:
```css
.map-container { background: red !important; }
```
If you see a red rectangle, the container is sized correctly and the issue is map initialization. If you see nothing, the container has zero height — fix the CSS chain.

---

## Fullscreen Maps {#fullscreen}

### Simple Fullscreen (entire viewport)
```css
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  /* OR simply: */
  width: 100vw;
  height: 100vh;
}
```

### Fullscreen Below a Fixed Header
```css
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  z-index: 1000;
}

.map-container {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  bottom: 0;
}

/* Alternative with calc */
.map-container {
  width: 100%;
  height: calc(100vh - 64px);
}

/* Alternative with dvh for mobile (accounts for browser chrome) */
.map-container {
  height: calc(100dvh - 64px);
}
```

### Toggle Fullscreen Programmatically
```javascript
function toggleFullscreen(mapContainer) {
  if (!document.fullscreenElement) {
    mapContainer.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
}

// Listen for fullscreen changes to resize map
document.addEventListener('fullscreenchange', () => {
  map.invalidateSize();  // Leaflet
  // map.resize();        // Mapbox
});
```

---

## Map + Sidebar {#sidebar}

### Collapsible Sidebar (Flexbox)
```css
.layout {
  display: flex;
  height: 100vh;    /* or 100% with parent chain */
  overflow: hidden;
}

.sidebar {
  width: 360px;
  min-width: 0;           /* Allow shrinking */
  overflow-y: auto;
  transition: width 0.3s ease, margin-left 0.3s ease;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: 0;
  overflow: hidden;
}

.map-container {
  flex: 1;
  min-width: 0;           /* Prevent flex overflow */
  min-height: 0;
  position: relative;
}
```

```html
<div class="layout">
  <aside class="sidebar" [class.collapsed]="sidebarCollapsed">
    <!-- sidebar content -->
  </aside>
  <div class="map-container" id="map"></div>
</div>
```

**Remember**: After toggling sidebar, call `invalidateSize()` / `resize()`. The `ResizeObserver` pattern handles this automatically.

### Responsive: Sidebar on Top (Mobile)
```css
@media (max-width: 768px) {
  .layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: 40vh;
    max-height: 300px;
    order: -1;           /* Sidebar on top */
  }

  .sidebar.collapsed {
    height: 0;
    width: 100%;
  }

  .map-container {
    flex: 1;
  }
}
```

### Bottom Sheet (Mobile Alternative)
```css
.bottom-sheet {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-radius: 16px 16px 0 0;
  transform: translateY(calc(100% - 60px));  /* Peek mode: only handle visible */
  transition: transform 0.3s ease;
  z-index: 1000;
  max-height: 70vh;
  overflow-y: auto;
  touch-action: none;    /* Prevent scroll conflicts */
}

.bottom-sheet.open {
  transform: translateY(0);
}

.bottom-sheet .handle {
  width: 40px;
  height: 4px;
  background: #ccc;
  border-radius: 2px;
  margin: 12px auto;
}
```

---

## Map in Cards / Panels {#panels}

### Fixed Height Card
```css
.map-card {
  border-radius: 12px;
  overflow: hidden;        /* Clip map to rounded corners */
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.map-card .map-area {
  height: 300px;           /* Fixed height */
  width: 100%;
}

.map-card .card-content {
  padding: 16px;
}
```

### Aspect-Ratio Card (responsive)
```css
.map-area {
  width: 100%;
  aspect-ratio: 16 / 9;   /* Modern browsers */
}

/* Fallback for older browsers */
.map-area-wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;  /* 16:9 ratio */
}
.map-area-wrapper .map-area {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
}
```

### Map in Tabs / Accordions
```javascript
// The map is initialized but hidden — when the tab becomes visible:
tabElement.addEventListener('shown', () => {
  // Leaflet
  map.invalidateSize();
  // Mapbox
  map.resize();
  // Google Maps
  google.maps.event.trigger(map, 'resize');
});
```

### Map in Modal / Dialog
```javascript
// Wait for modal open animation to complete
modal.addEventListener('transitionend', () => {
  map.invalidateSize();
});

// Or with a safe delay
setTimeout(() => map.invalidateSize(), 300);
```

---

## Ionic / Capacitor Layout {#ionic}

### Full Page Map
```html
<ion-content [fullscreen]="true" class="ion-no-padding">
  <div id="map" class="map-fullscreen"></div>
</ion-content>
```

```css
.map-fullscreen {
  width: 100%;
  height: 100%;
}

/* Ionic sometimes adds padding — override */
ion-content {
  --padding-start: 0;
  --padding-end: 0;
  --padding-top: 0;
  --padding-bottom: 0;
}
```

### Map with Ionic Header + Footer
```html
<ion-header>
  <ion-toolbar>
    <ion-title>Map</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content class="ion-no-padding">
  <div id="map" style="width: 100%; height: 100%;"></div>
</ion-content>

<ion-footer>
  <ion-toolbar>
    <ion-button>Action</ion-button>
  </ion-toolbar>
</ion-footer>
```

Ionic `<ion-content>` handles the height calculation automatically — the map fills between header and footer.

### Map + FAB (floating action button)
```html
<ion-content class="ion-no-padding">
  <div id="map" style="width: 100%; height: 100%;"></div>
  <ion-fab vertical="bottom" horizontal="end" slot="fixed">
    <ion-fab-button (click)="centerOnUser()">
      <ion-icon name="locate"></ion-icon>
    </ion-fab-button>
  </ion-fab>
</ion-content>
```

---

## Mobile Responsive Patterns {#mobile}

### Viewport Meta (essential)
```html
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
```

### Dynamic Viewport Height
```css
/* Use dvh to account for mobile browser chrome (address bar, bottom nav) */
.map-container {
  height: 100dvh;
}

/* Fallback chain */
.map-container {
  height: 100vh;               /* Fallback */
  height: 100dvh;              /* Modern */
  height: -webkit-fill-available; /* iOS Safari fallback */
}
```

### Mobile Control Positioning
```javascript
// Leaflet — move zoom to bottom-right for thumb reach
map.zoomControl.setPosition('bottomright');

// Mapbox — same
map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');

// Hide unnecessary controls on mobile
if (window.innerWidth < 768) {
  map.removeControl(zoomControl);
  map.removeControl(scaleControl);
}
```

### Safe Areas (notched phones)
```css
.map-overlay-controls {
  position: absolute;
  bottom: calc(16px + env(safe-area-inset-bottom));
  right: calc(16px + env(safe-area-inset-right));
}

.map-search-bar {
  position: absolute;
  top: calc(16px + env(safe-area-inset-top));
  left: calc(16px + env(safe-area-inset-left));
  right: calc(16px + env(safe-area-inset-right));
}
```

### Orientation Change
```javascript
// Listen for orientation changes
window.addEventListener('orientationchange', () => {
  // Small delay for browser to finish layout
  setTimeout(() => {
    map.invalidateSize();  // Leaflet
    // map.resize();        // Mapbox
  }, 200);
});

// Better: use ResizeObserver (catches everything)
```

---

## ResizeObserver Pattern {#resize}

This is the **recommended universal approach** for handling map container resizes. It replaces ad-hoc `window.resize` listeners and catches ALL container size changes:

```javascript
function observeMapResize(map, container) {
  const observer = new ResizeObserver(
    debounce(() => {
      // Leaflet
      if (map.invalidateSize) map.invalidateSize({ animate: false });
      // Mapbox GL
      else if (map.resize) map.resize();
      // Google Maps
      else google.maps.event.trigger(map, 'resize');
    }, 100)
  );

  observer.observe(container);
  return observer;  // Store reference to disconnect later
}

// Simple debounce helper
function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}
```

**Use ResizeObserver for**: sidebar toggle, tab switching, accordion, modal, splitter panels, window resize, orientation change, soft keyboard.

---

## CSS Grid & Flexbox Patterns {#grid-flex}

### Dashboard Grid with Map
```css
.dashboard {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr;
  gap: 16px;
  height: 100vh;
  padding: 16px;
}

.stats-bar { grid-column: 1 / -1; }

.map-panel {
  min-height: 0;          /* Critical: prevents grid blowout */
  border-radius: 12px;
  overflow: hidden;
}

.data-panel {
  min-height: 0;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-rows: auto 50vh auto;
  }
}
```

### Split View (Flexbox)
```css
.split-view {
  display: flex;
  height: 100vh;
}

.list-panel {
  width: 400px;
  flex-shrink: 0;
  overflow-y: auto;
}

.map-panel {
  flex: 1;
  min-width: 0;     /* Prevents flex item from overflowing */
  min-height: 0;
}

@media (max-width: 768px) {
  .split-view {
    flex-direction: column-reverse;  /* Map on top */
  }
  .list-panel {
    width: 100%;
    height: 40%;
    flex-shrink: 0;
  }
  .map-panel {
    flex: 1;
  }
}
```

---

## Common Bugs & Fixes {#bugs}

### Map shows gray/blank tiles
- **Cause**: Container had 0 height during initialization
- **Fix**: Verify CSS chain, call `invalidateSize()` after container becomes visible

### Map only shows in top-left corner
- **Cause**: CSS file not loaded
- **Fix**: Import the library's CSS (`leaflet.css`, `mapbox-gl.css`)

### Markers offset from correct position
- **Cause**: `iconAnchor` doesn't match icon image
- **Fix**: Set `iconAnchor` to the point of the icon that should be at the coordinate (typically bottom-center for pins)

### Map doesn't resize with window
- **Cause**: No resize listener
- **Fix**: Use `ResizeObserver` pattern above

### Leaflet icons broken (404 errors)
- **Cause**: Bundler (webpack/Vite) breaks default icon URL resolution
- **Fix**: Manually set icon paths or use `leaflet-defaulticon-compatibility`

### Map interaction conflicts with page scroll
- **Cause**: Scroll events captured by map
- **Fix**: `scrollWheelZoom: false` (Leaflet), `cooperativeGestures: true` (Mapbox), `gestureHandling: 'cooperative'` (Google Maps)

### Flickering on iOS Safari
- **Cause**: GPU compositing issues
- **Fix**: Add `will-change: transform` or `transform: translateZ(0)` to map container

### Map overlaps fixed header
- **Cause**: Leaflet default z-index is high
- **Fix**: Set map container `z-index: 0` or header `z-index: 1000`
