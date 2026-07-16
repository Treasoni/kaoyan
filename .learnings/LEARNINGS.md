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


## [LRN-20260716-012] best_practice

**Logged**: 2026-07-16T15:51:16+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Obsidian 拆分笔记恢复或重构后必须验证最终 `.md` 文件可见，而不是只确认备份文件存在

### Details
本次用户指出 BJT 与基本放大电路章节“内容少很多”。检查后发现 01-07 的拆分内容实际存在，但文件名停留在 `.md.bak_restructure`，导致 Obsidian 正常链接不可见，章节导读指向的 wikilink 也像是空转。恢复为 `.md` 后，章节内容立即可见，并进一步用链接扫描确认 missing links 为 0。

### Suggested Action
以后用户反馈“章节内容缺失、链接打不开、拆分版不完整”时，先检查目标目录是否存在 `.bak_restructure`、`.bak`、临时后缀或未落地的拆分文件；恢复后必须检查：目录下 `.md` 文件列表、章节导读 wikilink、missing links、文件大小与标题数量。不要只看整章版或备份文件就判断内容完整。

### Related Rules
Pattern-Key: obsidian.split_notes_visibility

---

## [LRN-20260716-013] best_practice

**Logged**: 2026-07-16T15:51:16+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
专业课章节补笔记要同时做“学习路线前置链路”和“附件图覆盖”审计

### Details
本次修复 BJT 章节时，用户指出学习路线不像正常学习顺序，随后又指出第 01 节“没图”。实际问题是：章节一开始直接进入放大思想与 Q 点，但缺少 BJT 器件基础、NPN/PNP、三电极、电流关系、输入输出特性等前置环节；同时附件目录中已有结构图、符号图、放大状态载流子图、输入/输出特性曲线，却没有嵌入到第 01 节。补齐文字路线后，还必须把关键图嵌入并写明“图的作用 + 关键标注 + 做题结论”。

### Suggested Action
以后整理模电/专业课章节时，不要只按已有标题补文字。先按“前置概念 → 器件/模型 → 工作区 → 静态 → 动态 → 题型”的学习链路审计目录；再扫描对应附件目录，把关键教材图嵌入到相关小节，并为每张关键图补“看什么/做题结论”。如果用户问“没图吗”，优先检查附件库，不要立刻重画或回答没有。

### Related Rules
Pattern-Key: electronics.chapter_route_visual_audit

---
