# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260719-001] best_practice

**Logged**: 2026-07-19T16:12:20+08:00
**Priority**: medium
**Status**: pending
**Area**: docs/math

### Summary
线性代数必背笔记中，行列式记号优先使用 `\lvert A\rvert`，不要使用 `\det(A)`。

### Details
用户明确指出不想用 `\det(A)=0` 表示行列式；本次已将 [[线性代数/必背知识.md]] 中所有 `\det` 统一替换为 `\lvert ... \rvert` 形式，并确认剩余 `\det` 数量为 0。

### Suggested Action
后续更新线性代数必背/速查类笔记时，行列式统一写作 `\lvert A\rvert`、`\lvert AB\rvert`、`\lvert kA\rvert` 等形式；避免再写 `\det(A)`，并在写入后用 `grep '\\det'` 检查。

### Related Rules
Pattern-Key: math.determinant_notation_preference

---
