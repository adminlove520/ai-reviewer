"""
企业微信消息推送
"""
import os
import json
import requests
from typing import Optional

class WeComSender:
    """企业微信消息发送器"""
    
    def __init__(self, webhook_key: str = None):
        self.webhook_key = webhook_key or os.getenv("WECOM_WEBHOOK_KEY")
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
    
    def _send(self, data: dict) -> bool:
        """发送请求"""
        if not self.webhook_key:
            return False
        
        url = f"{self.base_url}?key={self.webhook_key}"
        
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                timeout=10
            )
            result = response.json()
            return result.get("errcode") == 0
        except Exception as e:
            print(f"WeCom send error: {e}")
            return False
    
    def send_text(self, content: str, mentioned_list: list = None) -> bool:
        """发送文本消息"""
        data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or []
            }
        }
        return self._send(data)
    
    def send_markdown(self, content: str) -> bool:
        """发送 Markdown 消息"""
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        return self._send(data)
    
    def send_review_result(self, review_result: dict) -> bool:
        """发送审查结果"""
        summary = review_result.get("summary", "无审查结果")
        status = review_result.get("status", "unknown")
        
        markdown = f"""## 🔍 AI 代码审查结果

> 状态: {status}
> 摘要: {summary}

---
*由 ai-reviewer 发送*"""
        
        return self.send_markdown(markdown)
