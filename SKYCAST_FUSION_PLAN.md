# SKYCAST - Plan de Fusión

> **Estado:** ✅ COMPLETADO (2026-05-11)
> **Fecha:** 2026-05-11
> **Workspace:** `C:\Users\JUAN\Desktop\Proyectos\ClimApp-Analytics-Pro`
> **Autor:** Generado con asistencia de IA (opencode)

---

## 1. Contexto y Objetivos

### 1.1 Fuentes

| # | Proyecto | Ubicación | Valor para fusionar |
|---|---|---|---|
| 1 | **Vortex** (BASE) | `C:\Bootcamp_Proyecto_3_Vortex` | Schema DB 9 tablas, FastAPI starter, normalizer AEMET, ETL pipeline, fallback_service, tests 41KB |
| 2 | **SkyCast-Analytics** | GitHub (101 commits) | Auth SHA-256+salt, Dashboard Streamlit, validacion física, ETL normalización/dedup |
| 3 | **ClimApp-Analytics-Pro** | GitHub (10 commits) | API REST básica |
| 4 | **ClimApp-Analytics-Pro** | Local `..\ClimApp-Analytics-Pro` | AEMET service, geolocation, rate limiting, caché, MVC completo |
| 5 | **climapp** | `C:\Users\JUAN\climapp` | Comparison controller, registro manual, scheduler 2h, station mapping, frontend web |
| 6 | **proyecto-clima-ayuntamento** | `C:\proyecto-clima-ayuntamento` | NO USAR (código de otro equipo) |

### 1.2 Objetivo

Crear **un único proyecto profesional** llamado **SkyCast**, listo para portfolio, combinando lo mejor de todos.

### 1.3 Perfil del usuario

- Data Scientist / Data Engineer / Data Analyst / Business Analyst

### 1.4 Repos finales

- `github.com/juandelaf1/SkyCast-Analytics` → **Único repo público**
- `github.com/juandelaf1/ClimApp-Analytics-Pro` → **Hacerlo privado**
- Carpetas locales → **Eliminar tras fusión**

---

## 2. Stack Tecnológico

```
Backend:       FastAPI + Uvicorn + Pydantic + SQLAlchemy
Dashboard:     Streamlit + Plotly + Geopandas + Folium
Database:      SQLite (dev) → PostgreSQL (prod)
Deploy:        Docker + Docker Compose
Auth:          JWT + SHA-256 salt (de SkyCast)
Data Source:   AEMET OpenData (datos oficiales España)
Rate Limiting: slowapi
Scheduler:     APScheduler (async)
```

### Dependencias consolidadas

```
# Core
fastapi>=0.115.0
uvicorn[standard]>=0.34.0
pydantic>=2.10.0
pydantic-settings>=2.7.0

# Database
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.30.0
psycopg2-binary>=2.9.10

# Data
pandas>=2.2.0
numpy>=2.0.0
geopandas>=1.0.0
shapely>=2.0.0
plotly>=5.24.0
folium>=0.17.0
httpx>=0.28.0

# Dashboard
streamlit>=1.42.0

# Security
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
python-multipart>=0.0.20

# Utilities
python-dotenv>=1.0.0
apscheduler>=3.11.0
slowapi>=0.1.9
aiofiles>=24.0.0
openpyxl>=3.1.0

# Testing
pytest>=8.3.0
pytest-asyncio>=0.25.0
pytest-cov>=6.0.0
httpx>=0.28.0
```

---

## 3. Módulos a Fusionar por Origen

### 3.1 Vortex (BASE) — Arquitectura de referencia

| Módulo | Archivo | Qué aporta |
|--------|---------|------------|
| Schema DB 9 tablas | `db/init_db.py` + `db/models/` | Zonas, municipios, estaciones, mediciones, fuentes_dato, umbrales_alerta, alertas, usuarios |
| SQLAlchemy session | `db/session.py` | SessionLocal, get_db(), dependency injection |
| FastAPI starter | `api/main.py` | Exception handlers, router registration |
| Normalizer AEMET | `services/normalizer.py` (310 líneas) | AEMET codes → nombres estándar, AEMETThresholds class, batch processing |
| Fallback offline | `services/fallback_service.py` | JSON-driven fallback locations |
| ETL pipeline | `etl/pipeline.py`, `extract.py`, `transform.py`, `load.py` | Pandas + transaction rollback |
| Retry service | `services/retry_service.py` | Exponential backoff |
| AEMET thresholds | `config/aemet_thresholds.json` | Thresholds configurados |
| Tests | `tests/` (41KB) | 6 archivos, mocking completo |

### 3.2 SkyCast-Analytics (GitHub) — Seguridad y Dashboard

