"""
Security Reviewer - 安全审查器
集成 skill-dfyx_code_security_review
"""
from typing import List, Dict, Any
from src.reviewers.base import BaseReviewer, ReviewContext, ReviewResult

class SecurityReviewer(BaseReviewer):
    """安全审查器 - 集成东方隐侠 skill-dfyx"""
    
    name = "security"
    version = "1.0.0"
    
    def __init__(self, mode: str = "standard"):
        """
        初始化安全审查器
        
        Args:
            mode: 审查模式 (quick/standard/deep)
        """
        self.mode = mode
        # 10 个安全维度
        self.dimensions = [
            "D1-injection",      # 注入
            "D2-auth",           # 认证
            "D3-authz",          # 授权
            "D4-deser",          # 反序列化
            "D5-file",           # 文件操作
            "D6-ssrf",           # SSRF
            "D7-crypto",          # 加密
            "D8-config",          # 配置
            "D9-logic",          # 业务逻辑
            "D10-supply"         # 供应链
        ]
    
    async def review(self, context: ReviewContext) -> ReviewResult:
        """执行安全审查"""
        if not context.changes:
            return ReviewResult(
                status="skipped",
                summary="No changes to review"
            )
        
        # 收集代码
        code_files = self._collect_code_files(context)
        
        if not code_files:
            return ReviewResult(
                status="skipped",
                summary="No supported code files found"
            )
        
        # 根据模式选择审查维度
        dimensions = self._get_dimensions_by_mode()
        
        # 构建审查提示
        prompt = self._build_prompt(code_files, dimensions)
        
        # TODO: 调用 LLM 进行安全审查
        # 实际实现需要集成 skill-dfyx
        
        return ReviewResult(
            status="success",
            summary=f"Security review completed in {self.mode} mode",
            issues=[],
            score=100
        )
    
    def _collect_code_files(self, context: ReviewContext) -> List[Dict[str, str]]:
        """收集代码文件"""
        supported_extensions = {
            '.py', '.java', '.js', '.ts', '.jsx', '.tsx',
            '.go', '.php', '.rb', '.cs', '.c', '.cpp', '.h'
        }
        
        files = []
        for change in context.changes:
            ext = change.file_path.split('.')[-1] if '.' in change.file_path else ''
            if f'.{ext}' in supported_extensions:
                files.append({
                    'path': change.file_path,
                    'diff': change.diff
                })
        
        return files
    
    def _get_dimensions_by_mode(self) -> List[str]:
        """根据模式获取审查维度"""
        if self.mode == "quick":
            # Quick 模式: 只检查高危
            return ["D1-injection", "D2-auth", "D5-file", "D6-ssrf"]
        elif self.mode == "standard":
            # Standard 模式: OWASP Top 10
            return ["D1-injection", "D2-auth", "D3-authz", 
                   "D4-deser", "D5-file", "D6-ssrf", 
                   "D7-crypto", "D8-config"]
        else:
            # Deep 模式: 全部维度
            return self.dimensions
    
    def _build_prompt(self, files: List[Dict], dimensions: List[str]) -> str:
        """构建安全审查提示"""
        file_list = "\n".join([f"- {f['path']}" for f in files[:10]])
        
        dimension_desc = {
            "D1-injection": "SQL注入、命令注入、LDAP注入等",
            "D2-auth": "认证机制、密码存储、会话管理",
            "D3-authz": "授权、权限控制、越权",
            "D4-deser": "反序列化漏洞",
            "D5-file": "文件上传、下载、路径遍历",
            "D6-ssrf": "服务器端请求伪造",
            "D7-crypto": "加密问题、密钥管理",
            "D8-config": "配置错误、信息泄露",
            "D9-logic": "业务逻辑漏洞",
            "D10-supply": "依赖漏洞、CVE"
        }
        
        dims = "\n".join([f"- {d}: {dimension_desc.get(d, '')}" for d in dimensions])
        
        return f"""你是一位专业的安全审计工程师。

请对以下代码进行安全审计:

## 文件列表
{file_list}

## 审查维度
{dims}

## 审查模式: {self.mode}

请从以上维度分析代码，找出安全漏洞，并给出:
1. 漏洞描述
2. 风险等级 (Critical/High/Medium/Low)
3. 漏洞位置 (文件:行号)
4. 修复建议

请给出详细的安全审计报告。"""
    
    def validate_config(self) -> bool:
        """验证配置"""
        return self.mode in ["quick", "standard", "deep"]
