# SKYCAST - Contexto, Skills y Agentes

> Archivo de referencia para IA durante la producción de SkyCast
> Generado: 2026-05-11

---

## 🎯 Identidad del Proyecto

**Nombre:** SkyCast — Enterprise Climate Intelligence Platform
**Descripción:** Plataforma de monitorización climática para España con datos oficiales de AEMET, analytics avanzado, dashboard BI y alertas inteligentes.
**Stack:** FastAPI + Streamlit + PostgreSQL + Docker + Geopandas + Folium + Plotly
**Perfil:** Data Scientist / Data Engineer / Data Analyst / Business Analyst

---

## 📁 Archivos de referencia

- `SKYCAST_FUSION_PLAN.md` — Hoja de ruta completa
- `C:\Bootcamp_Proyecto_3_Vortex` — BASE arquitectónica (Vortex)
- `C:\Users\JUAN\climapp` — Reference: comparison, scheduler, frontend
- GitHub `juandelaf1/SkyCast-Analytics` — Reference: auth SHA-256+salt, dashboard Streamlit
- `C:\Users\JUAN\Desktop\Proyectos\ClimApp-Analytics-Pro` — Workspace actual

---

## 🏗️ Arquitectura de referencia

### De Vortex (BASE) — Usar como template

```
db/session.py        → SQLAlchemy SessionLocal, get_db() generator
db/init_db.py        → Schema 9 tablas con FK e índices
db/models/           → 9 modelos ORM SQLAlchemy (zona, municipio, estacion, medicion, fuente_dato, umbral_alerta, alerta, usuario)
api/main.py          → FastAPI starter con exception handlers
services/normalizer.py → AEMET codes mapping, AEMETThresholds class (310 líneas)
services/fallback_service.py → JSON-driven offline fallback
services/retry_service.py → Exponential backoff (urllib3)
etl/pipeline.py      → Orchestrator con timing
etl/transform.py     → Pandas data cleaning
etl/load.py          → DB insertion con transaction rollback
config/aemet_thresholds.json → Thresholds configurados AEMET
tests/               → 6 archivos, mocking con FakeResponse, Monkeypatch
```

### De SkyCast-Analytics — Copiar/adaptar

```
auth.py              → SHA-256 + salt único (secrets.token_hex), complejidad password
validacion.py        → Rangos físicos: temp -20/60°C, humedad 0-100%, viento 0-150 km/h
app_visual.py        → Dashboard Streamlit: tabs, SMA 7 días, KPI delta, anomalías 2 std
```

### De ClimApp-Analytics-Pro (local) — Copiar/adaptar

```
services/aemet_service.py     → AEMET handshake, Haversine 50km
services/geolocation_service.py → IP-API + Nominatim + reverse geocoding
services/rate_limiter.py      → 30 req/min /clima, 10 req/min /geo
config/alertas.json           → Thresholds alertas configurables
```

### De climapp (Adriana) — Copiar/adaptar

```
controllers/compare_controller.py → Comparación manual vs AEMET
controllers/manual_controller.py → Registro manual de datos
controllers/scheduler_controller.py → Scheduler cada 2h (migrar a APScheduler)
repositories/json_repository.py   → Persistencia JSON funcional
static/js/estacion_por_municipio.json → Mapping municipio→estación
```

---

## 🔑 Reglas de producción

### 1. Estructura de archivos
- Toda la aplicación va en `app/`
- Dashboard va en `app/dashboard/`
- Tests van en `tests/`
- Scripts de utilidad en `scripts/`
- Docker files en `docker/`

### 2. Nomenclatura
- **Módulos Python:** `snake_case`
- **Clases:** `PascalCase`
- **Constantes:** `UPPER_SNAKE_CASE`
- **Variables y funciones:** `snake_case`
- **Endpoints API:** `snake_case` (ej: `/api/v1/clima`)
- **Métricas/tags:** `camelCase` (ej: `temperaturaMax`)

### 3. Imports
```python
# Estructura de imports
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
import pandas as pd
```

### 4. Validación de datos
- Usar **Pydantic** para todos los DTOs request/response
- Usar `validacion.py` (de SkyCast) para validación física
- Rangos: temp [-20, 60]°C, humedad [0, 100]%, viento [0, 150]km/h, lluvia >= 0
- No permitir fechas futuras
- Nombres de zona: sin dígitos, estandarizados

### 5. Base de datos
- Usar **SQLAlchemy** con el schema de Vortex (9 tablas)
- SQLite para desarrollo local
- PostgreSQL para producción (Docker)
- Siempre usar `get_db()` dependency injection
- Índices en columnas de búsqueda frecuente

### 6. API REST (FastAPI)
- Versionar: `/api/v1/`
- Usar `APIRouter` para agrupar endpoints
- Documentación automática con OpenAPI
- Validación automática con Pydantic
- Manejo de errores con `HTTPException`
- Rate limiting con `slowapi`

### 7. Auth
- Hash: **SHA-256 + salt único** por usuario (de SkyCast)
- Tokens: **JWT** con `python-jose`
- Dependency: `get_current_user` para endpoints protegidos
- Registrar: email regex + password complexity (8+ chars, upper, lower, digit)

