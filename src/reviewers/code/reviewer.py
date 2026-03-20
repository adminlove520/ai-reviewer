"""
Code Reviewer - 代码审查器
"""
from typing import List

from src.llm.factory import Factory
from src.reviewers.base import BaseReviewer, ReviewContext, ReviewResult


class CodeReviewer(BaseReviewer):
    """代码审查器"""

    name = "code"
    version = "1.0.0"

    def __init__(self, style: str = "professional"):
        self.style = style
        self.llm = Factory().getClient()

    async def review(self, context: ReviewContext) -> ReviewResult:
        """执行代码审查"""
        if not context.changes:
            return ReviewResult(
                status="skipped",
                summary="No changes to review"
            )

        # 收集所有 diff
        all_diffs = []
        for change in context.changes:
            diff_text = f"File: {change.file_path}\n\n{change.diff}"
            all_diffs.append(diff_text)

        # 调用 LLM 审查
        prompt = self._build_prompt(all_diffs)
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": prompt}
        ]

        try:
            result = self.llm.completions(messages)
            return ReviewResult(
                status="success",
                summary=result,
                issues=[],
                score=85
            )
        except Exception as e:
            return ReviewResult(
                status="error",
                summary=f"Review failed: {str(e)}",
                issues=[],
                score=0
            )

    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        prompts = {
            "professional": "你是一位资深的软件开发工程师，专注于代码审查。",
            "sarcastic": "你是一位毒舌的代码审查员，批评要直接不留情面。",
            "gentle": "你是一位温和的代码审查员，建议要委婉。",
            "humorous": "你是一位幽默的代码审查员，要轻松有趣。"
        }
        return prompts.get(self.style, prompts["professional"])

    def _build_prompt(self, diffs: List[str]) -> str:
        """构建审查提示词"""
        diff_text = "\n\n---\n\n".join(diffs[:5])  # 限制数量

        return f"""请审查以下代码变更:

{diff_text}

请从以下几个方面进行审查:
1. 代码规范
2. 潜在错误
3. 安全风险
4. 性能问题
5. 改进建议

请给出审查结果和改进建议。"""
