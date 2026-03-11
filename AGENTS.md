# AGENTS.md - XGrivanceMon

## Repository Overview

This repository contains a generic transport grievance monitoring system.
When working on this codebase:

1. **Docker First**: All services must run in Docker containers
2. **Test Coverage**: Maintain >80% test coverage for new code
3. **Database**: Use TursoDB (SQLite over HTTP) - no PostgreSQL/MySQL
4. **API**: FastAPI with async endpoints
5. **Documentation**: Update README and ARCHITECTURE.md for significant changes

## Key Files

- `src/main.py` - FastAPI server with scheduled jobs
- `src/collector.py` - X API integration and data collection
- `src/database.py` - TursoDB interface
- `src/analyzer.py` - Classification and sentiment analysis
- `src/reporter.py` - Report generation
- `migrations/schema.sql` - Database schema
- `tests/` - pytest test suite

## Testing

```bash
pytest tests/ -v --cov=src --cov-report=html
```

## CI/CD

GitHub Actions runs:
- Tests on Python 3.11, 3.12
- Docker build verification
- Linting with ruff
- Type checking with mypy

## Deployment

Use the provided docker-compose.yml. The system is designed to run on any Linux VM (DigitalOcean, AWS, GCP, Hetzner).
