# Self-Learning Skills Template

这是一个可移植的自学习模板包，用于把 `digest` 和 `maintain-learnings` 带到任意 agent 项目。

它提供四件事：

- `digest`：记录本次任务中真实发生的学习点和错误。
- `maintain-learnings`：当 `.learnings/` 变长或错误反复出现时，先修 skill / 模板 / hook / 项目规则，再归档已解决记录。
- hooks：在会话开始时自动读取 `.learnings/RULES.md`、`.learnings/ERRORS.md` 和最近的 `.learnings/LEARNINGS.md`。
- 多 agent 同步守护：检查多个 agent skill 目录是否保留同等共享功能。

## Install

把 `templates/self-learning/` 复制到目标项目后，在目标项目根目录执行。默认兼容历史行为，会安装 Codex 与 Claude Code 两个内置 profile：

```bash
python3 templates/self-learning/install.py --target .
```

安装通用 profile：

```bash
python3 templates/self-learning/install.py --target . --profile generic
```

安装到任意 agent 目录：

```bash
python3 templates/self-learning/install.py --target . --custom-agent myagent:.my-agent/skills:.my-agent/hooks
```

对于 Windows 盘符路径或需要复用的自定义布局，优先写一个与 `profiles/*.yaml` 字段一致的 scalar YAML profile：

```bash
python3 templates/self-learning/install.py --target . --profile-file /path/to/myagent.yaml
```

只安装内置单侧 profile：

```bash
python3 templates/self-learning/install.py --target . --profile codex
python3 templates/self-learning/install.py --target . --profile claude
```

如果不想安装 hooks：

```bash
python3 templates/self-learning/install.py --target . --profile generic --no-hooks
```

## Built-In Profiles

| Profile | Skills | Hooks | Entry Rules |
| --- | --- | --- | --- |
| `codex` | `.agents/skills` | `.codex/hooks` | `AGENTS.md` |
| `claude` | `.claude/skills` | `.claude/hooks` | `CLAUDE.md` |
| `generic` | `.agent/skills` | `.agent/hooks` | `AGENTS.md` |

Generic/custom profile 不会生成未知 agent 的配置文件；安装器会复制 `read_learnings.py` 和 `read-learnings.sh`，并输出需要接入到该 agent hook 系统的命令。

`--overwrite` 只更新安装器管理的 skill 和 hook 脚本；已有 `.learnings/` 记录和无关 hook 配置始终保留。

## Project Rules Snippet

把 `AGENTS.snippet.md` 中的内容合并进目标项目的入口规则文件，例如 `AGENTS.md`、`CLAUDE.md`、`INSTRUCTIONS.md` 或团队自定义规范。

## Commands

审计经验库：

```bash
python3 <skills-dir>/maintain-learnings/scripts/audit_learnings.py --root . --skills-dir <skills-dir> --rules-file <entry-file> --hooks-path <hooks-dir>
```

Codex 内置 profile 示例：

```bash
python3 .agents/skills/maintain-learnings/scripts/audit_learnings.py --root . --skills-dir .agents/skills --rules-file AGENTS.md --hooks-path .codex/hooks
```

Claude Code 内置 profile 示例：

```bash
python3 .claude/skills/maintain-learnings/scripts/audit_learnings.py --root . --skills-dir .claude/skills --rules-file CLAUDE.md --hooks-path .claude/hooks
```

检查多个 agent profile 的共享 skill 是否一致：

```bash
python3 .agents/skills/maintain-learnings/scripts/sync_platform_skills.py --root . --skill maintain-learnings
python3 .agents/skills/maintain-learnings/scripts/sync_platform_skills.py --root . --platform generic=.agent/skills --base-platform agents --compare-platform generic --skill maintain-learnings
```

从一个 profile dry-run 同步到另一个 profile：

```bash
python3 .agents/skills/maintain-learnings/scripts/sync_platform_skills.py --root . --from-platform agents --to-platform claude --skill maintain-learnings
```

确认后应用：

```bash
python3 .agents/skills/maintain-learnings/scripts/sync_platform_skills.py --root . --from-platform agents --to-platform claude --skill maintain-learnings --apply
```

## Customize

- 把 `AGENTS.snippet.md` 中的 `<PROJECT_NAME>`、`<PRIMARY_OUTPUT>`、`<WORKFLOW>` 替换成目标项目自己的名称。
- 如果目标项目已有 hook 配置，不要直接覆盖；合并其中的 read-learnings command 即可。
- `agents/openai.yaml` 是 OpenAI UI 元数据，只应留在需要它的 profile 中。
- Windows 或非 POSIX 环境优先使用 `read_learnings.py`；有 Bash 的 Linux/macOS/WSL/Git Bash 也可以使用 `read-learnings.sh`。
