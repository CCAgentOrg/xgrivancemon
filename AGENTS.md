# AGENTS.md - XGrivanceMon

## Repository Overview

XGrivanceMon is a generic transport grievance monitoring system that tracks public complaints and government responses across Indian transport authorities on X (Twitter).

When working on this codebase:

1. **Docker First**: All services must run in Docker containers
2. **Test Coverage**: Maintain >80% test coverage for new code
3. **Database**: Use TursoDB (SQLite over HTTP) - no PostgreSQL/MySQL
4. **API**: FastAPI with async endpoints
5. **Documentation**: Update README and ARCHITECTURE.md for significant changes

## Active Transport Monitoring Agents (12 Authorities)

| # | Authority | Handle | Type | City/State | Schedule |
|---|-----------|--------|------|------------|----------|
| 1 | MTC Chennai | @MtcChennai | Bus | Chennai, TN | Wednesdays 9:00 AM |
| 2 | BEST Mumbai | @myBESTBus | Bus | Mumbai, MH | Mondays 9:00 AM |
| 3 | DTC Delhi | @dtc_india | Bus | Delhi | Fridays 9:00 AM |
| 4 | BMTC Bangalore | @BMTC_BENGALURU | Bus | Bangalore, KA | Tuesdays 9:00 AM |
| 5 | KSRTC Kerala | @KSRTC_Kerala | Bus | Kerala | Wednesdays 9:00 AM |
| 6 | UPSRTC UP | @UPSRTCHQ | Bus | Uttar Pradesh | Saturdays 9:00 AM |
| 7 | TGSRTC Telangana | @TGSRTCHQ | Bus | Telangana | Sundays 9:00 AM |
| 8 | Chennai ONE | @Chennai_One | Mixed | Chennai, TN | Mondays 2:00 PM |
| 9 | Chennai DRM | @drmchennai | Rail | Chennai, TN | Wednesdays 4:00 PM |
| 10 | Chennai CUMTA | @cumtaOfficial | Mixed | Chennai, TN | Thursdays 5:00 PM |
| 11 | Chennai Metro | @cmrlchennai | Metro | Chennai, TN | Tuesdays 3:00 PM |
| 12 | Chennai Corporation | @chennaicorp | Corp | Chennai, TN | Mondays 11:00 AM |

## Key Files

- `src/main.py` - FastAPI server with scheduled jobs
- `src/collector.py` - X API integration and data collection
- `src/database.py` - TursoDB interface
- `src/analyzer.py` - Classification and sentiment analysis
- `src/reporter.py` - Report generation
- `src/config.py` - Settings management
- `migrations/schema.sql` - Database schema with all 12 authorities
- `config/authorities.json` - Authority configurations
- `tests/` - pytest test suite

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/authorities` | GET/POST | List/add authorities |
| `/complaints` | GET | List grievances |
| `/reports` | GET | List reports |
| `/dashboard` | GET | Dashboard stats |
| `/collect` | POST | Trigger collection |
| `/report` | POST | Trigger reports |

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

```bash
docker-compose up -d
```

## Environment Variables

```env
X_API_KEY=your_x_api_key
X_API_SECRET=your_x_api_secret
TURSO_URL=your_turso_url
TURSO_TOKEN=your_turso_token
COLLECTION_HOUR=8
REPORT_DAY=sun
REPORT_HOUR=10
```
