#!/usr/bin/env python3
"""
XGrivanceMon - Main Application with Dashboard
"""
import os
import asyncio
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import uvicorn

from .config import Settings
from .database import Database
from .collector import XCollector
from .analyzer import GrievanceAnalyzer
from .reporter import ReportGenerator

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    app.state.db = Database(settings.turso_url, settings.turso_token)
    await app.state.db.initialize()
    
    app.state.collector = XCollector(
        api_key=settings.x_api_key,
        api_secret=settings.x_api_secret,
        cookie_session=settings.x_cookie_session
    )
    app.state.analyzer = GrievanceAnalyzer()
    app.state.reporter = ReportGenerator()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        collect_grievances,
        CronTrigger(hour=settings.collection_hour, minute=0),
        args=[app.state.db, app.state.collector]
    )
    scheduler.add_job(
        generate_reports,
        CronTrigger(day_of_week=settings.report_day, hour=settings.report_hour, minute=0),
        args=[app.state.db, app.state.reporter]
    )
    scheduler.start()
    app.state.scheduler = scheduler
    
    yield
    
    scheduler.shutdown()
    await app.state.db.close()

app = FastAPI(
    title="XGrivanceMon",
    description="Transport Grievance Monitoring System",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static frontend files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

@app.get("/")
async def root():
    """Redirect to dashboard"""
    return RedirectResponse(url="/frontend/index.html")

# API v1 routes
@app.get("/api/v1/stats")
async def api_stats():
    """Dashboard statistics API"""
    db = app.state.db
    total_agents = await db.get_agent_count()
    today_runs = await db.get_today_agent_runs()
    total_complaints = await db.get_complaint_count()
    avg_response = await db.get_avg_response_time()
    
    return {
        "totalAgents": total_agents,
        "todayRuns": today_runs,
        "totalComplaints": total_complaints,
        "avgResponseTime": avg_response
    }

@app.get("/api/v1/agent-runs")
async def api_agent_runs(limit: int = Query(20, ge=1, le=100)):
    """Recent agent runs API"""
    db = app.state.db
    runs = await db.get_recent_agent_runs(limit=limit)
    return {"agentRuns": runs}

@app.get("/api/v1/complaints/by-authority")
async def complaints_by_authority():
    """Complaints grouped by authority"""
    db = app.state.db
    data = await db.get_complaints_by_authority()
    return {"complaintsByAuthority": data}

async def collect_grievances(db: Database, collector: XCollector):
    """Scheduled job: Collect grievances"""
    authorities = await db.get_active_authorities()
    for authority in authorities:
        complaints = await collector.search_complaints(
            to_handle=authority["handle"],
            since_hours=24
        )
        for complaint in complaints:
            await db.insert_complaint(complaint)

async def generate_reports(db: Database, reporter: ReportGenerator):
    """Scheduled job: Generate reports"""
    authorities = await db.get_active_authorities()
    week_start = datetime.now() - timedelta(days=7)
    week_end = datetime.now()
    
    for authority in authorities:
        stats = await db.get_weekly_stats(authority["id"], week_start, week_end)
        report = reporter.generate_markdown_report(stats, authority)
        await db.insert_report({
            "authority_id": authority["id"],
            "week_start": week_start.date(),
            "week_end": week_end.date(),
            "report_markdown": report,
            "stats": stats
        })

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=settings.debug)
