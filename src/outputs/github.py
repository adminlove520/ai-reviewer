"""
GitHub 评论输出
"""
import os
from github import Github

class GitHubCommenter:
    """GitHub 评论发送器"""
    
    def __init__(self, token: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.github = Github(self.token) if self.token else None
    
    def post_pr_comment(self, repo: str, pr_number: int, body: str) -> bool:
        """在 PR 上评论"""
        if not self.github:
            return False
        
        try:
            repo_obj = self.github.get_repo(repo)
            pr = repo_obj.get_pull(pr_number)
            pr.create_issue_comment(body)
            return True
        except Exception as e:
            print(f"GitHub comment error: {e}")
            return False
    
    def post_commit_comment(self, repo: str, commit_sha: str, body: str) -> bool:
        """在 Commit 上评论"""
        if not self.github:
            return False
        
        try:
            repo_obj = self.github.get_repo(repo)
            repo_obj.get_commit(commit_sha).create_comment(body)
            return True
        except Exception as e:
            print(f"GitHub comment error: {e}")
            return False
    
    def send_review_result(self, repo: str, pr_number: int, review_result: dict) -> bool:
        """发送审查结果到 PR"""
        summary = review_result.get("summary", "无审查结果")
        status = review_result.get("status", "unknown")
        
        body = f"""## 🔍 AI Code Review

**状态**: {status}
**摘要**: {summary}

---
*由 ai-reviewer 自动生成*"""
        
        return self.post_pr_comment(repo, pr_number, body)
