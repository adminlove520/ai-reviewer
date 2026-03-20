# ai-reviewer

> 基于大模型的自动化代码审查工具 v2.0

[![GitHub stars](https://img.shields.io/github/stars/adminlove520/ai-reviewer)](https://github.com/adminlove520/ai-reviewer)
[![License](https://img.shields.io/github/license/adminlove520/ai-reviewer)](LICENSE)

## 核心特性

- 🚀 **GitHub Workflow 支持** - 无需 VPS，Action 直接运行
- 🤖 **AI Agent 集成** - 支持 OpenClaw/Claude Code
- 🛡️ **安全专项审计** - 集成 skill-dfyx_code_security_review
- 🔧 **代码修复建议** - 自动生成修复方案
- 💬 **多风格审查** - 专业/毒舌/绅士/幽默

## 支持的模型

| 模型 | 支持 |
|------|------|
| DeepSeek | ✅ |
| OpenAI | ✅ |
| Claude | ✅ |
| 通义千问 | ✅ |
| 智谱AI | ✅ |
| MiniMax | ✅ |

## 快速开始

### 1. GitHub Workflow (推荐)

在仓库中创建 `.github/workflows/ai-review.yml`:

```yaml
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

### 2. Docker 部署

```bash
docker run -d -p 5001:5001 \
  -e DEEPSEEK_API_KEY=your_key \
  adminlove520/ai-reviewer
```

### 3. 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python api.py
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 服务状态 |
| `/api/health` | GET | 健康检查 |
| `/api/webhook/github` | POST | GitHub Webhook |
| `/api/review` | POST | 通用审查 |

## 项目结构

```
ai-reviewer/
├── src/
│   ├── api/           # API 层
│   ├── core/          # 核心引擎
│   ├── reviewers/     # 审查器
│   │   └── code/     # 代码审查
│   ├── triggers/      # 触发器
│   ├── outputs/      # 输出器
│   ├── llm/          # LLM 客户端
│   └── utils/        # 工具
├── .github/workflows/ # GitHub Workflows
└── api.py            # 入口
```

## 配置

通过环境变量配置:

```bash
# LLM 配置
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=xxx
OPENAI_API_KEY=xxx
ANTHROPIC_API_KEY=xxx

# 审查配置
REVIEW_STYLE=professional  # professional/sarcastic/gentle/humorous
SUPPORTED_EXTENSIONS=.py,.js,.ts,.java,.go,.php
```

## 开发

```bash
# 克隆项目
git clone https://github.com/adminlove520/ai-reviewer

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest

# 运行服务
python api.py
```

## License

MIT License
