# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - Production Release

### Added
- **Docker Containerization**: Full Docker support with lightweight Python 3.11-slim image.
- **Railway Deployment Ready**: Auto-deployment configuration (`railway.json`).
- **Gunicorn & gevent WSGI**: Supports concurrency and SSE streaming for AI chat in production.
- **CI/CD Pipeline**: Automated GitHub Actions for Linting (flake8) and Testing (pytest).
- **Security Hardening**:
  - `Flask-Talisman` for HTTP security headers (CSP, HSTS).
  - `Flask-Limiter` to rate limit authentication and file uploads.
- **Monitoring Endpoints**: `/health`, `/ready`, and `/live` endpoints.
- **Environment Configuration**: Multi-stage `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig`.
- **Database Fallback**: Defaults to `sqlite` locally, seamlessly adopts PostgreSQL if `DATABASE_URL` is set in production.

### Changed
- Refactored `app/__init__.py` to securely apply Content Security Policies.
- Upgraded testing suite to include API and Health testing.

### Fixed
- Fixed module imports to be fully package-compliant for `pytest`.
