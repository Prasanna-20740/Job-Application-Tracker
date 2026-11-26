
# Changelog

All notable changes to this project are documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Introduced API versioning with separate V1 and V2 endpoints.
- Added `/api/v1/applications` endpoint.
- Added `/api/v2/applications` endpoint.
- Added `Deprecation: true` response header to V1 endpoints.
- Added V2 summary response format using `?format=summary`.
- Added pagination support to versioned application endpoints.

### Changed
- V2 supports both full and summary application responses.
- Existing application data structure is maintained in V1.

### Documentation
- Added API versioning documentation.
- Added V1 to V2 migration guide.
