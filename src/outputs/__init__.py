"""
Outputs Module - 消息输出器
"""
from .dingtalk import DingTalkSender
from .feishu import FeiShuSender
from .wecom import WeComSender
from .github import GitHubCommenter

__all__ = ["DingTalkSender", "FeiShuSender", "WeComSender", "GitHubCommenter"]