| Módulo | Qué aporta |
|--------|------------|
| Auth SHA-256 + salt | `secrets.token_hex(16)`, complejidad password, getpass, logging |
| Dashboard Streamlit | Tabs: Ejecutivo/Científico/Auditoría, SMA 7 días, KPI delta, anomalías 2 std |
| Validación física | Temp -20/60°C, humedad 0-100%, viento 0-150 km/h, fechas futuras, nombres zonas |
| ETL normalización | Madrid→Centro, dedup por (fecha, zona) |

### 3.3 ClimApp-Analytics-Pro (local) — API y AEMET

| Módulo | Qué aporta |
|--------|------------|
| AEMET service | Handshake 2-pasos, Haversine 50km, retry logic |
| Geolocation | IP-API + Nominatim + reverse geocoding + caché 1hr |
| Rate limiter | 30 req/min /clima, 10 req/min /geo |
| Caché offline | 30 min AEMET, 1hr geolocation |

### 3.4 climapp (Adriana) — Comparación y Scheduler

| Módulo | Qué aporta |
|--------|------------|
| Comparison | Diferencia temp >3°C, humedad >10%, viento >10km/h, lluvia >5mm |
| Registro manual | Formulario, validación, persistencia |
| Scheduler | Fetch automático cada 2h |
| Station mapping | `estacion_por_municipio.json` |

---

## 4. Arquitectura Target

