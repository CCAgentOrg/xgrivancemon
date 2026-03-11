# XGrivanceMon Architecture

## Overview
Generic, self-hostable transport grievance monitoring system.

## Components

### 1. Data Collection (XCollector)
- Polls X API every hour for new complaints
- Searches: to:@handle OR mentions of transport authority
- Extracts: post content, author, timestamp, location hints

### 2. Classification (GrievanceAnalyzer)
- Auto-categorizes: frequency, infrastructure, staff, fares, other
- Sentiment analysis: frustrated, neutral, positive
- Route extraction: regex for bus route numbers

### 3. Database (TursoDB)
- SQLite over HTTP - distributed by default
- Tables: authorities, complaints, responses, reports
- Indexed for fast queries

### 4. Reporting (ReportGenerator)
- Weekly markdown reports
- Metrics: response rate, avg response time, top issues
- Auto-publishes to web dashboard

### 5. Dashboard (FastAPI + React)
- Real-time stats
- Filter by city, authority, category
- Download reports

## Flow
```
X API → Collector → Classifier → TursoDB → Reporter → Dashboard
   ↑________________________________________↓
         (Authority responses tracked)
```

## Why TursoDB?
- Serverless SQLite - no DB server to manage
- Edge replicated - fast from any VM location
- Free tier: 9GB storage, 1B row reads/month
- Perfect for this scale

## Why Docker?
- Runs on any Linux VM (DigitalOcean, AWS, GCP, Hetzner)
- Single command deployment
- Easy updates
- Isolated dependencies
