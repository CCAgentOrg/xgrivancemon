"""TursoDB database interface"""
import libsql_client
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid

class Database:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.client = None
    
    async def initialize(self):
        """Initialize database connection"""
        self.client = libsql_client.create_client(
            url=self.url,
            auth_token=self.token
        )
    
    async def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
    
    async def get_active_authorities(self) -> List[Dict]:
        """Get all active authorities"""
        result = self.client.execute(
            "SELECT * FROM authorities WHERE active = 1 ORDER BY schedule_day, schedule_hour"
        )
        return [dict(row) for row in result.rows]
    
    async def get_authorities(self, city: Optional[str] = None, active_only: bool = True) -> List[Dict]:
        """Get authorities with optional filtering"""
        query = "SELECT * FROM authorities WHERE 1=1"
        params = []
        if city:
            query += " AND city = ?"
            params.append(city)
        if active_only:
            query += " AND active = 1"
        query += " ORDER BY name"
        
        result = self.client.execute(query, params)
        return [dict(row) for row in result.rows]
    
    async def insert_authority(self, authority: Dict) -> str:
        """Insert new authority"""
        authority_id = str(uuid.uuid4())
        self.client.execute(
            """INSERT INTO authorities 
               (id, name, handle, city, state, type, schedule_day, schedule_hour, active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                authority_id,
                authority['name'],
                authority['handle'],
                authority.get('city', ''),
                authority.get('state', ''),
                authority.get('type', 'bus'),
                authority.get('schedule_day', 0),
                authority.get('schedule_hour', 9),
                authority.get('active', True)
            ]
        )
        return authority_id
    
    async def insert_complaint(self, complaint: Dict) -> str:
        """Insert complaint"""
        complaint_id = str(uuid.uuid4())
        try:
            self.client.execute(
                """INSERT INTO complaints 
                   (id, x_post_id, authority_id, content, author_handle, posted_at, url, category, sentiment)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(x_post_id) DO UPDATE SET updated_at = CURRENT_TIMESTAMP""",
                [
                    complaint_id,
                    complaint['x_post_id'],
                    complaint.get('authority_id'),
                    complaint['content'],
                    complaint.get('author_handle'),
                    complaint['posted_at'],
                    complaint.get('url'),
                    complaint.get('category'),
                    complaint.get('sentiment', 0)
                ]
            )
        except Exception as e:
            print(f"Error inserting complaint: {e}")
        return complaint_id
    
    async def get_complaints(self, authority_id: Optional[str] = None, 
                            category: Optional[str] = None,
                            days: int = 7, limit: int = 50) -> List[Dict]:
        """Get complaints with filtering"""
        since = datetime.now() - timedelta(days=days)
        
        query = "SELECT * FROM complaints WHERE posted_at > ?"
        params = [since.isoformat()]
        
        if authority_id:
            query += " AND authority_id = ?"
            params.append(authority_id)
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY posted_at DESC LIMIT ?"
        params.append(limit)
        
        result = self.client.execute(query, params)
        return [dict(row) for row in result.rows]
    
    async def get_weekly_stats(self, authority_id: str, week_start: datetime, week_end: datetime) -> Dict:
        """Get weekly statistics for an authority"""
        result = self.client.execute(
            """SELECT 
                COUNT(*) as total_complaints,
                SUM(CASE WHEN has_response = 1 THEN 1 ELSE 0 END) as total_responses,
                AVG(response_time_hours) as avg_response_time,
                category
               FROM complaints 
               WHERE authority_id = ? AND posted_at BETWEEN ? AND ?
               GROUP BY category""",
            [authority_id, week_start.isoformat(), week_end.isoformat()]
        )
        
        stats = {
            "total_complaints": 0,
            "total_responses": 0,
            "avg_response_time": 0,
            "categories": []
        }
        
        for row in result.rows:
            stats["categories"].append({
                "category": row[3],
                "count": row[0]
            })
            stats["total_complaints"] += row[0]
            stats["total_responses"] += row[1] if row[1] else 0
        
        return stats
    
    async def insert_report(self, report: Dict) -> str:
        """Insert generated report"""
        report_id = str(uuid.uuid4())
        self.client.execute(
            """INSERT INTO reports 
               (id, authority_id, week_start, week_end, report_markdown, 
                total_complaints, total_responses, avg_response_time, top_categories)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                report_id,
                report['authority_id'],
                report['week_start'],
                report['week_end'],
                report['report_markdown'],
                report['stats']['total_complaints'],
                report['stats']['total_responses'],
                report['stats']['avg_response_time'],
                str(report['stats'].get('categories', []))
            ]
        )
        return report_id
    
    async def get_reports(self, authority_id: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get reports with filtering"""
        query = "SELECT * FROM reports WHERE 1=1"
        params = []
        
        if authority_id:
            query += " AND authority_id = ?"
            params.append(authority_id)
        
        query += " ORDER BY week_end DESC LIMIT ?"
        params.append(limit)
        
        result = self.client.execute(query, params)
        return [dict(row) for row in result.rows]
    
    async def get_dashboard_stats(self) -> Dict:
        """Get dashboard summary statistics"""
        total_authorities = self.client.execute(
            "SELECT COUNT(*) FROM authorities WHERE active = 1"
        ).rows[0][0]
        
        week_start = datetime.now() - timedelta(days=7)
        weekly_complaints = self.client.execute(
            "SELECT COUNT(*) FROM complaints WHERE posted_at > ?",
            [week_start.isoformat()]
        ).rows[0][0]
        
        weekly_responses = self.client.execute(
            """SELECT COUNT(*) FROM complaints 
               WHERE posted_at > ? AND has_response = 1""",
            [week_start.isoformat()]
        ).rows[0][0]
        
        return {
            "total_authorities": total_authorities,
            "weekly_complaints": weekly_complaints,
            "weekly_responses": weekly_responses,
            "response_rate": (weekly_responses / weekly_complaints * 100) if weekly_complaints > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }

    async def get_agent_count(self) -> int:
        """Get total number of unique agents"""
        result = await self.client.execute(
            "SELECT COUNT(DISTINCT agent_id) as count FROM agent_runs"
        )
        return result.rows[0]["count"] if result.rows else 0
    
    async def get_today_agent_runs(self) -> int:
        """Get count of agent runs today"""
        result = await self.client.execute(
            "SELECT COUNT(*) as count FROM agent_runs WHERE DATE(created_at) = DATE('now')"
        )
        return result.rows[0]["count"] if result.rows else 0
    
    async def get_recent_agent_runs(self, limit: int = 20):
        """Get recent agent runs with stats"""
        result = await self.client.execute(
            """SELECT agent_id, created_at, duration_ms, status, 
                      complaints_collected, authority_handle
               FROM agent_runs 
               ORDER BY created_at DESC 
               LIMIT ?""",
            [limit]
        )
        return [dict(row) for row in result.rows] if result.rows else []
    
    async def get_complaints_by_authority(self):
        """Get complaint counts grouped by authority"""
        result = await self.client.execute(
            """SELECT a.name, COUNT(c.id) as complaint_count
               FROM authorities a
               LEFT JOIN complaints c ON a.id = c.authority_id
               WHERE c.created_at >= date('now', '-7 days')
               GROUP BY a.id
               ORDER BY complaint_count DESC"""
        )
        return [dict(row) for row in result.rows] if result.rows else []
