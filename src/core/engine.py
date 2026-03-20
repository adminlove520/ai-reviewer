"""
ai-reviewer - Core Engine
"""
from typing import List, Optional
from .config import ReviewConfig

class ReviewEngine:
    """统一调度引擎"""
    
    def __init__(self, config: ReviewConfig):
        self.config = config
    
    async def review(self, event: dict) -> dict:
        """执行审查"""
        return {"status": "ok", "message": "Review engine initialized"}
