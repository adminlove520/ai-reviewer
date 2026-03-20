"""
Triggers Module - 触发器
"""
from .gitlab import GitLabWebhook
from .gitea import GiteaWebhook

__all__ = ["GitLabWebhook", "GiteaWebhook"]
