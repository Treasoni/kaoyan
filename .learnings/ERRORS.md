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
