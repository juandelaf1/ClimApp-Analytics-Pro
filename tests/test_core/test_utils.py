import pytest
from app.core.utils import haversine


class TestHaversine:
    def test_madrid_centro(self):
        dist = haversine(40.4168, -3.7038, 40.4168, -3.7038)
        assert dist == 0.0

    def test_madrid_alcala(self):
        dist = haversine(40.4168, -3.7038, 40.4821, -3.3644)
        assert 25 < dist < 35

    def test_simetric(self):
        d1 = haversine(40.0, -3.0, 41.0, -4.0)
        d2 = haversine(41.0, -4.0, 40.0, -3.0)
        assert abs(d1 - d2) < 0.001