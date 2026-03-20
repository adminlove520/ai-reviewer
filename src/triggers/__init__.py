"""
Triggers Module - 触发器
"""
from .gitea import GiteaWebhook
from .gitlab import GitLabWebhook

__all__ = ["GitLabWebhook", "GiteaWebhook"]
