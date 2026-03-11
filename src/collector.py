import requests
from datetime import datetime, timedelta
from typing import List, Dict

class XCollector:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.x.com/2"
    
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def search_complaints(self, to_handle: str, since_hours: int = 24) -> List[Dict]:
        """Search for complaints mentioning an authority"""
        # Note: This uses X API v2 recent search
        # In production, you'd use the full archive search for historical data
        
        since_time = datetime.now() - timedelta(hours=since_hours)
        since_str = since_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        query = f"to:{to_handle} OR @{to_handle}"
        
        url = f"{self.base_url}/tweets/search/recent"
        params = {
            "query": query,
            "start_time": since_str,
            "tweet.fields": "created_at,author_id,public_metrics,geo",
            "user.fields": "username,public_metrics",
            "max_results": 100
        }
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            if response.status_code == 200:
                data = response.json()
                tweets = data.get("data", [])
                
                complaints = []
                for tweet in tweets:
                    complaint = {
                        "id": tweet["id"],
                        "x_post_id": tweet["id"],
                        "content": tweet["text"],
                        "author_handle": tweet.get("author_id"),  # Would need to lookup username
                        "posted_at": tweet["created_at"],
                        "url": f"https://x.com/i/status/{tweet['id']}",
                        "authority_id": to_handle
                    }
                    complaints.append(complaint)
                
                return complaints
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            return []
    
    async def get_replies(self, tweet_id: str, authority_handle: str) -> List[Dict]:
        """Get replies from the authority to a complaint"""
        # This would check if the authority replied
        # Implementation depends on X API capabilities
        return []
