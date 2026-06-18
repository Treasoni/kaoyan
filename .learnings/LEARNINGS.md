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
