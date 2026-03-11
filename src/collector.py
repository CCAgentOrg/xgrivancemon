"""
X Grievance Collector - Cookie-based Session Auth
Uses stored session cookies for X web scraping (not API)
"""

import requests
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class XCollector:
    def __init__(self, auth_token: str, csrf_token: str):
        self.session = requests.Session()
        self.base_url = "https://x.com/i/api"
        
        # Set up session cookies
        self.session.cookies.set("auth_token", auth_token, domain=".x.com")
        self.session.headers.update({
            "X-Csrf-Token": csrf_token,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Referer": "https://x.com/",
        })
    
    def search_tweets(self, query: str, since: str, until: str) -> List[Dict]:
        """Search tweets using X web interface"""
        tweets = []
        
        try:
            search_url = f"{self.base_url}/2/search/adaptive.json"
            params = {
                "q": query,
                "count": 100,
                "result_type": "recent",
                "tweet_mode": "extended"
            }
            
            response = self.session.get(search_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                for tweet in data.get("globalObjects", {}).get("tweets", {}).values():
                    tweets.append(self._parse_tweet(tweet))
            
            elif response.status_code == 429:
                time.sleep(60)
                return self.search_tweets(query, since, until)
                
        except Exception as e:
            print(f"Error: {e}")
        
        return tweets
    
    def _parse_tweet(self, tweet: Dict) -> Dict:
        return {
            "id": tweet.get("id_str"),
            "x_post_id": tweet.get("id_str"),
            "content": tweet.get("full_text", ""),
            "posted_at": tweet.get("created_at"),
            "url": f"https://x.com/i/status/{tweet.get('id_str')}",
            "reply_count": tweet.get("reply_count", 0),
            "retweet_count": tweet.get("retweet_count", 0),
            "like_count": tweet.get("favorite_count", 0),
        }
    
    async def search_complaints(self, to_handle: str, since_hours: int = 168) -> List[Dict]:
        since_time = datetime.now() - timedelta(hours=since_hours)
        query = f"to:{to_handle} OR @{to_handle} since:{since_time.strftime('%Y-%m-%d')}"
        return self.search_tweets(query, "", "")
    
    async def search_responses(self, from_handle: str, since_hours: int = 168) -> List[Dict]:
        since_time = datetime.now() - timedelta(hours=since_hours)
        query = f"from:{from_handle} since:{since_time.strftime('%Y-%m-%d')}"
        return self.search_tweets(query, "", "")

async def collect_grievances(auth_token: str, csrf_token: str, authority_handle: str):
    collector = XCollector(auth_token, csrf_token)
    complaints = await collector.search_complaints(authority_handle)
    responses = await collector.search_responses(authority_handle)
    return {
        "complaints": complaints,
        "responses": responses,
        "authority": authority_handle,
        "collected_at": datetime.now().isoformat()
    }
