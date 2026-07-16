# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260716-010] best_practice

**Logged**: 2026-07-16T10:55:08+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
题目解析、示例解析和错题正确解法区块适合统一改为 Obsidian 默认折叠 callout

### Details
本次用户要求“笔记中的题目解析都用折叠形式”。处理线性代数第一章行列式目录时，最有效的做法不是折叠题干或个人错因，而是只折叠解析过程：示例计算、经典例题解法、递推推导后的求解过程、克拉默法则详细计算、错题本中的“正确解法/答案”区块。个人块 `[!personal]` 保持原样，避免覆盖用户个人理解；题目本身保持可见，方便快速自测。写入后需要额外检查 callout 内表格前是否有 `>` 空行、表格 LaTeX 管道符、奇数 `$` 和控制字符。

### Suggested Action
以后用户要求“题目解析折叠/答案折叠/解析收起”时，默认采用 `> [!note]- 题目解析：...`：题干与错因保持可见，解法步骤和最终答案放入折叠块；若折叠块内含表格，写后必须执行 callout 表格空行和 LaTeX 管道符校验。不要把 `[!personal]` 个人笔记块一并折叠或改写。

### Related Rules
Pattern-Key: obsidian.problem_solution_collapsible

---
