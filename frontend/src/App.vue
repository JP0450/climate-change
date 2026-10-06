<script setup>
import { computed, onMounted, ref } from "vue";
import {
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  Bell,
  ChartNoAxesCombined,
  CloudSun,
  Droplets,
  Globe2,
  Leaf,
  MapPin,
  Menu,
  Wind,
  X,
} from "lucide-vue-next";

const dashboard = ref(null);
const loading = ref(true);
const error = ref("");
const activeNav = ref("Resumen");
const menuOpen = ref(false);
const todayLabel = new Intl.DateTimeFormat("es-CO", {
  weekday: "long",
  day: "2-digit",
  month: "long",
}).format(new Date()).toUpperCase();

const navItems = [
  { label: "Resumen", icon: ChartNoAxesCombined },
  { label: "Clima", icon: CloudSun },
  { label: "Calidad del aire", icon: Wind },
  { label: "Agua", icon: Droplets },
];

const bars = computed(() => {
  const values = dashboard.value?.weekly_emissions ?? [];
  const max = Math.max(...values.map((item) => item.value), 1);
  return values.map((item) => ({
    ...item,
    height: `${Math.max((item.value / max) * 100, 12)}%`,
  }));
});

async function loadDashboard() {
  loading.value = true;
  error.value = "";
  try {
    const response = await fetch("/api/dashboard");
    if (!response.ok) {
      throw new Error(`La API respondió con estado ${response.status}.`);
    }
    dashboard.value = await response.json();
  } catch (cause) {
    error.value = cause instanceof Error
      ? cause.message
      : "No fue posible cargar el panel climático.";
  } finally {
    loading.value = false;
  }
}

