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
