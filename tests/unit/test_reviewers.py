"""
Simplified tests - run without complex imports
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from src.core.config import ReviewConfig, LLMConfig
        from src.reviewers.base import ReviewContext, CodeChange
        from src.outputs import DingTalkSender, FeiShuSender
        print("✓ All imports successful")
    except Exception as e:
        print(f"✗ Import failed: {e}")
        raise

def test_config():
    """Test config"""
    from src.core.config import ReviewConfig, LLMConfig
    
    config = ReviewConfig()
    assert config.review_style == "professional"
    print("✓ Config test passed")

def test_code_change():
    """Test CodeChange"""
    from src.reviewers.base import CodeChange
    
    change = CodeChange(
        file_path="test.py",
        diff="+print('hello')",
        additions=1,
        deletions=0
    )
    assert change.file_path == "test.py"
    print("✓ CodeChange test passed")

def test_review_context():
    """Test ReviewContext"""
    from src.reviewers.base import ReviewContext, CodeChange
    
    change = CodeChange(
        file_path="test.py",
        diff="+print('hello')",
        additions=1,
        deletions=0
    )
    
    context = ReviewContext(
        trigger_type="test",
        platform="github",
        event_type="pull_request",
        changes=[change],
        metadata={"pr_number": 1}
    )
    
    assert context.trigger_type == "test"
    assert len(context.changes) == 1
    print("✓ ReviewContext test passed")

if __name__ == "__main__":
    print("Running tests...")
    test_imports()
    test_config()
    test_code_change()
    test_review_context()
    print("\n✓ All tests passed!")
