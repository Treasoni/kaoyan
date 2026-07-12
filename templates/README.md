# Prompt Cache Templates

这组文件可直接复用到任何同时使用 Codex、Claude Code 或两者的项目中。

| 文件 | 用途 |
| --- | --- |
| `prompt-cache-bootstrap.sh` | 自动安装规则、更新入口文件，并检查常见缓存破坏项 |
| `prompt-cache-rules.md` | 可复制到 `rules/prompt-cache.md` 的完整规则 |
| `AGENTS-cache-snippet.md` | 可粘贴到 `AGENTS.md` 的精简入口规则 |
| `prompt-cache-playbook.md` | 设计原理、反例、指标与落地检查清单 |

## Quick Start

先检查目标项目，不会写入文件：

```bash
bash templates/prompt-cache-bootstrap.sh --check --platform both --target /path/to/project
```

确认后安装 Codex 和 Claude Code 两套规则：

```bash
bash templates/prompt-cache-bootstrap.sh --apply --platform both --target /path/to/project
```

只配置一个平台时，将 `--platform both` 换成 `codex` 或 `claude`。

## What The Script Changes

- Codex：创建 `.codex/rules/common/prompt-cache.md`，并向 `AGENTS.md` 追加带标记的入口规则。
- Claude Code：创建 `.claude/rules/common/prompt-cache.md`，并向 `CLAUDE.md` 追加带标记的入口规则。
- 检查 `prompts/`、`.codex/prompts/`、`.claude/prompts/` 中可能放错位置的时间戳、UUID、git 状态等动态字段。

脚本不会改写现有业务提示词，也不会覆盖已存在的规则文件。重复执行是安全的：它会保留现有规则，并识别已插入的入口块。

## Recommended Workflow

1. 执行 `--check` 查看缺失项和警告。
2. 执行 `--apply` 安装基础规范。
3. 把高频提示词整理到 `prompts/`，使用稳定前缀和末尾参数块。
4. 根据 `prompt-cache-playbook.md` 接入 token、缓存读取 token、延迟和费用指标。
