"""
Outputs Module - 消息输出器
"""
from .dingtalk import DingTalkSender
from .feishu import FeiShuSender
from .github import GitHubCommenter
from .wecom import WeComSender

__all__ = ["DingTalkSender", "FeiShuSender", "WeComSender", "GitHubCommenter"]