### 8. Dashboard (Streamlit)
- Usar `st.cache_data` para caching pesado
- Conectar a API via `httpx` async
- Gráficos: **Plotly** (no matplotlib)
- Mapas: **Folium** con marcadores de estaciones + **Geopandas** para análisis
- Choropleth con GeoJSON de distritos Madrid

### 9. Geoespacial
- Fórmula **Haversine** para distancia entre coordenadas
- Buscar estación más cercana en radio 50km (fallback 100km)
- GeoJSON para estaciones y distritos
- Geopandas GeoDataFrame con CRS 4326

### 10. AEMET API
- Handshake 2-pasos: get URL → fetch data
- Retry con exponential backoff (de Vortex)
- Caché: 30 min para datos, 1 hr para geocoding
- Fallback offline (de Vortex)

### 11. Tests
- Usar `pytest` con fixtures
- Mockear llamadas HTTP con clases FakeResponse
- Testear: servicios, endpoints API, ETL, validators
- Coverage mínimo 80% en core modules

### 12. Docker
- Imagen ligera (alpine si posible)
- Multi-stage build para producción
- docker-compose con: api, dashboard, postgres
- Variables de entorno para configuración
- No hardcodear credenciales

---

## 📋 Checklist de calidad por módulo

### Antes de marcar una fase como completa:

- [ ] Todos los tests pasan (`pytest -v`)
- [ ] Type hints en todas las funciones públicas
- [ ] Docstrings en clases y funciones principales
- [ ] No hardcoded secrets (todo en .env)
- [ ] Error handling en todas las operaciones I/O
- [ ] Logging en puntos críticos
- [ ] Validación Pydantic en todos los endpoints
- [ ] Índices de base de datos creados si hay nuevas tablas
- [ ] .env.example actualizado si hay nuevas variables

---

## 🚫 No hacer

- **NO** usar Flask para la API (usar FastAPI)
- **NO** hardcodear thresholds (usar JSON config)
- **NO** hacer commits con secrets o API keys
- **NO** usar datos de OpenWeather (usar AEMET)
- **NO** mezclar código de otros equipos sin referencia
- **NO** hacer refactorizaciones grandes sin tests
- **NO** ignorar errores silenciosamente (siempre log o raise)

---

## 🗺️ Roadmap de fases

| Fase | Módulo | Prioridad | Dependencias |
|---|---|---|---|
| 1 | Estructura base + DB | 🔴 Alta | Ninguna |
| 2 | Auth industrial | 🔴 Alta | Fase 1 |
| 3 | Core API + AEMET | 🔴 Alta | Fase 1 |
| 4 | Alertas + validación | 🟡 Media | Fase 3 |
| 5 | ETL + anomalías | 🟡 Media | Fase 4 |
| 6 | Registro + comparación + scheduler | 🟡 Media | Fase 3-4 |
| 7 | Dashboard Streamlit | 🟡 Media | Fase 3 |
| 8 | Docker + Deploy | 🟢 Baja | Fase 7 |
| 9 | Documentación + limpieza | 🟢 Baja | Todas |

---

## 📞 Patrones de referencia rápida

### FastAPI endpoint pattern
```python
@router.get("/clima", response_model=WeatherResponse)
async def get_clima(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # lógica
    pass
```

### SQLAlchemy model pattern (de Vortex)
```python
class Estacion(Base):
    __tablename__ = "estaciones"
    id = Column(Integer, primary_key=True, index=True)
    idema = Column(String(10), unique=True, index=True)
    nombre = Column(String(200), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    municipio_id = Column(Integer, ForeignKey("municipios.id"))
```

### AEMET service pattern (de ClimApp local)
```python
async def get_weather(latitude, longitude):
    # 1. Encontrar estación más cercana (Haversine)
    # 2. Request a AEMET para obtener URL temporal
    # 3. Segundo request para obtener datos
    # 4. Normalizar con normalizer.py
    # 5. Aplicar alertas
    # 6. Guardar en DB
    # 7. Retornar respuesta
```

### Streamlit dashboard pattern (de SkyCast)
```python
st.set_page_config(page_title="SkyCast", page_icon="🌦️")
st.title("SkyCast - Resumen Ejecutivo")
# KPIs con st.metric(delta=...)
# Gráficos con st.plotly_chart(fig)
# Tablas con st.dataframe(df)
```

### Auth pattern (de SkyCast)
```python
def _hash_password(password, salt):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

salt = secrets.token_hex(16)  # único por usuario
```

### ETL pattern (de Vortex)
```python
# extract → transform (pandas) → load (SQLAlchemy con rollback)
def run_pipeline():
    data = extract("data/registros.json")
    df = transform(data)
    load(df, session)
```

### Geopandas + Folium pattern
```python
gdf = geopandas.GeoDataFrame(stations, geometry=geopandas.points_from_xy(lon, lat), crs="EPSG:4326")
m = gdf.explore(column="temperatura", cmap="RdYlBu_r")
```

---

*Este archivo es la referencia de contexto para la IA durante toda la producción.*
*Mantener actualizado si hay cambios de arquitectura o decisiones.*