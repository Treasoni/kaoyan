# Errors

Command failures and integration errors.

---


## [ERR-20260719-010] note_update

**Logged**: 2026-07-19T21:34:24+08:00
**Priority**: medium
**Status**: resolved
**Area**: docs/obsidian

### Summary
Mermaid 流程图节点中直接使用 `<`、`<=`、括号和未加引号的中文文本，导致 Obsidian 渲染异常。

### Error
```text
用户反馈：flowchart 显示有问题
原始节点示例：B{vGS <= VGS(off) ?}、D{vDS < vGS - VGS(off) ?}
```

### Context
整理耗尽型 NMOS 工作区判断时，在 [[考研专业课/模拟电子技术/详细笔记/02-场效应管及其放大电路/02-MOSFET工作区判断]] 写入 Mermaid 流程图。节点文字未加引号，并直接使用 `<`、`<=`、`VGS(off)` 等容易被 Mermaid/Obsidian 误解析的字符。后续已改为给节点文本加双引号，并用 `≤`、`＜` 等更安全的显示符号。

### Suggested Action
以后在 Obsidian 笔记中写 Mermaid 流程图时，中文节点或含比较符号、括号、逗号、公式样文本的节点统一用双引号包裹；比较符优先写成 `≤`、`≥`、`＜`、`＞`，不要在节点标签里裸写 `<` 或 `<=`。

### Related Rules
Pattern-Key: obsidian.mermaid_node_label_escape

---

### Resolution
2026-07-19：已同步到 `.learnings/RULES.md` 的 Do / Don't / Watch For 区。

## [ERR-20260721-001] note_update

**Logged**: 2026-07-21T11:14:02+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/math

### Summary
重排 Markdown/LaTeX 笔记时，命令字符串经过 JSON/exec 层转义，导致 LaTeX 命令被污染成控制字符或错误文本。

### Error
```text
\boxed 被写成退格控制字符 + oxed；\text 被写成制表符 + ext。
控制字符扫描发现 11 处异常，后续手动替换修复。
```

### Context
在重排 [[考研数学/0-基础知识/高数必背公式.md]] 的 7.9 多元微分模块时，虽然写入后做了控制字符扫描，但初始写入仍使用了会经过 JSON 转义的命令文本，导致 \b、\t 这类序列在到达 Python 脚本前已经被解释为控制字符。问题已当场修复并重新扫描通过。

### Suggested Action
以后通过 exec/JSON 命令写入含 LaTeX 的 Markdown 时，不能只依赖 Python raw string；必须优先用外部脚本文件、占位符替换或 `chr(92)` 拼接反斜杠。写入后必须扫描控制字符，并回读检查 `\boxed`、`\text`、`\begin`、`\rvert` 等高风险命令。

### Related Rules
Pattern-Key: write_verify.json_latex_escape
Pattern-Key: write_verify.latex_escape

---

### Resolution
2026-07-21：已同步到 `.learnings/RULES.md` 的 Do / Don't / Watch For 区；以后写含 LaTeX 的长 Markdown 前采用占位符/`chr(92)` 或外部脚本，并把 `\boxed`、`\text` 纳入回读检查。

