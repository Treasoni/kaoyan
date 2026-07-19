# Errors

Command failures and integration errors.

---

## [ERR-20260719-001] write_verify

**Logged**: 2026-07-19T16:12:20+08:00
**Priority**: high
**Status**: pending
**Area**: docs/math

### Summary
写入矩阵基本运算小节时，LaTeX `\times` 曾被转义污染为制表符加 `imes`。

### Error
```text
回读显示：$A=(a_{ij})_{m\times n}$ 被污染为 $A=(a_{ij})_{m\times n}$ 的制表符版本（表现为 `m\times n` 中的 `\t` 被解释）。
```

### Context
向 [[线性代数/必背知识.md]] 追加 `### 8. 矩阵基本运算` 时，首次回读发现 `m\times n` 被写成 `m\times n` 的控制字符污染；随后已修复，并执行控制字符扫描，确认异常控制字符为 0。

### Suggested Action
写入含 `\times`、`\rvert`、`\begin` 等 LaTeX 的 Markdown 时，继续优先使用 raw string、占位符或 `chr(92)` 构造反斜杠；写入后必须扫描控制字符并回读关键段落。

### Related Rules
Pattern-Key: write_verify.latex_escape

---

## [ERR-20260719-002] note_update

**Logged**: 2026-07-19T16:19:52+08:00
**Priority**: high
**Status**: pending
**Area**: docs/math

### Summary
伴随矩阵“代数余子式下标转置位置”这类位置关系，只写文字不够直观，应主动配图。

### Error
```text
用户反馈：图不给我，给我不是更方便我理解吗？
```

### Context
更新 [[线性代数/必背知识.md]] 的伴随矩阵小节时，先只写了“代数余子式 $A_{ij}$ 放到第 $j$ 行第 $i$ 列；下标是 $ji$，不是 $ij$”，没有主动生成位置对应图。后续已补充 [[线性代数/第二章：矩阵/assets/伴随矩阵下标转置位置图.svg]]，并在笔记中说明图的作用与做题结论。

### Suggested Action
遇到下标互换、行列位置对应、左右乘、转置/伴随等“空间位置关系”或“索引映射”知识点时，默认主动生成最小示意图，并配“图的作用 + 关键标注 + 做题结论”，不要等用户提醒。

### Related Rules
Pattern-Key: docs.proactive_visual_learning
Pattern-Key: docs.visual_source_coverage

---
