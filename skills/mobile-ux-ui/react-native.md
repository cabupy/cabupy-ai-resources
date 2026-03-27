# React Native — Referencia UX/UI

## Tabla de Contenidos
1. Estructura de Componentes
2. Theming y Design Tokens
3. Componentes UI Clave
4. Navegación con React Navigation
5. Diferencias de Plataforma
6. Animaciones y Gestos
7. Patrones de Layout
8. Performance y Optimización
9. Accesibilidad
10. Patrones Avanzados

---

## 1. Estructura de Componentes

Cada pantalla sigue esta estructura base:

```tsx
import React from 'react';
import { View, StyleSheet, StatusBar } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useTheme } from '../hooks/useTheme';

interface ScreenProps {
  children: React.ReactNode;
  headerTitle?: string;
}

export const Screen: React.FC<ScreenProps> = ({ children, headerTitle }) => {
  const { colors, isDark } = useTheme();

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <StatusBar
        barStyle={isDark ? 'light-content' : 'dark-content'}
        backgroundColor={colors.background}
      />
      {children}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
```

Reglas importantes:
- Siempre usa `SafeAreaView` de `react-native-safe-area-context` (no el de React Native core).
- Configura `StatusBar` consistentemente con el tema.
- Usa `StyleSheet.create()` para estilos estáticos (optimización automática).
- Componentes funcionales con hooks como estándar.

## 2. Theming y Design Tokens

### Theme centralizado

```tsx
// theme/tokens.ts
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const borderRadius = {
  sm: 8,
  md: 12,
  lg: 16,
  full: 9999,
} as const;

export const typography = {
  heading1: { fontSize: 28, fontWeight: '700' as const, lineHeight: 34 },
  heading2: { fontSize: 22, fontWeight: '600' as const, lineHeight: 28 },
  heading3: { fontSize: 18, fontWeight: '600' as const, lineHeight: 24 },
  body: { fontSize: 16, fontWeight: '400' as const, lineHeight: 22 },
  bodySmall: { fontSize: 14, fontWeight: '400' as const, lineHeight: 20 },
  caption: { fontSize: 12, fontWeight: '400' as const, lineHeight: 16 },
};

export const lightColors = {
  background: '#FFFFFF',
  surface: '#F5F5F5',
  surfaceElevated: '#FFFFFF',
  text: '#1A1A1A',
  textSecondary: '#666666',
  textTertiary: '#999999',
  primary: '#3880FF',
  primaryLight: '#EBF2FF',
  success: '#2DD36F',
  warning: '#FFC409',
  danger: '#EB445A',
  border: '#E0E0E0',
  separator: '#F0F0F0',
  shadow: 'rgba(0, 0, 0, 0.08)',
};

export const darkColors: typeof lightColors = {
  background: '#121212',
  surface: '#1E1E1E',
  surfaceElevated: '#2A2A2A',
  text: '#F4F4F4',
  textSecondary: '#B0B0B0',
  textTertiary: '#707070',
  primary: '#5B9FFF',
  primaryLight: '#1A2A40',
  success: '#4ADE80',
  warning: '#FFD54F',
  danger: '#FF6B6B',
  border: '#333333',
  separator: '#252525',
  shadow: 'rgba(0, 0, 0, 0.3)',
};
```

### Theme Provider con Dark Mode

```tsx
// theme/ThemeContext.tsx
import React, { createContext, useContext, useMemo } from 'react';
import { useColorScheme } from 'react-native';
import { lightColors, darkColors, spacing, borderRadius, typography } from './tokens';

interface Theme {
  colors: typeof lightColors;
  spacing: typeof spacing;
  borderRadius: typeof borderRadius;
  typography: typeof typography;
  isDark: boolean;
}

const ThemeContext = createContext<Theme | null>(null);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';

  const theme = useMemo<Theme>(() => ({
    colors: isDark ? darkColors : lightColors,
    spacing,
    borderRadius,
    typography,
    isDark,
  }), [isDark]);

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): Theme => {
  const theme = useContext(ThemeContext);
  if (!theme) throw new Error('useTheme must be used within ThemeProvider');
  return theme;
};
```

## 3. Componentes UI Clave

### Lista con Swipe Actions (react-native-gesture-handler + reanimated)

