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
