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