```tsx
import { Swipeable } from 'react-native-gesture-handler';
import Animated from 'react-native-reanimated';

const ListItem: React.FC<{ item: Item; onDelete: () => void }> = ({ item, onDelete }) => {
  const { colors, spacing } = useTheme();

  const renderRightActions = () => (
    <TouchableOpacity
      style={[styles.deleteAction, { backgroundColor: colors.danger }]}
      onPress={onDelete}
      accessibilityLabel={`Eliminar ${item.title}`}
      accessibilityRole="button"
    >
      <Icon name="trash-outline" size={24} color="#FFF" />
    </TouchableOpacity>
  );

  return (
    <Swipeable renderRightActions={renderRightActions} overshootRight={false}>
      <View style={[styles.itemContainer, { backgroundColor: colors.surface }]}>
        <View style={styles.itemContent}>
          <Text style={[styles.itemTitle, { color: colors.text }]}>{item.title}</Text>
          <Text style={[styles.itemSubtitle, { color: colors.textSecondary }]}>
            {item.subtitle}
          </Text>
        </View>
        <Icon name="chevron-forward" size={20} color={colors.textTertiary} />
      </View>
    </Swipeable>
  );
};

const styles = StyleSheet.create({
  itemContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 14,
    minHeight: 52,
  },
  itemContent: { flex: 1 },
  itemTitle: { fontSize: 16, fontWeight: '500' },
  itemSubtitle: { fontSize: 14, marginTop: 2 },
  deleteAction: {
    justifyContent: 'center',
    alignItems: 'center',
    width: 72,
  },
});
```

### Skeleton Screen

```tsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withTiming,
} from 'react-native-reanimated';

const SkeletonBox: React.FC<{ width: number | string; height: number }> = ({ width, height }) => {
  const { colors } = useTheme();
  const opacity = useSharedValue(0.3);

  React.useEffect(() => {
    opacity.value = withRepeat(withTiming(0.7, { duration: 800 }), -1, true);
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
  }));

  return (
    <Animated.View
      style={[
        { width, height, backgroundColor: colors.border, borderRadius: 6 },
        animatedStyle,
      ]}
    />
  );
};

// Uso en lista
const ListSkeleton: React.FC = () => (
  <View style={{ padding: 16 }}>
    {Array.from({ length: 6 }).map((_, i) => (
      <View key={i} style={{ flexDirection: 'row', marginBottom: 16, alignItems: 'center' }}>
        <SkeletonBox width={48} height={48} />
        <View style={{ marginLeft: 12, flex: 1 }}>
          <SkeletonBox width="60%" height={16} />
          <View style={{ marginTop: 8 }}>
            <SkeletonBox width="80%" height={12} />
          </View>
        </View>
      </View>
    ))}
  </View>
);
```

### Empty State

```tsx
const EmptyState: React.FC<{
  icon: string;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}> = ({ icon, title, description, actionLabel, onAction }) => {
  const { colors, spacing, typography } = useTheme();

  return (
    <View style={styles.container} accessibilityRole="text">
      <Icon name={icon} size={64} color={colors.textTertiary} />
      <Text style={[typography.heading3, { color: colors.text, marginTop: spacing.md }]}>
        {title}
      </Text>
      <Text style={[
        typography.body,
        { color: colors.textSecondary, textAlign: 'center', marginTop: spacing.sm, maxWidth: 280 }
      ]}>
        {description}
      </Text>
      {actionLabel && onAction && (
        <TouchableOpacity
          style={[styles.ctaButton, { backgroundColor: colors.primary, marginTop: spacing.lg }]}
          onPress={onAction}
          accessibilityRole="button"
        >
          <Text style={[typography.body, { color: '#FFF', fontWeight: '600' }]}>
            {actionLabel}
          </Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 32,
    minHeight: '50%',
  },
  ctaButton: {
    paddingHorizontal: 24,
    paddingVertical: 14,
    borderRadius: 12,
    minHeight: 48,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
```

### Bottom Sheet (con @gorhom/bottom-sheet)

```tsx
import BottomSheet, { BottomSheetBackdrop, BottomSheetView } from '@gorhom/bottom-sheet';

const MyScreen: React.FC = () => {
  const bottomSheetRef = useRef<BottomSheet>(null);
  const snapPoints = useMemo(() => ['25%', '50%', '90%'], []);
  const { colors } = useTheme();

  const renderBackdrop = useCallback(
    (props: any) => (
      <BottomSheetBackdrop {...props} disappearsOnIndex={-1} appearsOnIndex={0} opacity={0.5} />
    ),
    []
  );

  return (
    <>
      {/* Trigger */}
      <TouchableOpacity onPress={() => bottomSheetRef.current?.expand()}>
        <Text>Abrir detalles</Text>
      </TouchableOpacity>

      <BottomSheet
        ref={bottomSheetRef}
        index={-1}
        snapPoints={snapPoints}
        enablePanDownToClose
        backdropComponent={renderBackdrop}
        handleIndicatorStyle={{ backgroundColor: colors.textTertiary }}
        backgroundStyle={{ backgroundColor: colors.surfaceElevated }}
      >
        <BottomSheetView style={{ padding: 16 }}>
          {/* Contenido del bottom sheet */}
        </BottomSheetView>
      </BottomSheet>
    </>
  );
};
```

## 4. Navegación con React Navigation

