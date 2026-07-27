# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260727-001] best_practice

**Logged**: 2026-07-27T20:03:47+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/handwritten-notes

### Summary
处理用户多页手写笔记时，必须逐页展示与识别，不能只给一张总结图或把原图全部折叠到来源里。

### Details
本次整理“图解法分析共射电压放大倍数”三页手写笔记时，先把内容整理进笔记并生成了标准总结图，但最终汇报和笔记呈现偏向一张重绘图，导致用户质疑“三张图为什么只给一张，是否完整看懂”。复核后确认三页实际承担不同逻辑层：第 1 页是固定偏置共射电路的静态基础，第 2 页是输入负载线随交流输入平移，第 3 页是输出特性族线、反相波形与 $A_u=-10$。最终补救方案是在正文中加入“5.6.0 三页手写图识别卡”，每页原图直接可见，并配视觉盘点、解决的问题、公式链、做题结论和待确认项，再接标准重绘图与公式总结。

### Suggested Action
以后处理用户多页手写笔记、截图或教材图并写入笔记时，默认采用“逐页识别卡 → 标准图/重绘图 → 公式链 → 做题结论 → 标题树回看”的结构：每一页原图都要在正文中直接对应一个知识层，写清视觉盘点、该页解决的问题、关键公式/逻辑链、待确认项和做题结论；原图不能只折叠为来源，也不能被一张总结图替代。完成后回读标题树，确认新增内容符合学习顺序。

### Related Rules
Pattern-Key: handwritten_note.page_card_mapping
Pattern-Key: docs.visual_source_coverage
Pattern-Key: notes.learning_route_coherence

### Resolution
2026-07-27：已同步到 `.learnings/RULES.md` 的 Do / Watch For 区。

---
