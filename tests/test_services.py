import pytest
from services.normalizer_service import normalizar_datos_aemet
from services.alert_service import AlertService


def test_normalizer_handles_ip_rain():
    """Verifica que la lluvia inapreciable 'Ip' se convierta en 0.0."""
    raw_data = [
        {"fint": "2023-10-27T10:00:00", "prec": "Ip", "ta": "20", "hr": "50", "vv": "10", "ubi": "Test"}
    ]
    normalized = normalizar_datos_aemet(raw_data, "TEST")
    assert normalized["lluvia"] == 0.0
    assert isinstance(normalized["lluvia"], float)


def test_normalizer_handles_none_values():
    """Verifica que valores None se conviertan a 0.0."""
    raw_data = [
        {"fint": "2023-10-27T10:00:00", "prec": None, "ta": "20", "hr": None, "vv": None, "ubi": "Test"}
    ]
    normalized = normalizar_datos_aemet(raw_data, "TEST")
    assert normalized["lluvia"] == 0.0
    assert normalized["humedad"] == 0.0
    assert normalized["viento"] == 0.0


def test_alert_service_red_alert():
    """Verifica que se dispare la alerta ROJA a partir de 40 grados."""
    service = AlertService()
    data = {
        "temperatura": 42.0,
        "viento": 10.0,
        "lluvia": 0.0,
        "humedad": 40
    }
    alertas = service.evaluar_alertas(data)
    assert "ROJA" in alertas


def test_alert_service_orange_alert():
    """Verifica que se dispare la alerta NARANJA a partir de 35 grados."""
    service = AlertService()
    data = {
        "temperatura": 36.0,
        "viento": 10.0,
        "lluvia": 0.0,
        "humedad": 40
    }
    alertas = service.evaluar_alertas(data)
    assert "NARANJA" in alertas


def test_alert_service_cold_alert():
    """Verifica que se dispare HELADA a 0 grados o menos."""
    service = AlertService()
    data = {
        "temperatura": -1.0,
        "viento": 10.0,
        "lluvia": 0.0,
        "humedad": 40
    }
    alertas = service.evaluar_alertas(data)
    assert "HELADA" in alertas


def test_alert_service_multiple_alerts():
    """Verifica que las alertas sean acumulativas (viento y lluvia)."""
    service = AlertService()
    data = {
        "temperatura": 20.0,
        "viento": 80.0,
        "lluvia": 45.0,
        "humedad": 50
    }
    alertas = service.evaluar_alertas(data)
    assert "VIENTO_FUERTE" in alertas
    assert "LLUVIA_INTENSA" in alertas
    assert len(alertas) == 2


def test_alert_service_high_humidity():
    """Verifica alerta de humedad alta."""
    service = AlertService()
    data = {
        "temperatura": 25.0,
        "viento": 10.0,
        "lluvia": 0.0,
        "humedad": 95
    }
    alertas = service.evaluar_alertas(data)
    assert "HUMEDAD_ALTA" in alertas