onMounted(loadDashboard);
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar" :class="{ 'sidebar-open': menuOpen }">
      <a class="brand" href="#" aria-label="Climatic, inicio">
        <span class="brand-mark"><Leaf :size="21" :stroke-width="2.2" /></span>
        <span>climatic<span class="brand-period">.</span></span>
      </a>

      <div class="workspace-label">TU ESPACIO</div>
      <nav class="side-nav" aria-label="Navegación principal">
        <button
          v-for="item in navItems"
          :key="item.label"
          class="nav-item"
          :class="{ 'nav-item-active': activeNav === item.label }"
          @click="activeNav = item.label; menuOpen = false"
        >
          <component :is="item.icon" :size="18" :stroke-width="1.8" />
          <span>{{ item.label }}</span>
          <span v-if="item.label === 'Clima'" class="nav-live"></span>
        </button>
      </nav>

      <div class="sidebar-bottom">
        <div class="sidebar-note">
          <div class="note-icon"><Globe2 :size="17" /></div>
          <p>El planeta no necesita un puñado de personas perfectas.</p>
          <span>Necesita millones haciendo lo mejor que pueden.</span>
        </div>
        <button class="profile-button">
          <span class="avatar">Y</span>
          <span class="profile-copy"><strong>Tu espacio</strong><small>Plan personal</small></span>
          <span class="profile-menu">···</span>
        </button>
      </div>
    </aside>

    <main class="main-content">
      <header class="topbar">
        <button
          class="mobile-menu icon-button"
          :aria-label="menuOpen ? 'Cerrar menú' : 'Abrir menú'"
          @click="menuOpen = !menuOpen"
        >
          <X v-if="menuOpen" :size="19" />
          <Menu v-else :size="19" />
        </button>
        <div class="breadcrumb">Tu espacio <span>/</span> <strong>{{ activeNav }}</strong></div>
        <div class="topbar-actions">
          <span class="live-status"><span></span> Datos en vivo</span>
          <button class="icon-button notification-button" aria-label="Notificaciones">
            <Bell :size="18" />
            <i></i>
          </button>
          <span class="top-avatar">Y</span>
        </div>
      </header>

      <div v-if="loading" class="state-message" role="status">
        <span class="loader"></span>
        Cargando tu resumen climático...
      </div>
      <div v-else-if="error" class="state-message error-message" role="alert">
        <div>
          <strong>No pudimos conectar con Climatic</strong>
          <span>{{ error }} Comprueba que la API esté activa e inténtalo de nuevo.</span>
        </div>
        <button class="retry-button" @click="loadDashboard">Reintentar</button>
      </div>

      <template v-else-if="dashboard">
        <section class="welcome-section">
          <div>
            <div class="eyebrow"><span class="eyebrow-line"></span> {{ todayLabel }}</div>
            <h1>El planeta, <span>en perspectiva.</span></h1>
            <p class="welcome-copy">Entiende lo que pasa hoy. Inspira lo que puede pasar mañana.</p>
          </div>
          <button class="location-pill">
            <MapPin :size="15" />
            {{ dashboard.location }}
            <span class="location-chevron">⌄</span>
          </button>
        </section>

        <section class="metrics-grid" aria-label="Indicadores ambientales">
          <article
            v-for="metric in dashboard.metrics"
            :key="metric.id"
            class="metric-card"
          >
            <div class="metric-topline">
              <span>{{ metric.label }}</span>
              <span class="metric-icon">
                <CloudSun v-if="metric.icon === 'temperature'" :size="18" />
                <Wind v-else-if="metric.icon === 'air'" :size="18" />
                <Globe2 v-else :size="18" />
              </span>
            </div>
            <div class="metric-value">{{ metric.value }}<small>{{ metric.unit }}</small></div>
            <div class="metric-foot">
              <span class="metric-change" :class="`trend-${metric.trend}`">
                <ArrowDownRight v-if="metric.trend === 'down' || metric.trend === 'good'" :size="15" />
                <ArrowUpRight v-else :size="15" />
                {{ metric.change }}
              </span>
              <span v-if="metric.trend !== 'good'" class="metric-context">vs. ayer</span>
              <span v-else class="metric-context">en este momento</span>
            </div>
          </article>
        </section>

        <section class="insights-grid">
          <article class="chart-card">
            <div class="card-heading">
              <div>
                <div class="section-kicker">TU IMPACTO</div>
                <h2>Emisiones de CO₂</h2>
              </div>
              <button class="period-select">Esta semana <span>⌄</span></button>
            </div>
            <div class="chart-summary">
              <strong>{{ dashboard.emissions.value }}<small>{{ dashboard.emissions.unit }}</small></strong>
              <span><ArrowDownRight :size="15" /> {{ dashboard.emissions.change }} <small>vs. semana anterior</small></span>
            </div>
            <div class="chart" role="img" aria-label="Gráfico de emisiones durante la semana">
              <div class="chart-grid-lines"><i></i><i></i><i></i><i></i></div>
              <div v-for="bar in bars" :key="bar.day" class="bar-column">
                <div class="bar-track">
                  <div class="bar" :class="{ 'bar-highlight': bar.day === 'Jue' }" :style="{ height: bar.height }"></div>
                </div>
                <span>{{ bar.day }}</span>
              </div>
            </div>
            <div class="chart-footer"><span><i></i> Huella de carbono</span><span>Fuente: estimación personal</span></div>
          </article>

          <article class="insight-card">
            <div class="insight-orbit orbit-one"></div>
            <div class="insight-orbit orbit-two"></div>
            <div class="insight-content">
              <div class="insight-badge"><Leaf :size="15" /> INSIGHT DE LA SEMANA</div>
              <div class="insight-illustration"><Globe2 :size="29" :stroke-width="1.3" /></div>
              <h2>{{ dashboard.insight.title }}</h2>
              <p>{{ dashboard.insight.description }}</p>
              <a href="#" class="insight-link">Descubre cómo <ArrowRight :size="15" /></a>
            </div>
            <div class="insight-decoration">↗</div>
          </article>
        </section>

        <section class="bottom-banner">
          <div class="banner-icon"><Leaf :size="18" /></div>
          <p><strong>Cada dato cuenta.</strong> Sigue explorando y descubre cómo tus acciones se conectan con el planeta.</p>
          <span class="banner-weather"><CloudSun :size="17" /> Un buen día para empezar</span>
        </section>

        <footer class="page-footer">
          <span>Mostrando datos actualizados {{ dashboard.updated_at.toLowerCase() }}</span>
          <span>Hecho para un futuro más verde <span class="footer-heart">♥</span></span>
        </footer>
      </template>
    </main>
  </div>
</template>