### Estructura de Tabs + Stack

```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const HomeStack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const HomeStackScreen = () => (
  <HomeStack.Navigator
    screenOptions={{
      headerLargeTitle: true,          // iOS large title
      headerShadowVisible: false,      // Limpio
      headerBackTitleVisible: false,    // Solo flecha en iOS
    }}
  >
    <HomeStack.Screen name="HomeList" component={HomeListScreen} />
    <HomeStack.Screen name="Detail" component={DetailScreen} />
  </HomeStack.Navigator>
);

const TabNavigator = () => {
  const { colors } = useTheme();

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textTertiary,
        tabBarStyle: {
          backgroundColor: colors.surface,
          borderTopColor: colors.separator,
          borderTopWidth: StyleSheet.hairlineWidth,
        },
        tabBarIcon: ({ focused, color, size }) => {
          const iconName = getIconName(route.name, focused);
          return <Icon name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Home" component={HomeStackScreen} options={{ tabBarLabel: 'Inicio' }} />
      <Tab.Screen name="Search" component={SearchScreen} options={{ tabBarLabel: 'Buscar' }} />
      <Tab.Screen name="Profile" component={ProfileScreen} options={{ tabBarLabel: 'Perfil' }} />
    </Tab.Navigator>
  );
};

// Modal presentation (pantalla completa desde abajo)
const RootStack = createNativeStackNavigator();

export const App = () => (
  <ThemeProvider>
    <NavigationContainer>
      <RootStack.Navigator>
        <RootStack.Screen name="Tabs" component={TabNavigator} options={{ headerShown: false }} />
        <RootStack.Screen
          name="CreateItem"
          component={CreateItemScreen}
          options={{ presentation: 'modal', headerTitle: 'Nuevo Item' }}
        />
      </RootStack.Navigator>
    </NavigationContainer>
  </ThemeProvider>
);
```

## 5. Diferencias de Plataforma

```tsx
import { Platform } from 'react-native';

// Estilos adaptativos
const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 8,
    },
    android: {
      elevation: 4,
    },
  }),
  headerPadding: {
    paddingTop: Platform.OS === 'ios' ? 0 : 8,  // iOS maneja insets automáticamente
  },
});

// Haptics por plataforma
import * as Haptics from 'expo-haptics';
// o react-native-haptic-feedback para bare workflow

const triggerFeedback = () => {
  if (Platform.OS === 'ios') {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  } else {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    // Android puede necesitar ajuste de intensidad
  }
};
```

Convenciones por plataforma:
- **iOS**: Large titles, swipe back gesture, bottom tab bar, action sheets desde abajo,
  header blur effect, SF Symbols.
- **Android**: Material top app bar, FAB para acción primaria, navigation drawer,
  snackbar en vez de toast, ripple effect en touches, Material Icons.

## 6. Animaciones y Gestos

### Animación de entrada con Reanimated

```tsx
import Animated, { FadeInUp, FadeInDown, Layout } from 'react-native-reanimated';

const AnimatedListItem: React.FC<{ index: number }> = ({ index, children }) => (
  <Animated.View
    entering={FadeInUp.delay(index * 50).springify()}
    layout={Layout.springify()}
  >
    {children}
  </Animated.View>
);
```

### Pull to Refresh

```tsx
const [refreshing, setRefreshing] = useState(false);

const onRefresh = useCallback(async () => {
  setRefreshing(true);
  try {
    await fetchData();
  } finally {
    setRefreshing(false);
  }
}, []);

<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}
  refreshControl={
    <RefreshControl
      refreshing={refreshing}
      onRefresh={onRefresh}
      tintColor={colors.primary}    // iOS spinner color
      colors={[colors.primary]}     // Android spinner colors
    />
  }
/>
```

## 7. Patrones de Layout

### Flex patterns para mobile

```tsx
// Card con contenido flexible
const styles = StyleSheet.create({
  card: {
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 8,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  spaceBetween: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  // Imagen con aspect ratio fijo
  imageContainer: {
    width: '100%',
    aspectRatio: 16 / 9,
    borderRadius: 8,
    overflow: 'hidden',
  },
  // Footer fijo con safe area
  fixedBottom: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 34, // home indicator
    borderTopWidth: StyleSheet.hairlineWidth,
  },
});
```

### Scroll con header sticky

```tsx
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}
  ListHeaderComponent={<SearchBar />}
  stickyHeaderIndices={[0]}  // Sticky search bar
  ItemSeparatorComponent={() => (
    <View style={{ height: StyleSheet.hairlineWidth, backgroundColor: colors.separator, marginLeft: 16 }} />
  )}
  ListEmptyComponent={<EmptyState icon="search" title="Sin resultados" description="..." />}
  contentContainerStyle={{ flexGrow: 1 }}  // EmptyState centrado
/>
```

