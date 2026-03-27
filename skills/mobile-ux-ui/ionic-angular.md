# Ionic Framework + Angular — Referencia UX/UI

## Tabla de Contenidos
1. Estructura de Componentes
2. Theming con CSS Custom Properties
3. Componentes Ionic Clave para UX
4. Navegación y Routing
5. Adaptive Styling (iOS vs Android)
6. Integración con Capacitor
7. Patrones de Layout
8. Performance y Optimización
9. Accesibilidad
10. Patrones Avanzados

---

## 1. Estructura de Componentes

Cada pantalla en Ionic Angular sigue esta estructura base:

```html
<ion-header [translucent]="true">
  <ion-toolbar>
    <ion-buttons slot="start">
      <ion-back-button defaultHref="/home"></ion-back-button>
    </ion-buttons>
    <ion-title>Título de Pantalla</ion-title>
    <ion-buttons slot="end">
      <!-- Acciones secundarias -->
    </ion-buttons>
  </ion-toolbar>
</ion-header>

<ion-content [fullscreen]="true">
  <!-- Para large title effect en iOS -->
  <ion-header collapse="condense">
    <ion-toolbar>
      <ion-title size="large">Título de Pantalla</ion-title>
    </ion-toolbar>
  </ion-header>

  <!-- Contenido principal -->
  <ion-refresher slot="fixed" (ionRefresh)="onRefresh($event)">
    <ion-refresher-content></ion-refresher-content>
  </ion-refresher>

  <!-- ... contenido ... -->
</ion-content>

<!-- FAB o footer si aplica -->
<ion-footer *ngIf="showFooter">
  <ion-toolbar>
    <ion-button expand="block">Acción Principal</ion-button>
  </ion-toolbar>
</ion-footer>
```

Reglas importantes:
- Siempre usa `[translucent]="true"` en `ion-header` e `ion-content` para el efecto de blur en iOS.
- Usa `[fullscreen]="true"` en `ion-content` cuando uses collapsible large titles.
- El `ion-back-button` con `defaultHref` es obligatorio para navegación predecible.
- Slot `start` para navegación, slot `end` para acciones contextuales (máx. 2-3 iconos).

## 2. Theming con CSS Custom Properties

### Variables Globales (theme/variables.scss)

```scss
:root {
  // Colores primarios de marca
  --ion-color-primary: #3880ff;
  --ion-color-primary-rgb: 56, 128, 255;
  --ion-color-primary-contrast: #ffffff;
  --ion-color-primary-shade: #3171e0;
  --ion-color-primary-tint: #4c8dff;

  // Tipografía
  --ion-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --ion-text-color: #1a1a1a;

  // Espaciado consistente (design tokens)
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  // Bordes y sombras
  --border-radius-sm: 8px;
  --border-radius-md: 12px;
  --border-radius-lg: 16px;

  // Elevation (sombras)
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.16);
}

// Dark Mode
@media (prefers-color-scheme: dark) {
  :root {
    --ion-background-color: #121212;
    --ion-text-color: #f4f4f4;
    --ion-card-background: #1e1e1e;
    --ion-item-background: #1e1e1e;
    --ion-toolbar-background: #1a1a1a;
  }
}
```

### Variables por Componente

```scss
// Personalizar componentes específicos sin !important
ion-card {
  --background: var(--ion-card-background, #ffffff);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

ion-item {
  --padding-start: var(--spacing-md);
  --padding-end: var(--spacing-md);
  --min-height: 52px; // Touch target mínimo
}

ion-button {
  --border-radius: var(--border-radius-sm);
  --padding-top: 12px;
  --padding-bottom: 12px;
  min-height: 48px; // Accesibilidad
  font-weight: 600;
}
```

## 3. Componentes Ionic Clave para UX

### Listas con Swipe Actions

