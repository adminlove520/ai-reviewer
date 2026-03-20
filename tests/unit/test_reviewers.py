"""
Unit tests for reviewers
"""
import pytest
from src.reviewers.code import CodeReviewer
from src.reviewers.security import SecurityReviewer
from src.reviewers.base import ReviewContext, CodeChange

class TestCodeReviewer:
    """代码审查器测试"""
    
    def test_initialization(self):
        """测试初始化"""
        reviewer = CodeReviewer(style="professional")
        assert reviewer.name == "code"
        assert reviewer.style == "professional"
    
    def test_system_prompts(self):
        """测试系统提示词"""
        reviewer = CodeReviewer(style="sarcastic")
        prompt = reviewer._get_system_prompt()
        assert "毒舌" in prompt or "sarcastic" in prompt.lower()
    
    def test_validate_config(self):
        """测试配置验证"""
        reviewer = CodeReviewer()
        assert reviewer.validate_config() is True

class TestSecurityReviewer:
    """安全审查器测试"""
    
    def test_initialization(self):
        """测试初始化"""
        reviewer = SecurityReviewer(mode="quick")
        assert reviewer.name == "security"
        assert reviewer.mode == "quick"
    
    def test_dimensions_by_mode(self):
        """测试模式对应的维度"""
        reviewer = SecurityReviewer(mode="quick")
        dims = reviewer._get_dimensions_by_mode()
        assert len(dims) == 4  # quick 模式 4 个维度
        
        reviewer = SecurityReviewer(mode="standard")
        dims = reviewer._get_dimensions_by_mode()
        assert len(dims) == 8  # standard 模式 8 个维度
        
        reviewer = SecurityReviewer(mode="deep")
        dims = reviewer._get_dimensions_by_mode()
        assert len(dims) == 10  # deep 模式 10 个维度
    
    def test_validate_config(self):
        """测试配置验证"""
        reviewer = SecurityReviewer(mode="quick")
        assert reviewer.validate_config() is True
        
        reviewer = SecurityReviewer(mode="invalid")
        assert reviewer.validate_config() is False

class TestReviewContext:
    """审查上下文测试"""
    
    def test_empty_context(self):
        """测试空上下文"""
        context = ReviewContext(
            trigger_type="test",
            platform="github",
            event_type="pull_request",
            changes=[],
            metadata={}
        )
        assert context.trigger_type == "test"
        assert len(context.changes) == 0
    
    def test_context_with_changes(self):
        """测试带变更的上下文"""
        changes = [
            CodeChange(
                file_path="test.py",
                diff="+print('hello')",
                additions=1,
                deletions=0
            )
        ]
        
        context = ReviewContext(
            trigger_type="test",
            platform="github",
            event_type="pull_request",
            changes=changes,
            metadata={"pr_number": 1}
        )
        
        assert len(context.changes) == 1
        assert context.changes[0].file_path == "test.py"
        assert context.metadata["pr_number"] == 1

class TestCodeChange:
    """代码变更测试"""
    
    def test_code_change_creation(self):
        """测试代码变更创建"""
        change = CodeChange(
            file_path="test.py",
            diff="+print('hello')",
            additions=1,
            deletions=0
        )
        
        assert change.file_path == "test.py"
        assert change.diff == "+print('hello')"
        assert change.additions == 1
        assert change.deletions == 0
