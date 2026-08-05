# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260802-001] best_practice

**Logged**: 2026-08-02T21:09:11+08:00
**Priority**: high
**Status**: resolved
**Area**: ops/agent-config/prompt-cache

### Summary
多 agent 配置审计时，SessionStart hook 的重复注入必须全 profile 排查：本次 prompt-cache 审计发现 `.claude`、`.codex`、`.codebuddy` 三个 profile 同时注册 `read-learnings.sh` 与 `read_learnings.py` 两个等价的经验库注入 hook，每会话重复注入 ~20KB 内容。

### Details
prompt-cache-optimizer 审计以 `--platform both`（codex+claude）做只读检查时，初始只发现 `.claude` 与 `.codex` 各注册了两个 SessionStart hook（`read-learnings.sh` + `read_learnings.py`），输出内容几乎相同（同一份 RULES/ERRORS/LEARNINGS，仅标题语言不同），单次输出约 19.9KB。修改后用 `git diff` 与全库 grep 复核时，发现 `.codebuddy`（第三 profile）存在完全相同的重复；`.agent`（generic）无 hook 配置。按 CLAUDE.md 多 agent 一致性规则一并修复：三个 profile 统一保留 `read_learnings.py`，移除 `read-learnings.sh` 的注册；三个 `.sh` 脚本文件留在磁盘但已休眠。

### Suggested Action
审计或修改任何 agent profile 的 hook/启动注入时，先用 `grep -rn` 枚举全部 profile 目录（`.claude`、`.codex`、`.codebuddy`、`.agent` 等）并比对 SessionStart 注册的 hook 列表，同一内容只保留一个注入入口。改动后校验 JSON 语法并回读各 profile 配置，确认无悬挂引用。

### Related Rules
Pattern-Key: ops.hook_duplication

### Resolution
2026-08-02：用户确认同步后，已更新 `.learnings/RULES.md` 的 Do 区（多 agent profile hook 审计）与 Watch For 区（`ops.hook_duplication`）。


## [LRN-20260805-001] best_practice

**Logged**: 2026-08-05T11:56:14+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
用户明确其《必背知识》类笔记是「复习知识点」用的，不是背结论的：本次第 12 节「行列同数行列式」只有公式结论，被用户否回（"就给我一个结论？"），并要求先看现有源笔记再改写。

### Details
会话中先把特征值法推导补入第 11 节（用户提供内容，折叠块处理，无问题）。随后用户指出第 12 节「行列同数行列式（加边法）」只有必背公式 + 3 条干巴巴步骤，属于"背诵结论"，不符合"复习知识点、会做题"的用途。改写后的骨架：识别特征（含本质拆分：共同模板 + 对角线差额）→ 核心思想（为什么加边法）→ 操作模板（带中间矩阵的三步走）→ 必背公式 → 口诀 → 一句话理解公式 → 易错点。源笔记 1.4.4 中「加边 → 化爪形」的中间矩阵过程正是理解的关键，被压缩进操作模板而非删掉。

### Suggested Action
更新必背/速查类笔记时不允许只写公式结论：凡被定位为"操作/方法"的内容，必须补「核心思想（为什么这么做）」+「带中间状态的操作模板（怎么做）」；识别用行/列拆分等本质视角；长推导仍放 `> [!note]-` 折叠块、完整例题链接回源笔记。遇到结论型旧章节，按"识别特征 → 核心思想 → 操作模板 → 公式 → 口诀 → 易错点"骨架重构。

### Related Rules
Pattern-Key: notes.conclusion_only_reject

