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
