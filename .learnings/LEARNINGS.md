# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260719-004] best_practice

**Logged**: 2026-07-19T20:02:22+08:00
**Priority**: high
**Status**: pending
**Area**: docs/electronics

### Summary
专业课公式密集笔记应在正文前提供符号表，尤其是 MOSFET 工作区这类多电压、多下标内容。

### Details
在整理 [[考研专业课/模拟电子技术/详细笔记/02-场效应管及其放大电路/02-MOSFET工作区判断]] 时，正文已加入 $v_{GS}$、$v_{DS}$、$v_{GD}$、$V_{TN}$、$K_n$、$I_{D0}$ 等符号和公式，但一开始没有集中符号表，导致用户反馈“笔记缺少符号表”。随后已在判断 SOP 前补充符号表，按“电压与电流 / 阈值与器件参数 / 下标与端子”分组。

### Suggested Action
以后整理专业课公式密集笔记时，若出现 5 个以上核心符号或多个相近下标，先在正文前补一个符号表；首次出现核心公式时必须说明变量物理意义、方向/极性约定、单位或做题用法。

### Related Rules
Pattern-Key: electronics.symbol_table_required
Pattern-Key: electronics.formula_symbol_explain

---

## [LRN-20260719-005] best_practice

**Logged**: 2026-07-19T20:02:22+08:00
**Priority**: medium
**Status**: pending
**Area**: docs/obsidian

### Summary
长符号表适合用 Obsidian 默认折叠 callout，避免挤占主学习流程。

### Details
补入 MOSFET 符号表后，符号表内容较长，用户继续要求“符号表用折叠形式”。随后已改为 `> [!info]- 符号表（点击展开）`，使符号表默认折叠，主线从判断 SOP 开始更清爽。

### Suggested Action
以后符号表、长速查表、手写来源、补充推导等支持性材料超过约 10 行时，优先用默认折叠 callout；主线学习内容保持展开，辅助材料点击查看。

### Related Rules
Pattern-Key: obsidian.fold_supporting_material

---

## [LRN-20260719-006] best_practice

**Logged**: 2026-07-19T20:50:51+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/electronics

### Summary
好题解析类笔记必须按“题目完整卡片 + 题图 + 答案速览 + SOP + 分步解析 + 易错点”组织，不能只写解法。

### Details
本次整理 MOSFET 输出特性例题时，第一次写入内容只有解析、辅助负载线图和折叠原题整图，遗漏了题目原文与用户给出的关键图示在正文中的呈现。用户连续指出“没有题目”“电路图和曲线图没了”，说明好题解析笔记的入口信息不完整，会降低复习时的可读性和溯源能力。

### Suggested Action
以后处理题目/错题/好题解析时，先写完整题目卡片：题目原文、已知与所求、原题关键图、必要的裁剪/重绘图、答案速览，再展开 SOP 与分步解析。若题目来自图片，必须先检查题干、图、电路参数、曲线读数是否都进入正文。

### Related Rules
Pattern-Key: problem_note.complete_card
Pattern-Key: docs.visual_source_coverage


### Resolution
2026-07-19：已同步到 `.learnings/RULES.md` 的 Do 与 Watch For 区。
---

## [LRN-20260719-007] best_practice

**Logged**: 2026-07-19T20:50:51+08:00
**Priority**: medium
**Status**: resolved
**Area**: docs/obsidian

### Summary
用户给出明确目标笔记或更正目标路径后，必须立即以该路径为唯一写入目标，并清理误放内容。

### Details
用户最初要求“整理放入改笔记中”时目标不够明确，我将例题写入了 MOSFET 工作区判断笔记。用户随后明确指出应放入 [[考研专业课/模拟电子技术/详细笔记/02-场效应管及其放大电路/好题解析.md]]，之后才移动内容并清理误放区块。该问题说明：当任务是“题目解析/好题解析”时，不能仅凭当前主题笔记猜目标，应优先查找同目录的好题解析、错题本或用户显式路径。

### Suggested Action
写入题目解析前先确认目标文件：若用户给出路径，必须回读该文件并写入；若用户未给路径但同目录存在“好题解析.md/错题本.md”，优先考虑该类文件，必要时询问。误写到其他笔记时，要移动到正确目标并从原文件删除误放内容，最后回读验证。

### Related Rules
Pattern-Key: note_update.target_path_confirm
Pattern-Key: markdown.section_replace_boundary


### Resolution
2026-07-19：已同步到 `.learnings/RULES.md` 的 Do 与 Watch For 区。
---
