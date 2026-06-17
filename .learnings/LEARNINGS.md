# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260617-001] best_practice

**Logged**: 2026-06-17
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Obsidian callout 内写 `$$` 数学块时，`$$` 必须另起一行，不能紧跟 `[!type]`

### Details
错误写法：`> [!important] $$` — Obsidian 将 `$$` 当作 callout 标题，数学块不渲染。
正确写法：
```markdown
> [!important]
>
> $$\pmb{A}^2 = l \pmb{A}$$
```

### Suggested Action
1. Callout 内的 `$$` 必须与 `[!type]` 之间有空行
2. 多行 `$$...$$` 块改用单行 `$$...$$` 更稳定
3. 合并笔记时检查原始 callout 格式

### Metadata
- Source: user_feedback
- Tags: obsidian, callout, math, render
- Pattern-Key: obsidian.callout_math
- Recurrence-Count: 1
- First-Seen: 2026-06-17
- Related Files: 线性代数/第五章：矩阵相似理论/5.2-秩为1矩阵专题/5.2.2-秩为1矩阵的性质与结论.md

---
