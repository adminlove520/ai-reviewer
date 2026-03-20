"""
飞书消息推送
"""
import os
import json
import requests
from typing import Optional, List

class FeiShuSender:
    """飞书消息发送器"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("FEISHU_WEBHOOK_URL")
    
    def send_text(self, content: str) -> bool:
        """发送文本消息"""
        if not self.webhook_url:
            return False
        
        data = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        
        return self._send(data)
    
    def send_markdown(self, title: str, content: str) -> bool:
        """发送富文本消息"""
        if not self.webhook_url:
            return False
        
        data = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    },
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": content
                    }
                ]
            }
        }
        
        return self._send(data)
    
    def send_review_result(self, review_result: dict) -> bool:
        """发送审查结果"""
        summary = review_result.get("summary", "无审查结果")
        status = review_result.get("status", "unknown")
        
        markdown = f"""## 🔍 AI 代码审查结果

**状态**: {status}

**摘要**: 
{summary}

---
*由 ai-reviewer 发送*"""
        
        return self.send_markdown("AI 代码审查", markdown)
    
    def _send(self, data: dict) -> bool:
        """发送请求"""
        try:
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                timeout=10
            )
            result = response.json()
            return result.get("code") == 0
        except Exception as e:
            print(f"FeiShu send error: {e}")
            return False
