# 🌤️ ClimApp-Analytics-Pro

> API REST de clima en tiempo real para España. Datos oficiales de AEMET, geolocalización automática.

---

## 🚀 Uso Rápido

```bash
# Iniciar servidor
python app.py

# Endpoints base
http://localhost:5000
```

---

## 📡 API Endpoints

| Endpoint | Descripción | Ejemplo |
|----------|--------------|---------|
| `/api/clima` | Clima por coordenadas o IP | `?lat=40.41&lon=-3.70` |
| `/api/clima/<ciudad>` | Clima por ciudad | `/api/clima/Madrid` |
| `/api/geo/<ciudad>` | Geocodificar ciudad | `/api/geo/Barcelona` |
| `/api/health` | Estado del servidor | - |
| `/api/alertas` | Configuración de alertas | - |

---

## 📋 Características

- **Datos oficiales**: AEMET OpenData (85+ estaciones)
- **Geolocalización**: IP automática + Nominatim
- **Alertas**: Configurables desde JSON
- **Rate Limiting**: 30 req/min protección
- **Caché**: 30 minutos offline

---

## ⚙️ Configuración

Crear `.env`:
```
AEMET_API_KEY=tu_api_key_aemet
SECRET_KEY=clave_secreta
```

---

## 📄 Licencia

MIT © 2026 Juan de la Fuente