```html
<ion-list>
  <ion-item-sliding *ngFor="let item of items; trackBy: trackById">
    <ion-item-options side="start">
      <ion-item-option color="success" (click)="archive(item)">
        <ion-icon slot="icon-only" name="archive-outline"></ion-icon>
      </ion-item-option>
    </ion-item-options>

    <ion-item [detail]="true" [button]="true" (click)="openDetail(item)">
      <ion-avatar slot="start" *ngIf="item.avatar">
        <img [src]="item.avatar" [alt]="item.name" loading="lazy" />
      </ion-avatar>
      <ion-label>
        <h2>{{ item.title }}</h2>
        <p>{{ item.subtitle }}</p>
      </ion-label>
      <ion-note slot="end">{{ item.time | timeAgo }}</ion-note>
    </ion-item>

    <ion-item-options side="end">
      <ion-item-option color="danger" (click)="confirmDelete(item)">
        <ion-icon slot="icon-only" name="trash-outline"></ion-icon>
      </ion-item-option>
    </ion-item-options>
  </ion-item-sliding>
</ion-list>
```

### Skeleton Screens (Loading State)

```html
<!-- Mientras carga -->
<ng-container *ngIf="loading; else contentLoaded">
  <ion-list>
    <ion-item *ngFor="let _ of skeletonItems">
      <ion-avatar slot="start">
        <ion-skeleton-text [animated]="true"></ion-skeleton-text>
      </ion-avatar>
      <ion-label>
        <h2><ion-skeleton-text [animated]="true" style="width: 60%"></ion-skeleton-text></h2>
        <p><ion-skeleton-text [animated]="true" style="width: 80%"></ion-skeleton-text></p>
      </ion-label>
    </ion-item>
  </ion-list>
</ng-container>

<ng-template #contentLoaded>
  <!-- Contenido real -->
</ng-template>
```

### Empty State

```html
<div class="empty-state" *ngIf="!loading && items.length === 0">
  <ion-icon name="document-outline" class="empty-state__icon"></ion-icon>
  <h3 class="empty-state__title">No hay registros aún</h3>
  <p class="empty-state__description">
    Comienza agregando tu primer registro tocando el botón de abajo.
  </p>
  <ion-button (click)="createNew()" class="empty-state__cta">
    <ion-icon name="add-outline" slot="start"></ion-icon>
    Crear Registro
  </ion-button>
</div>
```

```scss
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--spacing-xl) var(--spacing-lg);
  min-height: 50vh;

  &__icon {
    font-size: 64px;
    color: var(--ion-color-medium);
    margin-bottom: var(--spacing-md);
  }

  &__title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--ion-text-color);
    margin-bottom: var(--spacing-sm);
  }

  &__description {
    font-size: 0.95rem;
    color: var(--ion-color-medium);
    max-width: 280px;
    line-height: 1.5;
    margin-bottom: var(--spacing-lg);
  }
}
```

### Bottom Sheet / Modal con presentingElement

```typescript
@Component({ ... })
export class MyPage {
  @ViewChild(IonContent) content: IonContent;

  async openBottomSheet() {
    const modal = await this.modalCtrl.create({
      component: DetailComponent,
      presentingElement: await this.modalCtrl.getTop() || document.querySelector('ion-router-outlet'),
      breakpoints: [0, 0.4, 0.75, 1],
      initialBreakpoint: 0.4,
      backdropBreakpoint: 0.4,
      handle: true,
      cssClass: 'bottom-sheet-modal'
    });
    await modal.present();
  }
}
```

### Action Sheet para Decisiones

```typescript
async showOptions(item: Item) {
  const actionSheet = await this.actionSheetCtrl.create({
    header: item.title,
    subHeader: 'Selecciona una acción',
    buttons: [
      {
        text: 'Editar',
        icon: 'create-outline',
        handler: () => this.edit(item)
      },
      {
        text: 'Compartir',
        icon: 'share-outline',
        handler: () => this.share(item)
      },
      {
        text: 'Eliminar',
        role: 'destructive',
        icon: 'trash-outline',
        handler: () => this.confirmDelete(item)
      },
      {
        text: 'Cancelar',
        role: 'cancel',
        icon: 'close-outline'
      }
    ]
  });
  await actionSheet.present();
}
```

## 4. Navegación y Routing

### Estructura de Tabs recomendada

