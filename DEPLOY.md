# XGrivanceMon Deployment Guide

## Self-Host on Any VM (Docker)

### Prerequisites
- Ubuntu 20.04+ / Debian 11+ / Any Linux VM
- Docker 24.0+ and docker-compose
- 2GB RAM minimum, 4GB recommended
- TursoDB account (free tier sufficient)

### Step 1: Setup TursoDB

```bash
# Install Turso CLI
curl -sSfL https://get.tur.so/install.sh | bash

# Login and create database
turso auth login
turso db create xgrivancemon
turso db tokens create xgrivancemon --name full-access

# Get connection URL
turso db show xgrivancemon
# Copy the "LibSQL URL" (e.g., libsql://xgrivancemon-youruser.turso.io)
```

### Step 2: Get X API Credentials

1. Go to https://developer.x.com/en/portal/dashboard
2. Create a new app
3. Generate API Key and Secret
4. For search API, you may need Elevated access

### Step 3: Deploy XGrivanceMon

```bash
# SSH into your VM
git clone https://github.com/youruser/xgrivancemon.git
cd xgrivancemon

# Create environment file
cat > .env << ENVEOF
TURSO_URL=libsql://xgrivancemon-youruser.turso.io
TURSO_TOKEN=your-turso-token-here
X_API_KEY=your-x-api-key
X_API_SECRET=your-x-api-secret
COLLECTION_HOUR=9
REPORT_DAY=thu
REPORT_HOUR=10
ENVEOF

# Start services
docker-compose up -d

# View logs
docker-compose logs -f xgrivance
```

### Step 4: Add Authorities to Monitor

```bash
# Use the API to add transport authorities
curl -X POST http://localhost:8080/authorities \
  -H "Content-Type: application/json" \
  -d '{
    "id": "mtc-chennai",
    "handle": "MtcChennai",
    "name": "MTC Chennai",
    "city": "Chennai",
    "state_code": "TN"
  }'
```

### Step 5: Verify Deployment

```bash
# Health check
curl http://localhost:8080/health

# View dashboard stats
curl http://localhost:8080/dashboard

# List authorities
curl http://localhost:8080/authorities
```

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `TURSO_URL` | TursoDB connection URL | Required |
| `TURSO_TOKEN` | TursoDB auth token | Required |
| `X_API_KEY` | X API Key | Required |
| `X_API_SECRET` | X API Secret | Required |
| `COLLECTION_HOUR` | Hour to collect grievances (0-23) | 9 |
| `REPORT_DAY` | Day to generate reports (mon-sun) | thu |
| `REPORT_HOUR` | Hour to generate reports | 10 |

## Architecture

```
┌─────────────────────────────────────────┐
│           Your VM (Any Cloud)            │
│  ┌──────────────────────────────────┐  │
│  │     Docker Container               │  │
│  │  ┌────────────────────────────┐    │  │
│  │  │   XGrivanceMon App       │    │  │
│  │  │   - FastAPI server       │    │  │
│  │  │   - Scheduled collector  │    │  │
│  │  │   - Report generator     │    │  │
│  │  └────────────────────────────┘    │  │
│  │           │                        │  │
│  │           ▼                        │  │
│  │  ┌────────────────────────────┐    │  │
│  │  │   SQLite (local cache)     │    │  │
│  │  └────────────────────────────┘    │  │
│  └──────────────────────────────────┘  │
│                   │                      │
│                   ▼                      │
└─────────────────────────────────────────┘
                    │
         ┌──────────▼──────────┐
         │    TursoDB Cloud    │
         │  (SQLite over HTTP) │
         │  - Persistent store │
         │  - Edge replicated  │
         └─────────────────────┘
                    │
         ┌──────────▼──────────┐
         │      X API          │
         │  - Search tweets    │
         │  - Get replies      │
         └─────────────────────┘
```

## Troubleshooting

### Issue: Container won't start
```bash
# Check logs
docker-compose logs xgrivance

# Verify .env exists
cat .env

# Rebuild
docker-compose down
docker-compose up --build -d
```

### Issue: Can't connect to TursoDB
```bash
# Test connection
turso db shell xgrivancemon

# Verify token
turso db tokens list xgrivancemon
```

### Issue: No tweets being collected
```bash
# Check X API rate limits
docker-compose logs xgrivance | grep -i "rate"

# Verify API key is correct
curl -X GET "https://api.x.com/2/tweets/search/recent?query=test" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Updates

```bash
# Pull latest version
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

## Backup

```bash
# Export TursoDB data
turso db dump xgrivancemon > backup-$(date +%Y%m%d).sql

# Or use API to export
curl http://localhost:8080/reports > reports-backup.json
```
