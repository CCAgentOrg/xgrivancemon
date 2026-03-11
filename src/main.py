#!/usr/bin/env python3
"""
XGrivanceMon - Main Application Entry Point
"""
import os
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
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
    # Startup
    app.state.db = Database(settings.turso_url, settings.turso_token)
    await app.state.db.initialize()
    
    app.state.collector = XCollector(
        api_key=settings.x_api_key,
        api_secret=settings.x_api_secret
    )
    app.state.analyzer = GrievanceAnalyzer()
    app.state.reporter = ReportGenerator()
    
    # Start scheduler
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
    
    # Shutdown
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

async def collect_grievances(db: Database, collector: XCollector):
    """Scheduled job: Collect grievances from X"""
    authorities = await db.get_active_authorities()
    for authority in authorities:
        complaints = await collector.search_complaints(
            to_handle=authority['handle'],
            since_hours=24
        )
        for complaint in complaints:
            await db.insert_complaint(complaint)

async def generate_reports(db: Database, reporter: ReportGenerator):
    """Scheduled job: Generate weekly reports"""
    authorities = await db.get_active_authorities()
    week_start = datetime.now() - timedelta(days=7)
    week_end = datetime.now()
    
    for authority in authorities:
        stats = await db.get_weekly_stats(authority['id'], week_start, week_end)
        report = reporter.generate_markdown_report(stats, authority)
        await db.insert_report({
            'authority_id': authority['id'],
            'week_start': week_start.date(),
            'week_end': week_end.date(),
            'report_markdown': report,
            'stats': stats
        })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/authorities")
async def list_authorities(
    city: str = Query(None, description="Filter by city"),
    active_only: bool = Query(True, description="Only active authorities")
):
    """List transport authorities"""
    db = app.state.db
    authorities = await db.get_authorities(city=city, active_only=active_only)
    return {"authorities": authorities, "count": len(authorities)}

@app.post("/authorities")
async def add_authority(authority: dict):
    """Add new authority to monitor"""
    db = app.state.db
    authority_id = await db.insert_authority(authority)
    return {"id": authority_id, "status": "created"}

@app.get("/complaints")
async def list_complaints(
    authority_id: str = Query(None),
    category: str = Query(None),
    days: int = Query(7, ge=1, le=30),
    limit: int = Query(50, ge=1, le=100)
):
    """List grievances with filtering"""
    db = app.state.db
    complaints = await db.get_complaints(
        authority_id=authority_id,
        category=category,
        days=days,
        limit=limit
    )
    return {"complaints": complaints, "count": len(complaints)}

@app.get("/reports")
async def list_reports(
    authority_id: str = Query(None),
    limit: int = Query(10, ge=1, le=50)
):
    """List generated reports"""
    db = app.state.db
    reports = await db.get_reports(authority_id=authority_id, limit=limit)
    return {"reports": reports, "count": len(reports)}

@app.get("/dashboard")
async def dashboard_stats():
    """Dashboard summary statistics"""
    db = app.state.db
    stats = await db.get_dashboard_stats()
    return stats

@app.post("/collect")
async def trigger_collection():
    """Manually trigger grievance collection"""
    await collect_grievances(app.state.db, app.state.collector)
    return {"status": "collection triggered"}

@app.post("/report")
async def trigger_report():
    """Manually trigger report generation"""
    await generate_reports(app.state.db, app.state.reporter)
    return {"status": "report generation triggered"}

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.debug
    )