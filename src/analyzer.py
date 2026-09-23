"""Grievance classification and sentiment analysis"""
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
        category_scores: Dict[str, int] = {}
        for cat, keywords in self.CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                category_scores[cat] = score
        
        category = max(category_scores, key=lambda k: category_scores[k]) if category_scores else "other"
        
        # Sentiment analysis (simple keyword-based)
        positive_count = sum(1 for word in self.POSITIVE_WORDS if word in text_lower)
        negative_count = sum(1 for word in self.NEGATIVE_WORDS if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = min(0.5 + 0.1 * positive_count, 1.0)
        elif negative_count > positive_count:
            sentiment = max(-0.5 - 0.1 * negative_count, -1.0)
        else:
            sentiment = 0.0
        
        return category, sentiment
    
    def analyze_batch(self, complaints: list) -> Dict:
        """Analyze a batch of complaints"""
        results = []
        for complaint in complaints:
            category, sentiment = self.classify(complaint.get('content', ''))
            results.append({
                'id': complaint.get('id'),
                'category': category,
                'sentiment': sentiment
            })
        
        return {
            'analyzed': len(results),
            'results': results,
            'categories': list(self.CATEGORIES.keys()) + ['other']
        }
