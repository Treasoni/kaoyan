# Errors

Command failures and integration errors.

---

## [ERR-20260716-002] digest

**Logged**: 2026-07-16T10:55:08+08:00
**Priority**: high
**Status**: pending
**Area**: ops

### Summary
digest 压缩写入 RULES.md 时再次因 Python 字符串转义生成控制字符

### Error
```text
RULES.md 中 `\begin`、`\rvert` 被普通 Python 字符串解释为控制字符：\x08、\r
```

### Context
执行 digest 阈值压缩并重写 `.learnings/RULES.md` 时，最初使用普通三引号字符串保存包含 LaTeX 命令的规则文本，导致 `\begin` 和 `\rvert` 被转义污染。随后立即改用 raw string 写回 RULES.md，并扫描 `.learnings/RULES.md`、`.learnings/LEARNINGS.md`、`.learnings/ERRORS.md`、归档文件，确认控制字符为 0。

---

## [ERR-20260716-003] write

**Logged**: 2026-07-16T10:58:45+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
更新行列式递推笔记时再次出现 LaTeX 控制字符污染和渲染不稳定写法

### Error
```text
`\begin{vmatrix}` 被写成控制字符 + `egin{vmatrix}`，显示为 `�egin{vmatrix}`；同时 `\text{\textellipsis}` 在 Obsidian/MathJax 中显示不稳定。
```

### Context
整理“隐藏的递推公式”到 `线性代数/第一章：行列式/1.4-特殊行列式的计算/1.4.2-爪形行列式的变形.md` 时，第一次写入后虽然检查了控制字符并修复，后续替换整段时又因 Python 普通字符串中的 `\begin` 被解释为退格控制字符 `\x08`，导致回读显示异常。最终通过扫描控制字符、替换坏 `begin`、改用 `\cdots` / `\vdots` / `\ddots`，并检查 `\begin` / `\end` 数量匹配后修复。

---
