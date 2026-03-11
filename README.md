# XGrivanceMon 🚌

[![CI/CD](https://github.com/CCAgentOrg/xgrivancemon/actions/workflows/ci.yml/badge.svg)](https://github.com/CCAgentOrg/xgrivancemon/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Transport Grievance Monitoring System for India**

XGrivanceMon tracks public complaints and government responses across 12 Indian transport authorities on X (Twitter), generating weekly audit reports with response time analysis and accountability metrics.

## 🎯 Features

- **12 Transport Authorities**: Monitors MTC Chennai, BEST Mumbai, DTC Delhi, BMTC Bangalore, KSRTC Kerala, UPSRTC UP, TGSRTC Telangana, and Chennai's ONE, DRM, CUMTA, Metro, and Corporation
- **Automated Data Collection**: Uses X API to gather complaints and responses
- **Weekly Audit Reports**: Markdown reports with response rates and category analysis
- **Dashboard API**: Real-time statistics and health monitoring
- **Docker-First**: Production-ready containerized deployment
- **Test Coverage**: >80% test coverage with pytest

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
git clone https://github.com/CCAgentOrg/xgrivancemon.git
cd xgrivancemon

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Start services
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up database
python -m migrations.apply

# Run server
python -m src.main
```

## 📊 Monitored Authorities

| Authority | Handle | Schedule |
|-----------|--------|----------|
| MTC Chennai | [@MtcChennai](https://x.com/MtcChennai) | Wednesdays 9:00 AM |
| BEST Mumbai | [@myBESTBus](https://x.com/myBESTBus) | Mondays 9:00 AM |
| DTC Delhi | [@dtc_india](https://x.com/dtc_india) | Fridays 9:00 AM |
| BMTC Bangalore | [@BMTC_BENGALURU](https://x.com/BMTC_BENGALURU) | Tuesdays 9:00 AM |
| KSRTC Kerala | [@KSRTC_Kerala](https://x.com/KSRTC_Kerala) | Wednesdays 9:00 AM |
| UPSRTC UP | [@UPSRTCHQ](https://x.com/UPSRTCHQ) | Saturdays 9:00 AM |
| TGSRTC Telangana | [@TGSRTCHQ](https://x.com/TGSRTCHQ) | Sundays 9:00 AM |
| Chennai ONE | [@Chennai_One](https://x.com/Chennai_One) | Mondays 2:00 PM |
| Chennai DRM | [@drmchennai](https://x.com/drmchennai) | Wednesdays 4:00 PM |
| Chennai CUMTA | [@cumtaOfficial](https://x.com/cumtaOfficial) | Thursdays 5:00 PM |
| Chennai Metro | [@cmrlchennai](https://x.com/cmrlchennai) | Tuesdays 3:00 PM |
| Chennai Corporation | [@chennaicorp](https://x.com/chennaicorp) | Mondays 11:00 AM |

## 🔧 API Endpoints

### Health Check
```bash
curl http://localhost:8080/health
```

### List Authorities
```bash
curl "http://localhost:8080/authorities?city=Chennai"
```

### Dashboard Stats
```bash
curl http://localhost:8080/dashboard
```

### Trigger Collection
```bash
curl -X POST http://localhost:8080/collect
```

### Trigger Report Generation
```bash
curl -X POST http://localhost:8080/report
```

## 📁 Project Structure

```
xgrivancemon/
├── src/
│   ├── main.py           # FastAPI server & scheduler
│   ├── collector.py      # X API integration
│   ├── database.py       # TursoDB interface
│   ├── analyzer.py       # Sentiment & classification
│   ├── reporter.py       # Report generation
│   └── config.py         # Settings management
├── migrations/
│   └── schema.sql        # Database schema
├── config/
│   └── authorities.json  # 12 authority configs
├── tests/
│   ├── test_collector.py
│   └── test_database.py
├── .github/workflows/
│   └── ci.yml            # GitHub Actions
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🧪 Testing

```bash
# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test
pytest tests/test_collector.py -v
```

## 🚢 Deployment

### Requirements
- Docker & Docker Compose
- TursoDB account (free tier)
- X API credentials (Basic tier)

### Environment Variables

```env
# X API
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret

# Database
TURSO_URL=libsql://your-db.turso.io
TURSO_TOKEN=your_token

# Scheduling
COLLECTION_HOUR=8
REPORT_DAY=sun
REPORT_HOUR=10
```

### Deploy to DigitalOcean/Hetzner

```bash
# On your VM
git clone https://github.com/CCAgentOrg/xgrivancemon.git
cd xgrivancemon
docker-compose up -d
```

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- Issues: [GitHub Issues](https://github.com/CCAgentOrg/xgrivancemon/issues)
- Telegram: [@CashlessConsumer](https://t.me/CashlessConsumer)

---

**Made with ❤️ for better public transport accountability in India**
