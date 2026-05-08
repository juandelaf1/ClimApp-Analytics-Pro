# 🌤️ ClimApp-Analytics-Pro

API REST de clima en tiempo real para España. Datos oficiales de AEMET, geolocalización automática.

---

## ⚡ Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (.env)
AEMET_API_KEY=tu_api_key
SECRET_KEY=tu_clave

# Ejecutar
python app.py
```

---

## 📡 API Endpoints

| Endpoint | Descripción | Ejemplo |
|----------|-------------|---------|
| `/api/clima` | Clima por coordenadas o IP | `?lat=40.41&lon=-3.70` |
| `/api/clima/<ciudad>` | Clima por ciudad | `/api/clima/Madrid` |
| `/api/geo/<ciudad>` | Geocodificar ciudad | `/api/geo/Barcelona` |
| `/api/health` | Estado del servidor | - |
| `/api/stats` | Estadísticas | - |
| `/api/alertas` | Configuración alertas | - |

---

## ✨ Características

- **Datos oficiales**: AEMET OpenData (85+ estaciones meteorológicas)
- **Geolocalización automática**: IP-API.com + Nominatim
- **Alertas configurables**: 6 niveles (extremo, alto, medio)
- **Rate Limiting**: 30 req/min para /clima, 10 req/min para /geo
- **Caché offline**: 30 minutos
- **Búsqueda de estación**: Haversine hasta 50km

---

## 🔧 Configuración

Variables de entorno en `.env`:
```
AEMET_API_KEY=          # Clave de AEMET OpenData
SECRET_KEY=             # Clave secreta Flask
AEMET_TIMEOUT=20       # Timeout en segundos
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 📂 Estructura

```
ClimApp-Analytics-Pro/
├── app.py                 # Gateway principal
├── services/             # Lógica de negocio
├── controllers/           # Controladores Flask
├── repositories/         # Persistencia
├── models/                # Modelos de datos
├── templates/             # Plantillas HTML
├── static/                # CSS, JS
├── config/                # Configuración
└── tests/                 # Tests
```

---

## 📄 Licencia

MIT © 2026 Juan de la Fuente