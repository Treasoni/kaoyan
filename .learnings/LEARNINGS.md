# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260618-001] best_practice

**Logged**: 2026-06-18T15:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
格式化笔记前先检查 RULES.md 的格式要求

### Details
在整理线性代数证明笔记时，直接用 `####` 标题格式写证明，没有先查阅 RULES.md。RULES.md 明确要求"证明内容统一使用 `> [!note]-` 折叠形式呈现"。事后才发现需要返工修改。

### Suggested Action
每次写入或修改笔记内容前，先快速浏览 `.learnings/RULES.md` 确认格式规范，避免返工。

---

## [LRN-20260618-002] best_practice

**Logged**: 2026-06-18T15:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
用户显式指令覆盖 RULES.md 中的一般性规则

### Details
RULES.md 记录"Callout 内不要用 `$$` 块级公式"，但用户明确要求将整个证明过程（含 `$$` 公式）放入 `> [!note]-` 折叠 callout 内。此时应以用户的显式指令为准，不被一般性规则阻塞。

### Suggested Action
当用户明确要求某种格式时，即使与 RULES.md 的一般性建议冲突，也应按用户要求执行。RULES.md 是经验总结而非硬性约束。

---

## [LRN-20260620-001] best_practice

**Logged**: 2026-06-20T07:41:35+00:00
**Priority**: medium
**Status**: resolved
**Area**: docs

### Summary
证明类内容的标题与正文都应放在同一个折叠块内

### Details
在 5.5.2-实对称矩阵的性质.md 中，第一次插入"性质 (2) 的证明"时用了 `### H3 标题` + 单独 `[!proof]` callout + 单独 `[!tip]` callout 的并列结构。用户反馈"证明内容+证明标题都要放在折叠块中啊"。

正确做法：使用嵌套 callout 包裹——外层 `> [!example]+ 标题`（`+` 表示默认折叠）作为可折叠入口，内层用 `> [!proof]` 和 `> [!tip]` 嵌套承载具体内容。这样打开笔记时默认收起证明区域，标题本身也是折叠块的一部分。

### Resolution
2026-06-20：经用户确认，规则已合并到 `RULES.md` Do 区（嵌套 callout 结构）与 Don't 区（单层 callout 禁 `$$` / 嵌套 callout 允许 `$$` 例外）。Watch For 区补充 `obsidian.proof_collapsible` 模式追踪。本条目关闭。

### Related Rules
- Pattern-Key: obsidian.proof_collapsible
- 已合并到 RULES.md

---
