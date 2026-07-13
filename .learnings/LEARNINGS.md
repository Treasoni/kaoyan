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

## [LRN-20260705-001] best_practice

**Logged**: 2026-07-05T16:30:00+08:00
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
证明过程统一使用 `> [!note]-` 单一折叠块（默认折叠）

### Details
为高数必背公式.md 中的四个三角积分（∫tan x、∫cot x、∫sec x、∫csc x）添加证明过程时，第一次写成零散 `> [!tip]` + 普通段落形式，用户反馈"证明过程放到 note 块中啊"；改为 `> [!note]` 后又反馈"我想用的是折叠形式的啊"。

用户明确表态"以后如果是某个东西的证明过程都是用这样的折叠"——即统一使用 `> [!note]-` 单一折叠 callout 包裹整个证明内容（默认折叠），不再使用嵌套 callout 结构（外层 `> [!example]+` + 内层 `> [!proof]/[!tip]/[!note]`）。

### Suggested Action
凡是"证明/推导"类内容，统一使用 `> [!note]-` 单一折叠块。Callout 内可包含 `$$` 公式、列表、表格（注意表格前后留空行）。不要再使用嵌套 callout 结构。

### Resolution
2026-07-05：经用户确认，原 RULES.md Do 区"嵌套 callout 结构"规则**被替换**为新的"证明过程统一用 `> [!note]-` 单一折叠块"规则。同时清除了 LRN-20260618-002（用户显式指令覆盖规则——本就是临时性观察，现已升级为显式规则）。Watch For 区保留 `obsidian.proof_collapsible` 模式追踪，更新计数为 2x。本条目关闭。

### Related Rules
- Pattern-Key: obsidian.proof_collapsible
- 替换原嵌套 callout 规则
- 已合并到 RULES.md

---

## [LRN-20260713-001] best_practice

**Logged**: 2026-07-13T11:29:16+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
图片纠正错题时，必须按新题完整重算并回读渲染结果

### Details
本次用户指出错题21的题目应以图片为准。修正时不能只替换题干，还要重新计算特征多项式、二重根分类、验秩矩阵和对角化结论。虽然新旧题最终的参数值恰好相同，但验秩矩阵完全不同；如果只沿用旧解析，会留下隐性错误。另一次写入时用 Python 普通字符串插入 LaTeX，导致 `\begin`、`\rvert` 等转义被误处理，幸好通过回读目标段落发现并用 raw string 重写修正。

### Suggested Action
处理用户基于图片/截图修正题目时：先按图片重新识别题目，再完整重算关键步骤；写入含大量 LaTeX 的 Markdown 时优先使用 raw string 或 here-doc 单引号，并在写入后必须回读目标段落检查是否出现控制字符、反斜杠丢失或公式变形。

---

## [LRN-20260713-002] best_practice

**Logged**: 2026-07-13T11:57:54+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
修正错题本题干后，必须同步检查错题题目索引文件

### Details
用户提醒：线性代数错题本中的错题21、错题24按图片修正后，`线性代数/第五章：矩阵相似理论/错题题目.md` 中对应题干也需要同步更新。本次检查发现错题21已经是新版，但错题24仍停留在旧的定参版本，导致“错题本解析”和“错题题目练习入口”不一致。

### Suggested Action
每次修改错题本中某道题的题干、参数或选项时，同时检索并更新同目录的 `错题题目.md` 对应条目；完成后回读两个文件的对应段落，确认题干一致。

---

## [LRN-20260713-003] best_practice

**Logged**: 2026-07-13T11:59:11+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
用户质疑解析正确性时，必须用目标等式直接验算

### Details
用户追问“你确定错题24的解析对了吗？”时，不能仅凭前面推导口头确认。对于相似变换题，最可靠的验算是直接计算目标等式：验证 `P^(-1)AP=B`，或等价地验证 `AP=PB`。本次用精确分数计算确认当前 `P` 满足 `P^(-1)AP=B`，因此解析正确。

### Suggested Action
遇到用户质疑数学解析、矩阵计算或最终答案时，优先做可复核的代入验算；对于相似变换矩阵题，直接验算 `P^(-1)AP=B` 或 `AP=PB`，并在回复中明确说明验算结果。

---
