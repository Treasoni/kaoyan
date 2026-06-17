# Errors

Command failures and integration errors.

---

## [ERR-20260617-001] obsidian-callout-math

**Logged**: 2026-06-17
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
Callout 内 `$$` 紧跟 `[!type]` 导致数学公式不渲染

### Error
```
> [!important] $$
> \pmb{A}^2 = l \pmb{A}
> $$
```
Obsidian 将 `$$` 解析为 callout 标题文字，数学块未渲染。

### Context
将两个笔记合并时，复制了原始 callout 格式，未注意 `$$` 位置问题。

### Suggested Fix
```markdown
> [!important]
>
> $$\pmb{A}^2 = l \pmb{A}$$
```
`$$` 必须另起一行，与 `[!type]` 之间用空行分隔。

### Metadata
- Reproducible: yes
- Related Files: 线性代数/第五章：矩阵相似理论/5.2-秩为1矩阵专题/5.2.2-秩为1矩阵的性质与结论.md
- Tags: obsidian, callout, math, render-failure

---
