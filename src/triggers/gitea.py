"""
Gitea Webhook 处理
"""
from typing import Optional
from pydantic import BaseModel

class GiteaPullRequest(BaseModel):
    """Gitea Pull Request"""
    id: int
    number: int
    title: str
    body: str
    state: str
    html_url: str
    head_branch: str
    base_branch: str

class GiteaPushEvent(BaseModel):
    """Gitea Push Event"""
    ref: str
    before: str
    after: str
    repository: dict
    pusher: dict
    commits: list

class GiteaWebhook:
    """Gitea Webhook 处理"""
    
    def __init__(self, token: str = None, base_url: str = None):
        self.token = token
        self.base_url = base_url or "https://gitea.com"
    
    def parse_pull_request(self, payload: dict) -> Optional[GiteaPullRequest]:
        """解析 Pull Request 事件"""
        if "pull_request" not in payload:
            return None
        
        pr = payload["pull_request"]
        
        return GiteaPullRequest(
            id=pr.get("id", 0),
            number=pr.get("number", 0),
            title=pr.get("title", ""),
            body=pr.get("body", ""),
            state=pr.get("state", ""),
            html_url=pr.get("html_url", ""),
            head_branch=pr.get("head", {}).get("ref", ""),
            base_branch=pr.get("base", {}).get("ref", "")
        )
    
    def parse_push(self, payload: dict) -> Optional[GiteaPushEvent]:
        """解析 Push 事件"""
        if "ref" not in payload:
            return None
        
        return GiteaPushEvent(
            ref=payload.get("ref", ""),
            before=payload.get("before", ""),
            after=payload.get("after", ""),
            repository=payload.get("repository", {}),
            pusher=payload.get("pusher", {}),
            commits=payload.get("commits", [])
        )
    
    def get_pull_request_diff(self, owner: str, repo: str, number: int, token: str) -> list:
        """获取 PR 的 diff"""
        import requests
        
        url = f"{self.base_url}/api/v1/repos/{owner}/{repo}/pulls/{number}"
        headers = {"Authorization": f"token {token}"}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                # 获取 diff
                diff_url = data.get("diff_url")
                if diff_url:
                    diff_response = requests.get(diff_url, timeout=30)
                    if diff_response.status_code == 200:
                        return self._parse_diff(diff_response.text)
        except Exception as e:
            print(f"Error getting PR diff: {e}")
        
        return []
    
    def _parse_diff(self, diff_text: str) -> list:
        """解析 diff 文本"""
        changes = []
        files = diff_text.split("diff --git")
        
        for file_diff in files:
            if not file_diff.strip():
                continue
            
            lines = file_diff.split("\n")
            file_path = ""
            diff_content = ""
            
            for line in lines:
                if line.startswith("+++ b/") or line.startswith("+++ "):
                    file_path = line.replace("+++ b/", "").replace("+++ ", "").strip()
                elif file_path:
                    diff_content += line + "\n"
            
            if file_path:
                changes.append({
                    "file": file_path,
                    "diff": diff_content.strip()
                })
        
        return changes
    
    def post_comment(self, owner: str, repo: str, number: int, body: str, token: str) -> bool:
        """在 PR 上评论"""
        import requests
        
        url = f"{self.base_url}/api/v1/repos/{owner}/{repo}/issues/{number}/comments"
        headers = {"Authorization": f"token {token}"}
        data = {"body": body}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            return response.status_code == 201
        except Exception as e:
            print(f"Error posting comment: {e}")
            return False
    
    def create_issue(self, owner: str, repo: str, title: str, body: str, token: str) -> bool:
        """创建 Issue"""
        import requests
        
        url = f"{self.base_url}/api/v1/repos/{owner}/{repo}/issues"
        headers = {"Authorization": f"token {token}"}
        data = {"title": title, "body": body}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            return response.status_code == 201
        except Exception as e:
            print(f"Error creating issue: {e}")
            return False
    
    def validate_token(self, token: str) -> bool:
        """验证 Gitea Token"""
        if not self.token:
            return True
        return token == self.token
