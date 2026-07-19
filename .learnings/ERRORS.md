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

## [ERR-20260719-007] note_update

**Logged**: 2026-07-19T20:50:51+08:00
**Priority**: high
**Status**: pending
**Area**: docs/electronics

### Summary
MOSFET 例题解析误写入工作区判断笔记，而不是用户期望的好题解析笔记。

### Error
```text
用户反馈：不是，是把笔记放到“.../02-场效应管及其放大电路/好题解析.md”啊
```

### Context
在整理用户上传的 MOSFET 输出特性曲线例题时，未先定位“好题解析.md”，而是把完整例题块插入 [[考研专业课/模拟电子技术/详细笔记/02-场效应管及其放大电路/02-MOSFET工作区判断]]。后续已将例题移动到 [[考研专业课/模拟电子技术/详细笔记/02-场效应管及其放大电路/好题解析.md]]，并清理原笔记中的误放区块。

### Suggested Action
涉及“题目/例题/好题解析/错题”时，写入前先检查目标文件是否应为好题解析或错题文件；用户明确给出目标路径后，不再按主题知识点笔记猜测目标。

### Related Rules
Pattern-Key: note_update.target_path_confirm

---

## [ERR-20260719-008] note_update

**Logged**: 2026-07-19T20:50:51+08:00
**Priority**: high
**Status**: pending
**Area**: docs/electronics

### Summary
好题解析初版遗漏题目原文和题目中的电路图、曲线图正文展示。

### Error
```text
用户反馈：我给的题目中不是有电路图和曲线图吗？你这里直接没了？
用户反馈：你的这个中没有题目
```

### Context
第一次写入好题解析时，只保留了解析、辅助图和折叠的原题整图，未把题干原文、输出特性曲线裁图、电路图裁图放在题目开头。后续已补充题目卡片、已知所求、题图拆解，并把原图裁成输出特性曲线与电路图分别嵌入正文。

### Suggested Action
图片题整理必须先完成“题目完整性检查”：题干、已知、所求、原题关键图、电路参数、曲线读数全部在正文可见；原题整图只能作为折叠溯源，不能替代正文关键图。

### Related Rules
Pattern-Key: problem_note.complete_card
Pattern-Key: docs.visual_source_coverage

---

## [ERR-20260719-009] tooling

**Logged**: 2026-07-19T20:50:51+08:00
**Priority**: medium
**Status**: pending
**Area**: docs/ops

### Summary
重排 Markdown 的 Python 写入脚本因 heredoc 内注释位置错误触发 SyntaxError。

### Error
```text
SyntaxError: invalid syntax
```

### Context
重排好题解析时，第一次 Python 脚本中有一行解释性文字没有以注释形式写入，导致脚本报错。幸好该次未覆盖目标文件，随后改用更简单的 raw string 写入并回读验证。

### Suggested Action
批量重写 Markdown 时继续使用 Python raw string，但脚本外说明不要混入 Python 代码块；写入前让构造逻辑尽量短，写入后必须回读关键段落和扫描控制字符。

### Related Rules
Pattern-Key: write_verify.latex_escape
Pattern-Key: ops.shell_quote_redirect

---
