# Errors

Command failures and integration errors.

---

## [ERR-20260719-005] note_update

**Logged**: 2026-07-19T20:02:22+08:00
**Priority**: high
**Status**: pending
**Area**: docs/electronics

### Summary
MOSFET 工作区笔记补充公式后遗漏符号表。

### Error
```text
用户反馈：笔记缺少符号表
```

### Context
在 [[考研专业课/模拟电子技术/详细笔记/02-场效应管及其放大电路/02-MOSFET工作区判断]] 中补入输出特性、转移特性和恒流区公式后，未同步增加符号表。后续已补充默认折叠符号表，覆盖电压电流、阈值参数和端子下标。

### Suggested Action
公式密集的专业课笔记新增或重排后，检查是否已有符号表；没有则在 SOP 前补齐，并包含方向/极性、单位、做题用法。

### Related Rules
Pattern-Key: electronics.symbol_table_required
Pattern-Key: electronics.formula_symbol_explain

---

## [ERR-20260719-006] note_update

**Logged**: 2026-07-19T20:02:22+08:00
**Priority**: medium
**Status**: pending
**Area**: docs/obsidian

### Summary
符号表初始为展开形式，影响主学习流程紧凑度。

### Error
```text
用户反馈：符号表用折叠形式
```

### Context
给 MOSFET 工作区笔记新增符号表时，最初直接展开三张表。用户要求折叠后，已改为 `> [!info]- 符号表（点击展开）`。

### Suggested Action
长表格、补充说明和来源材料默认用折叠 callout；尤其放在笔记开头时，避免展开内容挤掉核心 SOP。

### Related Rules
Pattern-Key: obsidian.fold_supporting_material

---