```typescript
// tabs-routing.module.ts
const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'home',
        loadChildren: () => import('../home/home.module').then(m => m.HomePageModule)
      },
      {
        path: 'search',
        loadChildren: () => import('../search/search.module').then(m => m.SearchPageModule)
      },
      {
        path: 'profile',
        loadChildren: () => import('../profile/profile.module').then(m => m.ProfilePageModule)
      },
      {
        path: '',
        redirectTo: 'home',
        pathMatch: 'full'
      }
    ]
  }
];
```

```html
<!-- tabs.page.html -->
<ion-tabs>
  <ion-tab-bar slot="bottom">
    <ion-tab-button tab="home">
      <ion-icon name="home-outline" aria-hidden="true"></ion-icon>
      <ion-label>Inicio</ion-label>
    </ion-tab-button>
    <ion-tab-button tab="search">
      <ion-icon name="search-outline" aria-hidden="true"></ion-icon>
      <ion-label>Buscar</ion-label>
    </ion-tab-button>
    <ion-tab-button tab="profile">
      <ion-icon name="person-outline" aria-hidden="true"></ion-icon>
      <ion-label>Perfil</ion-label>
    </ion-tab-button>
  </ion-tab-bar>
</ion-tabs>
```

Reglas de UX para tabs:
- Máximo 5 tabs. Si necesitas más, usa un drawer o reorganiza la arquitectura de información.
- Usa iconos `outline` para inactivo y `filled` para activo (Ionic lo maneja con `ion-icon`).
- Incluye siempre `ion-label` además del icono para accesibilidad y claridad.
- Cada tab mantiene su propio stack de navegación independiente.

## 5. Adaptive Styling (iOS vs Android)

Ionic aplica estilos adaptativos automáticamente con `mode="ios"` y `mode="md"`. Aprovéchalo:

```scss
// Estilos específicos por plataforma
.ios {
  ion-card {
    border-radius: 12px;
    box-shadow: none;
    border: 0.5px solid rgba(0, 0, 0, 0.1);
  }
}

.md {
  ion-card {
    border-radius: 8px;
    box-shadow: var(--shadow-sm);
    border: none;
  }
}
```

```typescript
// En código TypeScript
import { Platform } from '@ionic/angular';

constructor(private platform: Platform) {
  if (this.platform.is('ios')) {
    // Haptic feedback más sutil
  } else {
    // Ripple effects
  }
}
```

## 6. Integración con Capacitor

Funcionalidades nativas que mejoran la UX:

```typescript
// Haptics - feedback táctil
import { Haptics, ImpactStyle } from '@capacitor/haptics';

async onButtonTap() {
  await Haptics.impact({ style: ImpactStyle.Light });
}

async onSuccess() {
  await Haptics.notification({ type: 'SUCCESS' });
}

// Status Bar - integración visual
import { StatusBar, Style } from '@capacitor/status-bar';

async setDarkStatusBar() {
  await StatusBar.setStyle({ style: Style.Dark });
  await StatusBar.setBackgroundColor({ color: '#1a1a1a' });
}

// Keyboard - ajustar layout cuando aparece el teclado
import { Keyboard, KeyboardResize } from '@capacitor/keyboard';

Keyboard.addListener('keyboardWillShow', (info) => {
  // Ajustar scroll o layout
});

// Splash Screen - transición suave al contenido
import { SplashScreen } from '@capacitor/splash-screen';

async initApp() {
  await this.loadInitialData();
  await SplashScreen.hide({ fadeOutDuration: 300 });
}
```

## 7. Patrones de Layout

### Safe Area handling

```scss
// Respetar notch, home indicator, etc.
ion-content {
  --padding-top: env(safe-area-inset-top);
  --padding-bottom: env(safe-area-inset-bottom);
}

// Para elementos fijos fuera de ion-content
.fixed-bottom-bar {
  padding-bottom: calc(var(--spacing-md) + env(safe-area-inset-bottom));
}
```

### Grid responsive

