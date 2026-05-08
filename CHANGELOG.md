# Changelog - ClimApp-Analytics-Pro

All notable changes to this project will be documented in this file.

## [2.1.0] - 2026-05-08

### Added
- Rate Limiter (30 req/min /clima, 10 req/min /geo)
- Data validation with OMM ranges
- Improved station search (up to 100km)
- /api/stats endpoint
- /api/health with metrics

### Fixed
- Unicode encoding in alertas.json
- Duplicate /api/clima route conflict

## [2.0.0] - 2026-05-08

### Added
- GeolocationService (IP-API.com + Nominatim)
- AlertService with JSON config
- Offline cache (30 min)
- Health endpoints

## [1.0.0] - 2026-05-07

### Added
- Initial release
- AEMET OpenData integration
- Basic fallback by city