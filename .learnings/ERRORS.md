# Errors

Command failures and integration errors.

---

## [ERR-20260713-001] write_verify

**Logged**: 2026-07-13T11:29:16+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
用 Python 普通字符串写入 LaTeX Markdown 时发生转义污染

### Error
```
普通三引号字符串中的 \begin、\rvert 等 LaTeX 片段被解释为退格/回车等控制字符，首次写入后片段显示为异常字符和公式反斜杠缺失。
```

### Context
正在将错题21按图片题目重写到线性代数错题本。问题通过 sed 回读目标段落发现，随后改用 raw string 整段重写，并检查目标段落确认无控制字符残留。后续追加自我学习记录时也暴露出同类问题：未加引号的 shell heredoc 会执行反引号包裹内容，导致 `begin`、`rvert` 被当作命令；因此写入包含反引号/LaTeX 的 Markdown 时应使用 quoted heredoc（如 `<<'EOF'`）或 Python raw string。

---
