# Errors

Command failures and integration errors.

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


## [ERR-20260716-004] write

**Logged**: 2026-07-16T15:51:16+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
用 `---` 作为 Markdown 区块替换边界误命中表格分隔线，导致章节导读残留旧表格

### Error
```text
替换 `## 学习路径` 区块时，以第一个 `---` 作为结束边界；但学习路径表格第二行正是 `| --- | --- | --- |`，导致替换提前截断，文件中残留旧学习路径表格片段。第 01 节插入也因锚点换行过窄第一次未生效。
```

### Context
修复 `考研专业课/模拟电子技术/详细笔记/03-BJT与基本放大电路/00-章节导读.md` 和 `01-放大思想与工作区.md` 时，第一次写入后回读发现导读中出现 `--- | --- | --- |` 残片，且第 01 节新增 BJT 基础没有插入。随后改用“从 `## 学习路径` 到下一个 `## 快速入口`”的标题边界替换，并用更稳定的标题锚点插入，回读验证成功。

---
