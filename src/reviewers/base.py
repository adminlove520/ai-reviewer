"""
Base Reviewer - 审查器基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel

class CodeChange(BaseModel):
    """代码变更"""
    file_path: str
    diff: str
    additions: int = 0
    deletions: int = 0

class ReviewContext(BaseModel):
    """审查上下文"""
    trigger_type: str  # webhook, workflow, agent, cli
    platform: str  # github, gitlab, gitea
    event_type: str  # pull_request, push
    changes: List[CodeChange]
    metadata: Dict[str, Any] = {}

class ReviewResult(BaseModel):
    """审查结果"""
    status: str
    summary: str
    issues: List[Dict[str, Any]] = []
    score: int = 100

class BaseReviewer(ABC):
    """审查器基类"""
    
    name: str = "base"
    version: str = "1.0.0"
    
    @abstractmethod
    async def review(self, context: ReviewContext) -> ReviewResult:
        """执行审查"""
        pass
    
    def validate_config(self) -> bool:
        """验证配置"""
        return True
