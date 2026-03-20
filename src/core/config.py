"""
Configuration
"""
from typing import Optional

from pydantic import BaseModel


class LLMConfig(BaseModel):
    provider: str = "deepseek"
    api_key: str = ""
    base_url: Optional[str] = None
    model: str = "deepseek-chat"

class ReviewConfig(BaseModel):
    llm: LLMConfig = LLMConfig()
    review_style: str = "professional"
    supported_extensions: str = ".py,.js,.ts,.java,.go,.php"
