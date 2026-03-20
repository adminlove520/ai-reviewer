"""
钉钉消息推送
"""
import json
import os

import requests


class DingTalkSender:
    """钉钉消息发送器"""

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("DINGTALK_WEBHOOK_URL")

    def send_text(self, content: str, at_mobiles: list = None) -> bool:
        """发送文本消息"""
        if not self.webhook_url:
            return False

        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": False
            }
        }

        try:
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                timeout=10
            )
            return response.json().get("errcode") == 0
        except Exception as e:
            print(f"DingTalk send error: {e}")
            return False

    def send_markdown(self, title: str, content: str) -> bool:
        """发送 Markdown 消息"""
        if not self.webhook_url:
            return False

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "content": content
            }
        }

        try:
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                timeout=10
            )
            return response.json().get("errcode") == 0
        except Exception as e:
            print(f"DingTalk send error: {e}")
            return False

    def send_review_result(self, review_result: dict) -> bool:
        """发送审查结果"""
        summary = review_result.get("summary", "无审查结果")
        status = review_result.get("status", "unknown")

        markdown = f"""## 🔍 AI 代码审查结果

**状态**: {status}
**摘要**: {summary}

---
*由 ai-reviewer 发送*"""

        return self.send_markdown("AI 代码审查", markdown)
