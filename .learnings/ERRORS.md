# Errors

Command failures and integration errors.

---

## [ERR-20260715-001] write

**Logged**: 2026-07-15T17:04:04+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
写入错题93时 Python 字符串转义导致脚本语法错误与索引行控制字符污染

### Error
```text
SyntaxError: EOL while scanning string literal
SyntaxError: invalid syntax
索引行出现控制字符：\x0c、\x08、\t，表现为 \frac、\textrm、\big、\text 被污染
```

### Context
尝试用 Python 字符串构造包含大量 LaTeX 的错题93正文和索引行，并在脚本中做反斜杠归一化。多次失败后改用 quoted heredoc 写入正文；随后通过控制字符扫描发现索引行仍有污染，最终删除坏残留行并改成无复杂 LaTeX 的简洁索引描述。

---
