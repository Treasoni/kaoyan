# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260719-001] best_practice

**Logged**: 2026-07-19T16:12:20+08:00
**Priority**: medium
**Status**: pending
**Area**: docs/math

### Summary
线性代数必背笔记中，行列式记号优先使用 `\lvert A\rvert`，不要使用 `\det(A)`。

### Details
用户明确指出不想用 `\det(A)=0` 表示行列式；本次已将 [[线性代数/必背知识.md]] 中所有 `\det` 统一替换为 `\lvert ... \rvert` 形式，并确认剩余 `\det` 数量为 0。

### Suggested Action
后续更新线性代数必背/速查类笔记时，行列式统一写作 `\lvert A\rvert`、`\lvert AB\rvert`、`\lvert kA\rvert` 等形式；避免再写 `\det(A)`，并在写入后用 `grep '\\det'` 检查。

### Related Rules
Pattern-Key: math.determinant_notation_preference

---

## [LRN-20260719-002] best_practice

**Logged**: 2026-07-19T19:29:10+08:00
**Priority**: high
**Status**: pending
**Area**: docs/electronics

### Summary
连续手写笔记应保留原始书写顺序，不要按知识点把手写原图拆散到不同笔记。

### Details
整理 [[考研专业课/模拟电子技术/详细笔记/02-场效应管及其放大电路/01-FET核心思想与类型]] 与 [[考研专业课/模拟电子技术/详细笔记/02-场效应管及其放大电路/02-MOSFET工作区判断]] 时，最初按“知识点主题”把用户顺序书写的手写图拆到不同笔记。用户指出“我的手写笔记是按顺序写的”，随后已改为：结构化正文可按知识点分布，但手写原图统一按原始页序放在一个“手写原图顺序索引”折叠块中，其他主题笔记只回链说明。

### Suggested Action
以后处理多页连续手写笔记时，先判断它是否是同一次顺序书写的学习链：若是，则建立一个按页序排列的“手写原图顺序索引”；结构化笔记可分主题整理，但不要把原图页拆散，主题页只用 wikilink 回链到顺序索引。

### Related Rules
Pattern-Key: docs.handwritten_sequence_preserve

---

## [LRN-20260719-003] best_practice

**Logged**: 2026-07-19T19:29:10+08:00
**Priority**: medium
**Status**: pending
**Area**: docs/obsidian

### Summary
Obsidian 学习笔记中的图片默认使用正常阅读宽度，避免大图撑满页面影响学习节奏。

### Details
重排 FET 与 MOSFET 工作区笔记后，图片宽度一开始设置为 900、760、720、560，用户反馈“图片太大”。随后已调整为：正文教材图约 520，状态演变总览图约 600，手写原图约 420。这样的尺寸更适合在 Obsidian 中边看文字边看图。

### Suggested Action
以后为学习笔记嵌入图片时，默认采用阅读友好的宽度：普通教材图/曲线图约 500-540，总览型大图约 600，手写溯源图约 400-450；只有用户明确要求放大或图片细节确实看不清时才使用 700 以上宽度。写入后回读图片 embed 的 `|宽度` 参数。

### Related Rules
Pattern-Key: obsidian.image_reading_size

---
