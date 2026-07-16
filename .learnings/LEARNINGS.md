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

## [LRN-20260716-011] best_practice

**Logged**: 2026-07-16T10:58:45+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
数学例题讲解写入笔记时必须先补全题目本体，再写解析与递推过程

### Details
本次给线性代数“爪形行列式的变形”补充隐藏递推公式时，第一版只写了解法推导，没有在折叠块前保留原题矩阵和题目要求，导致复习时无法独立自测。随后用户指出“题目呢？”，才补充 `> [!example]- 例题：2015 数一隐藏递推行列式`、原题矩阵、求 D_n 和提示。对数学例题、错题、截图题而言，题目本体是解析成立的上下文，不能只保存方法。

### Suggested Action
以后向笔记写入“例题/错题/递推公式/题目解析”时，默认结构为：题目块可见或单独折叠展示，随后才是解析折叠块；必须包含题设、要求、关键提示或选项。写入后回读时检查是否满足“看到该段就能独立做题”，不能只有解法没有题目。

### Related Rules
Pattern-Key: math.problem_context_required

---
