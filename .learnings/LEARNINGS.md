# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260718-001] best_practice

**Logged**: 2026-07-18T19:20:31+0800
**Priority**: medium
**Status**: resolved
**Area**: docs

### Summary
以后处理用户提供的手写笔记，默认采用“主笔记提取重构 + 保留手写原图溯源”的混合结构。

### Details
整理增强型 NMOS 的四页手写推导时，正文使用统一的三状态标准图承载“无沟道、感生沟道、漏端夹断前兆”的主线；四张手写原图按内容分配到对应章节的折叠来源区，并逐张补了图的作用与转写结论。用户随后明确确认，这应成为以后接收手写笔记时的默认组织方式：正文服务检索、复习和做题，原图保留推理、纠错痕迹和个人理解。

### Suggested Action
先建立“原图页/关键图 → 正文章节”的覆盖清单；正文提取为结构化文字，按需配标准图或 AI 重绘图；原图保留在对应段落，重复内容可折叠为“手写来源”，并保留每张关键图的读图结论。

### Related Rules
Pattern-Key: docs.handwritten_hybrid

### Resolution
2026-07-18T19:31:50+0800：用户明确确认将该混合方式设为后续手写笔记的默认规则，已同步到 `.learnings/RULES.md` 的 Do 与 Watch For。

---

## [LRN-20260718-002] best_practice

**Logged**: 2026-07-18T19:30:35+0800
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
生成或更新学习内容时，应主动判断加入图示或图片描述是否更利于理解。

### Details
用户指出抽水做功这类内容只写公式不够直观。以后生成数学、专业课等学习笔记时，不能只按文字/公式输出；应先从学习效果角度判断是否需要图示：如果图能帮助定位变量、空间关系、变化趋势、易错方向或步骤流程，就应生成图并嵌入笔记，同时补充图的作用、关键标注和做题结论。

### Suggested Action
每次生成或更新学习内容前增加“图示价值判断”：若内容涉及几何位置、物理过程、函数/曲线、流程、结构关系、电路或容易混淆的变量方向，就主动生成 SVG/Excalidraw/数学图像等合适图片并嵌入 Obsidian 笔记；图片旁必须配“图的作用 + 关键标注 + 学习/做题结论”。

### Related Rules
Pattern-Key: docs.proactive_visual_learning

### Resolution
2026-07-18：用户明确要求将该做法作为以后生成内容的习惯，已同步到 `.learnings/RULES.md` 的 Do 与 Watch For。

---
