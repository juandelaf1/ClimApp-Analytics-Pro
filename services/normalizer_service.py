import uuid
from services.alert_service import AlertService
from services.logging_service import log_error

alert_service = AlertService()


def safe_float(value, default=0.0):
    """Convierte a float de forma segura, manejando 'Ip', None, etc."""
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    val_str = str(value).strip()
    if val_str == "" or val_str.lower() in ("ip", "Ip", "iP", "p"):
        return 0.0
    try:
        return float(val_str)
    except (ValueError, TypeError):
        return default


def normalizar_datos_aemet(data, fuente_ubicacion="AEMET"):
    """
    Estandariza los datos de AEMET, genera identificadores unicos 
    y asegura compatibilidad con el sistema de persistencia y alertas.
    """
    try:
        if not data:
            return None

        latest = data[-1] if isinstance(data, list) else data
        
        datos_normalizados = {
            "id": str(uuid.uuid4()),
            "municipio": latest.get("ubi", "Desconocida"),
            "estacion": latest.get("ubi", "Desconocida"),
            "fecha": latest.get("fint", "N/A"),
            "temperatura": safe_float(latest.get("ta")),
            "humedad": safe_float(latest.get("hr")),
            "viento": safe_float(latest.get("vv")),
            "presion": safe_float(latest.get("pres")),
            "lluvia": safe_float(latest.get("prec")),
            "fuente": fuente_ubicacion 
        }

        datos_normalizados["alertas"] = alert_service.evaluar_alertas(datos_normalizados)

        return datos_normalizados

    except Exception as e:
        log_error(f"Error en normalizacion de datos: {e}")
        return None