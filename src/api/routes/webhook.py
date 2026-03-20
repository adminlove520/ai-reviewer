"""
FastAPI Routes - Webhook
"""
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from src.core.engine import ReviewEngine
from src.core.config import ReviewConfig

router = APIRouter()

class WebhookPayload(BaseModel):
    event: str
    platform: str
    data: dict

@router.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "service": "ai-reviewer"}

@router.post("/webhook/github")
async def github_webhook(request: Request):
    """GitHub Webhook 处理"""
    # 获取 GitHub event
    event = request.headers.get("X-GitHub-Event", "")
    payload = await request.json()
    
    if event == "pull_request":
        action = payload.get("action", "")
        if action in ["opened", "synchronize"]:
            pr = payload.get("pull_request", {})
            return {
                "status": "ok",
                "event": "pull_request",
                "action": action,
                "pr_number": pr.get("number"),
                "title": pr.get("title")
            }
    
    return {"status": "ignored", "event": event}

@router.post("/review")
async def review(payload: WebhookPayload):
    """通用审查接口"""
    engine = ReviewEngine(ReviewConfig())
    result = await engine.review(payload.dict())
    return result
