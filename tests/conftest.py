"""
Test fixtures for ai-reviewer
"""
import pytest
from src.reviewers.code import CodeReviewer
from src.reviewers.security import SecurityReviewer
from src.reviewers.base import ReviewContext, CodeChange

@pytest.fixture
def sample_review_context():
    """示例审查上下文"""
    changes = [
        CodeChange(
            file_path="test.py",
            diff="""--- a/test.py
+++ b/test.py
@@ -1,3 +1,5 @@
+import os
+
 def hello():
-    print("hello")
+    print("hello world")
+    return True
""",
            additions=3,
            deletions=1
        )
    ]
    
    return ReviewContext(
        trigger_type="test",
        platform="github",
        event_type="pull_request",
        changes=changes,
        metadata={}
    )

@pytest.fixture
def code_reviewer():
    """代码审查器"""
    return CodeReviewer(style="professional")

@pytest.fixture
def security_reviewer():
    """安全审查器"""
    return SecurityReviewer(mode="quick")
