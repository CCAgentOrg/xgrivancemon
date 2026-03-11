# XGrivanceMon

A generic, self-hostable transport grievance redressal monitoring system that tracks public complaints on X (Twitter) and analyzes response patterns from transport authorities.

## Features

- **Generic Monitoring**: Works with any X handle (@MtcChennai, @dtc_india, etc.)
- **Automated Collection**: Hourly polling of complaints and responses
- **Smart Classification**: Auto-categorizes by type (frequency, infrastructure, staff, fares)
- **Analytics Dashboard**: Response rate, resolution time, sentiment analysis
- **Weekly Reports**: Auto-generated markdown reports published to web
- **Multi-City Support**: Monitor any number of transport authorities

## Quick Start

```bash
# Clone and setup
git clone https://github.com/CCAgentOrg/xgrivancemon.git
cd xgrivancemon
cp .env.example .env
# Edit .env with your X API keys and TursoDB URL

# Run locally
pip install -r requirements.txt
python -m src.main

# Or use Docker
docker-compose up -d
```

## Configuration

Edit `.env`:
```
X_API_BEARER_TOKEN=your_token_here
TURSO_DATABASE_URL=libsql://your-db.turso.io
TURSO_AUTH_TOKEN=your_auth_token
MONITORED_HANDLES=@MtcChennai,@dtc_india
COLLECTION_INTERVAL=3600
REPORT_SCHEDULE=0 9 * * 0  # Sundays 9 AM
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

## Deployment

See [DEPLOY.md](DEPLOY.md) for Docker deployment instructions.

## License

MIT - See LICENSE
