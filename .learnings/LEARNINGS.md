# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260719-004] best_practice

**Logged**: 2026-07-19T19:58:08+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/notes

### Summary
学习笔记中的符号应在笔记开头统一说明，方便查找和复习。

### Details
用户在更新 FET 核心思想笔记后明确反馈：“笔记中的符号要在笔记开头说明，方便我查找和复习”。这说明符号密集型笔记不能只在正文首次出现处零散解释；应在标题和导航后放一个“符号速查/符号说明”区块，把端口、变量、参数、缩写、方向/极性约定和做题用法集中起来。

### Suggested Action
后续整理专业课、数学等符号密集笔记时，默认在笔记开头加入“符号速查”折叠块或小节；先列出本节会出现的关键符号，再进入正文。尤其是电路/模电笔记，要把 G/D/S/B、$v_{GS}$、$i_D$、$g_m$、阈值电压、方向约定等放在开头，便于复习前快速查表。

### Resolution
已同步到 `.learnings/RULES.md` 的 Do 与 Watch For：新增 Pattern-Key `notes.symbol_quick_reference`。

### Related Rules
Pattern-Key: notes.symbol_quick_reference

---
