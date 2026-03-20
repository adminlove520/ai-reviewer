"""
FastAPI Main Entry
"""
from fastapi import FastAPI
from src.api.routes import webhook
from src.utils.log import logger

app = FastAPI(
    title="AI Reviewer",
    description="基于大模型的自动化代码审查工具",
    version="2.0.0"
)

# 注册路由
app.include_router(webhook.router, prefix="/api", tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "AI Reviewer is running", "version": "2.0.0"}

@app.on_event("startup")
async def startup():
    logger.info("AI Reviewer starting up...")

@app.on_event("shutdown")
async def shutdown():
    logger.info("AI Reviewer shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