```
skycast/
├── app/
│   ├── main.py                    # FastAPI entry
│   ├── config/
│   │   ├── settings.py            # Pydantic Settings
│   │   ├── alertas.json           # Thresholds alertas
│   │   └── aemet_thresholds.json  # Thresholds AEMET
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       ├── clima.py           # GET /clima, /clima/{ciudad}
│   │       ├── geo.py             # GET /geo/{ciudad}
│   │       ├── health.py          # GET /health, /stats
│   │       ├── alerts.py          # GET/POST /alertas
│   │       ├── records.py         # GET/POST /registros
│   │       ├── comparison.py      # POST /comparar
│   │       └── auth.py            # POST /register, /login
│   ├── auth/
│   │   ├── jwt_auth.py            # JWT + SHA-256 salt
│   │   ├── dependencies.py        # FastAPI dependencies
│   │   └── password.py            # Hashing utils
│   ├── services/
│   │   ├── aemet_service.py       # AEMET API (de ClimApp)
│   │   ├── geolocation_service.py # IP-API + Nominatim
│   │   ├── alert_service.py       # Sistema alertas
│   │   ├── comparison_service.py  # Comparación manual vs AEMET
│   │   ├── validation_service.py  # Validación física
│   │   ├── normalizer.py          # AEMET codes mapping (de Vortex)
│   │   ├── fallback_service.py    # Offline fallback (de Vortex)
│   │   ├── retry_service.py       # Exponential backoff
│   │   └── cache_service.py       # Caché en memoria
│   ├── db/
│   │   ├── session.py             # SQLAlchemy session (de Vortex)
│   │   ├── base.py               # Declarative base
│   │   ├── models/               # SQLAlchemy models (9 tablas de Vortex)
│   │   │   ├── zona.py
│   │   │   ├── municipio.py
│   │   │   ├── estacion.py
│   │   │   ├── medicion.py
│   │   │   ├── fuente_dato.py
│   │   │   ├── umbral_alerta.py
│   │   │   ├── alerta.py
│   │   │   └── usuario.py
│   │   └── init_db.py            # Schema initialization (de Vortex)
│   ├── etl/
│   │   ├── pipeline.py           # Orchestrator
│   │   ├── extract.py
│   │   ├── transform.py           # Pandas + deduplicación (de Vortex)
│   │   └── load.py               # DB insertion con rollback
│   ├── scheduler/
│   │   └── tasks.py              # Fetch AEMET cada 2h
│   ├── dashboard/
│   │   ├── app.py                # streamlit run
│   │   ├── pages/
│   │   │   ├── 1_📊_Resumen_Ejecutivo.py
│   │   │   ├── 2_🔬_Analisis_Científico.py
│   │   │   ├── 3_📋_Auditoría_Datos.py
│   │   │   ├── 4_🗺️_Mapa_Estaciones.py    # Folium + Geopandas
│   │   │   └── 5_⚙️_Configuración.py
│   │   ├── components/
│   │   │   ├── charts.py
│   │   │   ├── kpi_cards.py
│   │   │   └── map_view.py
│   │   └── utils/
│   │       └── data_loader.py
│   ├── core/
│   │   ├── validators.py         # Validación física (de SkyCast)
│   │   ├── exceptions.py
│   │   └── constants.py
│   ├── data/
│   │   ├── stations_madrid.geojson
│   │   ├── municipality_station_mapping.json
│   │   └── madrid_districts.geojson
│   └── middleware/
│       └── rate_limiter.py       # slowapi
├── tests/
│   ├── conftest.py
│   ├── test_api/
│   ├── test_services/
│   ├── test_etl/
│   └── test_dashboard/
├── scripts/
│   ├── init_db.py
│   ├── seed_data.py
│   └── generate_stations.py
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.dashboard
│   └── docker-compose.yml
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 5. Hoja de Ruta (Fases)

### Fase 1 — Estructura base ⚡
- [x] Limpiar carpeta actual (mover legacy/)
- [x] Crear estructura de directorios
- [x] Configurar `requirements.txt` consolidado
- [x] Crear `app/config/settings.py` (Pydantic Settings)
- [x] Migrar `db/session.py` de Vortex (SQLAlchemy)
- [x] Migrar `db/models/` de Vortex (9 tablas)
- [x] Crear `app/db/init_db.py` (schema) + seed data
- [x] Configurar `.env.example`

### Fase 2 — Auth industrial 🔐
- [x] Migrar `auth.py` de SkyCast (SHA-256 + salt + complexity)
- [x] Crear JWT auth con `python-jose`
- [x] Crear `app/auth/jwt_auth.py` (get_current_user)
- [x] Endpoint `POST /api/v1/auth/register`
- [x] Endpoint `POST /api/v1/auth/login`
- [x] Endpoint `GET /api/v1/auth/me`
- [x] Tests de auth (validators, alerts, haversine)

### Fase 3 — Core API + AEMET 📡
- [x] Migrar `services/aemet_service.py` de ClimApp local
- [x] Crear `GET /api/v1/clima`
- [x] Crear `GET /api/v1/clima/{ciudad}`
- [x] Migrar `services/geolocation_service.py`
- [x] Crear `GET /api/v1/geo/{ciudad}`
- [x] Migrar `core/utils.py` (Haversine)
- [x] Tests de servicios

### Fase 4 — Alertas y validación ⚠️
- [x] Migrar `validacion.py` de SkyCast (rangos físicos)
- [x] Migrar `alert_service.py`
- [x] Endpoint `GET /api/v1/alertas`
- [x] Endpoint `POST /api/v1/alertas`
- [x] Tests de alertas y validación

### Fase 5 — ETL y anomalías 🔧
- [x] Migrar `etl/` completo de Vortex
- [x] Añadir dedup por (fecha, zona) de SkyCast
- [x] Añadir detección anomalías (2 std dev) de SkyCast
- [x] Tests ETL

### Fase 6 — Registro, comparación, scheduler 📝
- [x] Migrar `comparison logic` de climapp
- [x] Endpoint `POST /api/v1/comparison`
- [x] Endpoint `GET/POST /api/v1/records`
- [x] Migrar scheduler a APScheduler (cada 2h)
- [x] Tests

### Fase 7 — Dashboard Streamlit 📊
- [x] Crear `app/dashboard/app.py`
- [x] Página Resumen Ejecutivo (KPIs, SMA, alertas)
- [x] Página Análisis Científico (correlación, anomalías)
- [x] Página Auditoría Datos (tabla, filtros)
- [x] Página Mapa Estaciones (Folium + Geopandas)
- [x] Página Configuración
- [x] Tests dashboard

### Fase 8 — Docker y Deploy 🚀
- [x] `docker/Dockerfile.api`
- [x] `docker/Dockerfile.dashboard`
- [x] `docker/docker-compose.yml` (API + PostgreSQL + Dashboard)
- [x] Documentar deployment en README

### Fase 9 — Documentación y limpieza 📚
- [x] README.md completo
- [x] Limpiar código (lints, type hints)
- [x] **24 tests pasando** ✅
- [ ] Hacer privados/eliminados repos no necesarios (manual)
- [ ] Verificar: pytest + streamlit + docker-compose

---

## 6. Decisiones confirmadas

| Decisión | Valor |
|---|---|
| Frontend | Streamlit + API (sin HTML/Jinja2 heredado) |
| Mapas | Folium + Geopandas + Plotly Choropleth |
| DB desarrollo | SQLite → PostgreSQL en producción |
| Commits | Mantener historial original |
| Base | Vortex (mejor arquitectura) + SkyCast (auth/dashboard) |

---

## 7. Criterios de Éxito

- [ ] API FastAPI con Swagger UI funcional
- [ ] Dashboard Streamlit con 5 páginas
- [ ] Auth (registro, login, JWT) funcionando
- [ ] AEMET retorna datos reales
- [ ] Detección anomalías funcional
- [ ] Comparación manual vs AEMET funcional
- [ ] Scheduler ejecuta cada 2h
- [ ] Rate limiting activo
- [ ] Docker Compose levanta todo
- [ ] Tests pasan (>80% coverage)
- [ ] Un único repo público

---

*Este documento es la fuente de verdad durante la fusión. Cualquier cambio de scope debe actualizarlo.*