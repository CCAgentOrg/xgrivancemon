"""Grievance classification and sentiment analysis"""
import re
from typing import Dict, Tuple

class GrievanceAnalyzer:
    """Simple rule-based grievance analyzer"""
    
    CATEGORIES = {
        'frequency': ['late', 'delay', 'wait', 'timing', 'schedule', 'frequency', 'bus not coming'],
        'infrastructure': ['stop', 'terminal', 'shelter', 'road', 'display', 'infrastructure'],
        'staff': ['driver', 'conductor', 'behavior', 'rude', 'staff', 'crew'],
        'route': ['route', 'stop missing', 'wrong route', 'extension', 'new route'],
        'fare': ['fare', 'ticket', 'price', 'cost', 'expensive', 'overcharge']
    }
    
    POSITIVE_WORDS = ['resolved', 'thank', 'good', 'improved', 'helpful', 'appreciate']
    NEGATIVE_WORDS = ['worst', 'terrible', 'pathetic', 'useless', 'frustrating', 'angry', 'problematic']
    
    def classify(self, text: str) -> Tuple[str, float]:
        """Classify complaint category and sentiment"""
        text_lower = text.lower()
        
        # Category detection
        category_scores = {}
        for cat, keywords in self.CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                category_scores[cat] = score
        
        category = max(category_scores, key=category_scores.get) if category_scores else 'other'
        
        # Sentiment analysis (simple keyword-based)
        positive_count = sum(1 for word in self.POSITIVE_WORDS if word in text_lower)
        negative_count = sum(1 for word in self.NEGATIVE_WORDS if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 0.5
        elif negative_count > positive_count:
            sentiment = -0.5
        else:
            sentiment = 0
        
        return category, sentiment
    
    def analyze_complaint(self, complaint: Dict) -> Dict:
        """Analyze a single complaint"""
        category, sentiment = self.classify(complaint['content'])
        complaint['category'] = category
        complaint['sentiment'] = sentiment
        return complaint
