import os
import requests
from services.logging_service import log_info, log_warning

def resolve_location(lat=None, lon=None, city=None):
    """
    Lógica de Failover: GPS -> Geocoding -> Default (Madrid).
    Resuelve coordenadas asegurando compatibilidad con tipos de JS.
    """
    
    # --- 1. Limpieza de entrada (Evita "null"/"undefined" de JavaScript) ---
    def is_valid(value):
        return value and str(value).lower() not in ["none", "null", "undefined", ""]

    # --- 2. Prioridad 1: Coordenadas GPS directas ---
    if is_valid(lat) and is_valid(lon):
        try:
            log_info(f"Ubicación establecida mediante GPS: {lat}, {lon}")
            return {
                "lat": float(lat), 
                "lon": float(lon), 
                "source": "GPS", 
                "success": True
            }
        except ValueError:
            log_warning(f"Coordenadas GPS inválidas recibidas: {lat}, {lon}")

    # --- 3. Prioridad 2: Texto Manual (Geocoding) ---
    if is_valid(city):
        city_clean = str(city).strip().lower()
        
        # Diccionario de ciudades soportadas (capitales de provincia España)
        mock_cities = {
            # Madrid y grandes ciudades
            "madrid": {"lat": 40.4167, "lon": -3.7033},
            "barcelona": {"lat": 41.3851, "lon": 2.1734},
            "valencia": {"lat": 39.4699, "lon": -0.3763},
            "sevilla": {"lat": 37.3891, "lon": -5.9845},
            # Andalucía
            "málaga": {"lat": 36.7213, "lon": -4.4214},
            "córdoba": {"lat": 37.8888, "lon": -4.7794},
            "granada": {"lat": 37.1773, "lon": -3.5986},
            "huelva": {"lat": 37.2614, "lon": -6.9448},
            "cadiz": {"lat": 36.5271, "lon": -6.2886},
            "almería": {"lat": 36.8340, "lon": -2.4517},
            "jerez de la frontera": {"lat": 36.6854, "lon": -6.1260},
            # Cataluña
            "tarragona": {"lat": 41.1153, "lon": 1.2539},
            "girona": {"lat": 41.9794, "lon": 2.8214},
            "lleida": {"lat": 41.6176, "lon": 0.6202},
            # Comunidad Valenciana
            "alicante": {"lat": 38.3452, "lon": -0.4810},
            "castellón": {"lat": 39.9713, "lon": -0.0321},
            # Galicia
            "a coruña": {"lat": 43.3623, "lon": -8.3965},
            "vigo": {"lat": 42.2408, "lon": -8.7207},
            "ourense": {"lat": 42.3355, "lon": -7.8638},
            "lugo": {"lat": 43.0108, "lon": -7.5558},
            "santiago de compostela": {"lat": 42.8782, "lon": -8.5448},
            # Castilla y León
            "valladolid": {"lat": 41.6351, "lon": -4.7195},
            "burgos": {"lat": 42.3439, "lon": -3.6969},
            "león": {"lat": 42.5997, "lon": -5.5705},
            "salamanca": {"lat": 40.9702, "lon": -5.6635},
            "palencia": {"lat": 42.0096, "lon": -4.4876},
            "segovia": {"lat": 40.9429, "lon": -4.1083},
            "ávila": {"lat": 40.2822, "lon": -4.9255},
            "soria": {"lat": 41.7640, "lon": -2.4789},
            "zamora": {"lat": 41.5033, "lon": -5.5707},
            # Castilla-La Mancha
            "toledo": {"lat": 39.8678, "lon": -4.0167},
            "albacete": {"lat": 38.9943, "lon": -1.8588},
            "cuenca": {"lat": 40.0701, "lon": -2.1374},
            "guadalajara": {"lat": 40.6326, "lon": -3.1673},
            "ciudad real": {"lat": 38.9864, "lon": -3.9302},
            # País Vasco
            "bilbao": {"lat": 43.2630, "lon": -2.9350},
            "vitoria": {"lat": 42.8125, "lon": -2.6727},
            "donostia": {"lat": 43.3203, "lon": -1.9818},
            # Asturias
            "oviedo": {"lat": 43.3619, "lon": -5.8494},
            "gijón": {"lat": 43.5423, "lon": -5.6761},
            # Cantabria
            "santander": {"lat": 43.4623, "lon": -3.8099},
            # Navarra
            "pamplona": {"lat": 42.8125, "lon": -1.6458},
            # La Rioja
            "logroño": {"lat": 42.4637, "lon": -2.4450},
            # Aragón
            "zaragoza": {"lat": 41.6488, "lon": -0.8891},
            "huesca": {"lat": 42.1315, "lon": -0.4077},
            "teruel": {"lat": 40.3456, "lon": -1.1061},
            # Extremadura
            "badajoz": {"lat": 38.8743, "lon": -6.9538},
            "cáceres": {"lat": 39.4735, "lon": -6.3770},
            # Murcia
            "murcia": {"lat": 37.9838, "lon": -1.1445},
            "cartagena": {"lat": 37.6067, "lon": -0.9850},
            # Canarias
            "las Palmas": {"lat": 28.1248, "lon": -15.4466},
            "santa Cruz de Tenerife": {"lat": 28.4636, "lon": -16.2518},
            # Baleares
            "palma": {"lat": 39.5696, "lon": 2.6502},
            "ibiza": {"lat": 38.9067, "lon": 1.4207},
            "mahón": {"lat": 39.8895, "lon": 4.2795},
            # Ceuta y Melilla
            "ceuta": {"lat": 35.8894, "lon": -5.3215},
            "melilla": {"lat": 35.2938, "lon": -2.9386}
        }

        if city_clean in mock_cities:
            log_info(f"Ubicación resuelta por búsqueda manual: {city_clean}")
            coords = mock_cities[city_clean]
            return {
                "lat": coords["lat"], 
                "lon": coords["lon"], 
                "source": "MANUAL_SEARCH", 
                "success": True
            }
        
        log_warning(f"Ciudad '{city}' no encontrada en el sistema. Aplicando fallback.")

    # --- 4. Prioridad 3: Ubicación por defecto (Madrid HQ) ---
    # Esto es lo que evita que la pantalla se quede en "Cargando..." si falla el GPS
    log_info("Aplicando ubicación por defecto: Madrid (DashLogistics HQ)")
    return {
        "lat": 40.4530, 
        "lon": -3.6883, 
        "source": "IP_INFERRED", 
        "success": True
    }