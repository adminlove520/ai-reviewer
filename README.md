# ai-reviewer

基于大模型的自动化代码审查工具 v2.0

## 核心特性

- 🚀 **GitHub Workflow 支持** - 无需 VPS，Action 直接运行
- 🤖 **AI Agent 集成** - 支持 OpenClaw/Claude Code
- 🛡️ **安全专项审计** - 集成 skill-dfyx_code_security_review
- 🔧 **代码修复建议** - 自动生成修复方案

## 功能

- 多模型支持 (DeepSeek/OpenAI/Claude/Qwen/ZhipuAI/MiniMax)
- 多平台 Webhook (GitHub/GitLab/Gitea)
- 多风格审查 (专业/毒舌/绅士/幽默)
- 消息推送 (钉钉/企业微信/飞书)

## 快速开始

### GitHub Workflow (推荐)

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: adminlove520/ai-reviewer-action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          llm-provider: deepseek
```

### Docker 部署

```bash
docker run -d -p 5001:5001 \
  -e DEEPSEEK_API_KEY=xxx \
  adminlove520/ai-reviewer
```

## 开发

```bash
# 克隆项目
git clone https://github.com/adminlove520/ai-reviewer

# 安装依赖
pip install -r requirements.txt

# 运行
python api.py
```

## License

MIT
