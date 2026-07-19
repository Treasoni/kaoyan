# Errors

Command failures and integration errors.

---

---

## [ERR-20260719-001] write_verify

**Logged**: 2026-07-19T15:10:19+0800
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
写入含 LaTeX 反斜杠的 Markdown 时发生转义污染，并出现一次 shell 引号失败。

### Error
```text
zsh: unmatched '
LaTeX 转义污染：\theta 被写成制表符 + heta；\boxed 被写成退格控制字符 + oxed；cases 换行反斜杠数量也被写错。
```

### Context
在把源笔记中的三对角型递推特征方程法压缩写入《线性代数必背知识.md》时，先用 shell 命令提取含中文括号和引号的标题导致引号失败；随后写入含 \theta、\boxed、\begin{cases} 的 Markdown 时出现转义污染。最终通过回读目标段落、扫描控制字符、逐行修复反斜杠数量解决。

### Suggested Action
写入含 LaTeX 命令的 Markdown 时，优先从源文件读取原文片段再做最小替换；写入脚本中使用 raw string、占位符或 `chr(92)` 生成反斜杠。每次写入后必须回读目标段落，并扫描控制字符，重点检查 \theta、\boxed、\begin、\rvert、cases 换行符。

### Related Rules
Pattern-Key: write_verify.latex_escape
