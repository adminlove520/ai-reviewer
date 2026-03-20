"""
GitLab Webhook 处理
"""
from typing import Optional
from pydantic import BaseModel

class GitLabMergeRequest(BaseModel):
    """GitLab Merge Request"""
    id: int
    iid: int
    title: str
    description: str
    source_branch: str
    target_branch: str
    state: str
    web_url: str

class GitLabPushEvent(BaseModel):
    """GitLab Push Event"""
    ref: str
    before: str
    after: str
    user_name: str
    user_username: str
    project: dict
    commits: list

class GitLabWebhook:
    """GitLab Webhook 处理"""
    
    def __init__(self, token: str = None, base_url: str = None):
        self.token = token
        self.base_url = base_url or "https://gitlab.com"
    
    def parse_merge_request(self, payload: dict) -> Optional[GitLabMergeRequest]:
        """解析 Merge Request 事件"""
        if "object_attributes" not in payload:
            return None
        
        attrs = payload["object_attributes"]
        
        return GitLabMergeRequest(
            id=attrs.get("id", 0),
            iid=attrs.get("iid", 0),
            title=attrs.get("title", ""),
            description=attrs.get("description", ""),
            source_branch=attrs.get("source_branch", ""),
            target_branch=attrs.get("target_branch", ""),
            state=attrs.get("state", ""),
            web_url=attrs.get("url", "")
        )
    
    def parse_push(self, payload: dict) -> Optional[GitLabPushEvent]:
        """解析 Push 事件"""
        if "ref" not in payload:
            return None
        
        return GitLabPushEvent(
            ref=payload.get("ref", ""),
            before=payload.get("before", ""),
            after=payload.get("after", ""),
            user_name=payload.get("user_name", ""),
            user_username=payload.get("user_username", ""),
            project=payload.get("project", {}),
            commits=payload.get("commits", [])
        )
    
    def get_merge_request_changes(self, project_id: str, mr_iid: int, token: str) -> list:
        """获取 MR 的变更"""
        import requests
        
        url = f"{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes"
        headers = {"PRIVATE-TOKEN": token}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                changes = []
                for change in data.get("changes", []):
                    changes.append({
                        "file": change["new_path"],
                        "diff": change["diff"],
                        "additions": change.get("new_file", False),
                        "deletions": change.get("deleted_file", False)
                    })
                return changes
        except Exception as e:
            print(f"Error getting MR changes: {e}")
        
        return []
    
    def post_comment(self, project_id: str, mr_iid: int, body: str, token: str) -> bool:
        """在 MR 上评论"""
        import requests
        
        url = f"{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
        headers = {"PRIVATE-TOKEN": token}
        data = {"body": body}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            return response.status_code == 201
        except Exception as e:
            print(f"Error posting comment: {e}")
            return False
    
    def validate_token(self, token: str) -> bool:
        """验证 GitLab Token"""
        if not self.token:
            return True
        return token == self.token
