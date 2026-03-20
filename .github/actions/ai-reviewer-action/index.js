const core = require('@actions/core');
const github = require('@actions/github');
const https = require('https');
const { spawn } = require('child_process');

async function run() {
  try {
    // 获取输入
    const githubToken = core.getInput('github-token', { required: true });
    const llmProvider = core.getInput('llm-provider') || 'deepseek';
    const reviewStyle = core.getInput('review-style') || 'professional';
    
    // 获取环境变量中的 API Key
    const apiKeys = {
      deepseek: process.env.DEEPSEEK_API_KEY,
      openai: process.env.OPENAI_API_KEY,
      anthropic: process.env.ANTHROPIC_API_KEY,
      qwen: process.env.QWEN_API_KEY,
      zhipuai: process.env.ZHIPUAI_API_KEY
    };
    
    const apiKey = apiKeys[llmProvider.toLowerCase()];
    if (!apiKey) {
      core.setFailed(`No API key found for provider: ${llmProvider}`);
      return;
    }
    
    const octokit = github.getOctokit(githubToken);
    const context = github.context;
    
    // 检查是否是 PR 事件
    if (context.eventName !== 'pull_request' && context.eventName !== 'push') {
      core.info('Not a pull request or push event, skipping');
      return;
    }
    
    // 获取代码变更
    const changes = await getChanges(octokit, context);
    
    if (!changes || changes.length === 0) {
      core.info('No changes found');
      return;
    }
    
    // 调用 LLM 进行审查
    const reviewResult = await reviewWithLLM(changes, {
      provider: llmProvider,
      apiKey: apiKey,
      style: reviewStyle
    });
    
    // 写入审查结果到 PR 评论
    if (context.eventName === 'pull_request') {
      await postReviewComment(octokit, context, reviewResult);
    }
    
    // 写入 Summary
    core.summary.addRaw(reviewResult).write();
    
  } catch (error) {
    core.setFailed(error.message);
  }
}

async function getChanges(octokit, context) {
  const { owner, repo } = context.repo;
  let changes = [];
  
  if (context.eventName === 'pull_request') {
    const prNumber = context.payload.pull_request.number;
    
    // 获取 PR diff
    const response = await octokit.rest.pulls.get({
      owner,
      repo,
      pull_number: prNumber,
      accept: 'application/vnd.github.v3.diff'
    });
    
    // 解析 diff
    const diffContent = response.data;
    const fileDiffs = parseDiff(diffContent);
    changes = fileDiffs;
    
  } else if (context.eventName === 'push') {
    // 获取 push 的 commit changes
    const commits = context.payload.commits;
    for (const commit of commits || []) {
      core.info(`Processing commit: ${commit.id}`);
    }
  }
  
  return changes;
}

function parseDiff(diffContent) {
  const files = [];
  const fileBlocks = diffContent.split(/^diff --git/m).filter(Boolean);
  
  for (const block of fileBlocks) {
    const lines = block.split('\n');
    let filePath = '';
    let diff = '';
    
    for (const line of lines) {
      if (line.startsWith('+++ b/')) {
        filePath = line.replace('+++ b/', '').trim();
      } else if (line.startsWith('@@')) {
        diff += line + '\n';
      } else if (diff || line.startsWith('+') || line.startsWith('-')) {
        diff += line + '\n';
      }
    }
    
    if (filePath) {
      files.push({ file: filePath, diff: diff.trim() });
    }
  }
  
  return files;
}

async function reviewWithLLM(changes, config) {
  // 简化版：生成审查提示
  const fileList = changes.map(c => `- ${c.file}`).join('\n');
  
  const prompt = `请审查以下代码变更:

${fileList}

请从以下几个方面进行审查:
1. 代码规范
2. 潜在错误
3. 安全风险
4. 性能问题
5. 改进建议

请简洁地给出审查结果。`;

  // 这里简化处理，实际应该调用 LLM API
  const result = `## 🔍 AI Code Review

### 审查的文件
${fileList}

### 审查模式: ${config.style}

**注意**: 这是简化版本，实际审查需要配置 LLM API。

### 建议
- 请配置 LLM API Key 以启用完整审查功能
- 支持 DeepSeek、OpenAI、Claude 等模型
`;

  return result;
}

async function postReviewComment(octokit, context, result) {
  const { owner, repo } = context.repo;
  const prNumber = context.payload.pull_request.number;
  
  await octokit.rest.issues.createComment({
    owner,
    repo,
    issue_number: prNumber,
    body: result
  });
  
  core.info('Review comment posted successfully');
}

run();