```html
<ion-grid fixed>
  <ion-row>
    <ion-col size="12" size-md="6" size-lg="4" *ngFor="let card of cards">
      <app-card-component [data]="card"></app-card-component>
    </ion-col>
  </ion-row>
</ion-grid>
```

### Scroll infinito con virtualización

```html
<ion-content>
  <ion-list>
    <ion-virtual-scroll [items]="items" approxItemHeight="72px">
      <ion-item *virtualItem="let item">
        <ion-label>{{ item.name }}</ion-label>
      </ion-item>
    </ion-virtual-scroll>
  </ion-list>

  <ion-infinite-scroll (ionInfinite)="loadMore($event)">
    <ion-infinite-scroll-content
      loadingSpinner="crescent"
      loadingText="Cargando más...">
    </ion-infinite-scroll-content>
  </ion-infinite-scroll>
</ion-content>
```

## 8. Performance y Optimización

- **Lazy loading de páginas**: Siempre usa `loadChildren` en routing, nunca imports directos.
- **OnPush Change Detection**: Usa `changeDetection: ChangeDetectionStrategy.OnPush` en componentes
  de presentación para reducir re-renders innecesarios.
- **TrackBy en ngFor**: Siempre proporciona `trackBy` en listas para evitar re-creación del DOM.
- **Imágenes**: Usa `loading="lazy"` en `<img>`, considera `ion-img` para intersection observer
  integrado. Sirve imágenes en el tamaño correcto (no envíes 2000px para un thumbnail de 80px).
- **Animations**: Prefiere CSS transforms y opacity (GPU-accelerated) sobre propiedades que
  causan layout (width, height, top, left).

## 9. Accesibilidad

```html
<!-- Roles y labels -->
<ion-button aria-label="Agregar nuevo registro" (click)="add()">
  <ion-icon slot="icon-only" name="add-outline" aria-hidden="true"></ion-icon>
</ion-button>

<!-- Live regions para actualizaciones dinámicas -->
<div aria-live="polite" class="sr-only">
  {{ statusMessage }}
</div>

<!-- Agrupación semántica -->
<ion-item role="listitem">
  <ion-label>
    <h2 id="item-title-{{item.id}}">{{ item.title }}</h2>
    <p aria-describedby="item-title-{{item.id}}">{{ item.description }}</p>
  </ion-label>
</ion-item>
```

```scss
// Clase para screen readers
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
```

## 10. Patrones Avanzados

### Formulario con validación UX-friendly

```typescript
// Validación inline, no intrusiva
this.form = this.fb.group({
  email: ['', [Validators.required, Validators.email]],
  phone: ['', [Validators.required, Validators.pattern(/^\+?[0-9]{8,15}$/)]],
});

// Mostrar error solo cuando el campo pierde foco (blur), no mientras escribe
shouldShowError(field: string): boolean {
  const control = this.form.get(field);
  return control?.invalid && control?.touched;
}
```

```html
<ion-item [class.ion-invalid]="shouldShowError('email')">
  <ion-input
    label="Email"
    labelPlacement="floating"
    type="email"
    formControlName="email"
    inputmode="email"
    autocomplete="email"
    (ionBlur)="markTouched('email')">
  </ion-input>
  <ion-note slot="error">Ingresa un email válido</ion-note>
</ion-item>
```

### Patrón de Search con debounce

```typescript
searchControl = new FormControl('');

ngOnInit() {
  this.searchControl.valueChanges.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(query => this.searchService.search(query))
  ).subscribe(results => {
    this.results = results;
    this.cdr.markForCheck();
  });
}
```

### Estado de conectividad visible

```typescript
import { Network } from '@capacitor/network';

async initNetworkListener() {
  Network.addListener('networkStatusChange', (status) => {
    if (!status.connected) {
      this.showOfflineBanner();
    } else {
      this.hideOfflineBanner();
      this.syncPendingData();
    }
  });
}
```

```html
<div class="offline-banner" *ngIf="isOffline" role="alert">
  <ion-icon name="cloud-offline-outline"></ion-icon>
  <span>Sin conexión. Los cambios se sincronizarán automáticamente.</span>
</div>
```