## 8. Performance y Optimización

- **FlatList sobre ScrollView**: Siempre para listas de más de ~20 items. Usa `getItemLayout` si los
  items tienen altura fija para evitar cálculos dinámicos.
- **React.memo**: Envuelve componentes de lista para evitar re-renders innecesarios.
- **useCallback / useMemo**: Para handlers y datos derivados pasados como props.
- **Imágenes**: Usa `react-native-fast-image` para caching agresivo. Precarga imágenes críticas.
  Especifica siempre width/height para evitar layout jumps.
- **Hermes**: Asegúrate de que Hermes está habilitado (default en RN 0.70+).
- **Evita inline styles en listas**: `StyleSheet.create()` se ejecuta una vez, objetos inline
  se re-crean en cada render.

```tsx
// Optimización de FlatList
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={keyExtractor}
  removeClippedSubviews={true}        // Desmonta items fuera de viewport
  maxToRenderPerBatch={10}            // Items por batch de render
  windowSize={5}                       // Ventana de render (5 = 2 antes + visible + 2 después)
  initialNumToRender={10}             // Items iniciales
  getItemLayout={(data, index) => ({  // Skip measurement si items son fijos
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

## 9. Accesibilidad

```tsx
// Touch targets mínimos
const styles = StyleSheet.create({
  touchable: {
    minHeight: 48,
    minWidth: 48,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

// Labels y roles
<TouchableOpacity
  style={styles.touchable}
  onPress={onDelete}
  accessibilityLabel={`Eliminar ${item.title}`}
  accessibilityRole="button"
  accessibilityHint="Toca dos veces para eliminar este elemento"
>
  <Icon name="trash" size={24} />
</TouchableOpacity>

// Estados dinámicos
<View
  accessibilityRole="alert"
  accessibilityLiveRegion="polite"
>
  <Text>{statusMessage}</Text>
</View>

// Agrupación
<View accessible={true} accessibilityLabel={`${item.title}, ${item.subtitle}, ${item.status}`}>
  <Text>{item.title}</Text>
  <Text>{item.subtitle}</Text>
  <Badge status={item.status} />
</View>

// Font scaling — NO uses heights fijas en texto
const styles = StyleSheet.create({
  textContainer: {
    minHeight: 44,      // minHeight, no height
    justifyContent: 'center',
    paddingVertical: 8, // padding para acomodar texto escalado
  },
});
```

## 10. Patrones Avanzados

### Formulario con validación

```tsx
import { useForm, Controller } from 'react-hook-form';

const MyForm: React.FC = () => {
  const { colors, spacing } = useTheme();
  const { control, handleSubmit, formState: { errors } } = useForm({
    defaultValues: { email: '', phone: '' }
  });

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={{ flex: 1 }}
    >
      <ScrollView
        contentContainerStyle={{ padding: spacing.md }}
        keyboardShouldPersistTaps="handled"
      >
        <Controller
          control={control}
          name="email"
          rules={{
            required: 'Email es requerido',
            pattern: { value: /^\S+@\S+\.\S+$/, message: 'Email no válido' }
          }}
          render={({ field: { onChange, onBlur, value } }) => (
            <View style={{ marginBottom: spacing.md }}>
              <Text style={styles.label}>Email</Text>
              <TextInput
                style={[
                  styles.input,
                  { borderColor: errors.email ? colors.danger : colors.border }
                ]}
                onBlur={onBlur}
                onChangeText={onChange}
                value={value}
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
                textContentType="emailAddress"
                accessibilityLabel="Email"
              />
              {errors.email && (
                <Text style={[styles.errorText, { color: colors.danger }]}>
                  {errors.email.message}
                </Text>
              )}
            </View>
          )}
        />

        <TouchableOpacity
          style={[styles.submitButton, { backgroundColor: colors.primary }]}
          onPress={handleSubmit(onSubmit)}
          accessibilityRole="button"
        >
          <Text style={styles.submitText}>Guardar</Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};
```

### Gestión de estado de red

```tsx
import NetInfo from '@react-native-community/netinfo';

const useNetworkStatus = () => {
  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsConnected(state.isConnected ?? true);
    });
    return unsubscribe;
  }, []);

  return isConnected;
};

// Banner de offline
const OfflineBanner: React.FC = () => {
  const isConnected = useNetworkStatus();
  const { colors } = useTheme();

  if (isConnected) return null;

  return (
    <Animated.View
      entering={FadeInDown.duration(200)}
      exiting={FadeInDown.duration(200)}
      style={[styles.banner, { backgroundColor: colors.warning }]}
      accessibilityRole="alert"
    >
      <Icon name="cloud-offline-outline" size={16} />
      <Text style={styles.bannerText}>Sin conexión. Los cambios se guardarán localmente.</Text>
    </Animated.View>
  );
};
```
