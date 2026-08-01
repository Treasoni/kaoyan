# Errors

Command failures and integration errors.

---

## [ERR-20260728-001] diagram_generation

**Logged**: 2026-07-28T21:36:33+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/electronics/diagrams

### Summary
生成固定偏置共射动态指标标准图时出现 BJT 微变等效图拓扑误连。

### Error
左上角微变等效图把基极节点和集电极节点误连，等效为输入端与输出端短接；输出端 $u_o$ 画法也容易误读成端口短接。

### Context
用户提供五页手写笔记，要求整理并放入共射动态指标笔记。生成标准图时没有先查标准电路图画法并写节点网表，只凭视觉布局手搓 SVG，导致拓扑错误进入笔记。用户指出“感觉图画错了”后复核并修正。

### Resolution
2026-07-28：已重新查标准资料、修正 SVG/PNG，并把“先查标准画法 + 节点网表 + 拓扑检查”同步到 RULES。

---
## [ERR-20260801-001] wikilink_assumption

**Logged**: 2026-08-01T12:15:00+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/wikilink

### Summary
新条目最初沿用旧错题本里「章节名式」wikilink，凭记忆写 `[[4.1 向量组及其线性相关性]]`，Glob 验证才发现文件不存在。

### Error
创建好题28索引行时最初按错题本既有风格写了 `[[4.1 向量组及其线性相关性]]`，实际 vault 内不存在该文件（真实文件夹为 `4.1-向量的基本概念`、`4.3-线性相关、线性无关与线性表示` 等编号式）。

### Context
整理「循环累加型向量组」错题到第四章错题本时，复制了同文件里旧链接的章节名式写法。写入前按「生成 wikilink 前先用 Glob 确认目标文件存在」规则做了 Glob 验证，纠正为 `[[4.3.1-线性相关与无关定义]]`，未造成新坏链接；但审计暴露整个错题本 90 处同类历史遗留坏链接。

### Resolution
已用 fix_links.py 批量修复 90 处，复审计 0 残留。教训：不要沿用同文件里已有的旧式链接，每个 wikilink 都必须独立 Glob 验证。

---
