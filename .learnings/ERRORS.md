# Errors

Command failures and integration errors.

---


## [ERR-20260724-001] beautify_write

**Logged**: 2026-07-24T20:05:52+08:00
**Priority**: high
**Status**: pending
**Area**: docs/obsidian/handwritten-notes

### Summary
未先看懂手写图片内容，就按当前笔记标题把“直接耦合/阻容耦合”误写进“分压式射极偏置”。

### Error
图片主题识别错误：把手写图中的直接耦合与阻容耦合内容误归类为分压式射极偏置，并据此重排笔记。

### Context
用户要求重新排版当前笔记。当前 note 是“04-分压式射极偏置”，但附件中的三张手写图实际标题和内容是“两种实用放大电路”、直接耦合和阻容耦合。应先查看图片并识别真实知识点，再决定写入位置。

---


## [ERR-20260725-001] note_reconstruction

**Logged**: 2026-07-25T21:29:41+08:00
**Priority**: high
**Status**: pending
**Area**: docs/obsidian/handwritten-notes

### Summary
手写笔记写入后没有主动回看整篇标题结构，导致动态图解法 initially 被挂成局部附属小节。

### Error
整理“图解法分析共射电压放大倍数”时，第一次写入只检查了主题落点、公式、图片链接和图示质量，没有主动判断新增内容是否应该升为独立学习模块。结果把动态图解法放成 `5.5.1`，用户追问后才重排为独立的 `5.6` 模块。

### Context
用户要求提取手写笔记、完善整理并放入合适笔记。该内容与前面的“图解法求固定偏置 Q 点”构成“静态定 Q → 动态看小信号移动”的连续学习链条。正确做法应是在写入后立即回看标题树，主动完成模块升格和顺号。

---
