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

## [LRN-20260617-002] best_practice

**Logged**: 2026-06-17
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
删除 Obsidian 文件时必须使用 safe-delete skill 清理悬空链接

### Details
直接用 `rm` 删除文件后，vault 中可能残留指向已删除文件的 wikilinks，导致链接失效。safe-delete skill 会扫描所有引用并自动清理。

### Suggested Action
1. 删除任何 Obsidian 笔记文件前，先调用 safe-delete skill
2. 不要直接使用 `rm` 命令删除 .md 文件

### Metadata
- Source: user_feedback
- Tags: obsidian, safe-delete, cleanup
- Pattern-Key: obsidian.file_deletion
- Recurrence-Count: 1
- First-Seen: 2026-06-17

---

## [LRN-20260617-003] best_practice

**Logged**: 2026-06-17
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Obsidian callout 内的 `$$` 块级公式应移到 callout 外面

### Details
callout 块内嵌套 `$$...$$` 块级公式会导致 Obsidian 渲染异常。正确的做法是将公式移到 callout 块外面，保留 callout 的标题和说明文字在块内。

### Suggested Action
1. `$$` 块级公式不要放在 callout 内部
2. callout 内只放行内公式 `$...$`
3. 合并笔记时检查并修复此类问题

### Metadata
- Source: user_feedback
- Tags: obsidian, callout, math, render
- Pattern-Key: obsidian.callout_block_math
- Recurrence-Count: 2
- First-Seen: 2026-06-17
- Related Files: 线性代数/第五章：矩阵相似理论/5.3-矩阵相似/5.3-矩阵相似.md

---

## [LRN-20260617-004] best_practice

**Logged**: 2026-06-17
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
证明内容统一使用折叠形式（`> [!note]-`）呈现

### Details
用户明确要求：关于证明的内容，都用折叠形式。这样保持笔记简洁，不被长篇证明打断，需要时点击展开查看。

### Suggested Action
1. 整理笔记时，证明部分用 `> [!note]-` 包裹
2. 主结论和证明分离，便于复习

### Metadata
- Source: user_feedback
- Tags: obsidian, callout, proof, format
- Pattern-Key: obsidian.proof_collapse
- Recurrence-Count: 1
- First-Seen: 2026-06-17
- Related Files: 线性代数/第五章：矩阵相似理论/5.3-矩阵相似/5.3-矩阵相似.md

---
