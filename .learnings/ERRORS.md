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

## [ERR-20260713-002] write_verify

**Logged**: 2026-07-13T11:57:54+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
修正错题题目文件时，对 raw string 与 LaTeX 反斜杠的处理不够稳

### Error
```
在准备重写错题24题干时，多次生成未完成的 Python 脚本草稿；同时一度误判 raw string 会导致 Markdown 中出现双反斜杠。实际回读显示文件内容是正常的单反斜杠 LaTeX 命令，幸好未写入错误草稿。
```

### Context
正在同步更新 `线性代数/第五章：矩阵相似理论/错题题目.md` 的错题24题干。最终通过 `grep -n "## 错题24" -A24` 回读确认内容正确。

---
