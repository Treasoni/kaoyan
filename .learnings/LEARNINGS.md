# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260720-001] best_practice

**Logged**: 2026-07-20T10:47:27+08:00
**Priority**: medium
**Status**: pending
**Area**: docs/obsidian/math

### Summary
处理“必背公式/速查”类数学笔记时，先确认该文件在用户工作流中的真实定位：若用户实际用作快速复习笔记，不能只按狭义公式表压缩。

### Details
本次更新 [[考研数学/0-基础知识/高数必背公式.md]] 时，先从多元函数基本概念笔记中提取邻域、连续、偏导数内容。对偏导数部分，初始建议偏向“只保留定义、公式和少量易错点”；用户指出该笔记本身就是快速复习用。由此确认：速查/必背类文件不等于只放公式，还应保留考场启动规则、易错判断链、方法选择口诀、必要定义式和来源链接，尤其是偏导数这种结构识别型内容。

### Suggested Action
以后更新“必背公式/速查/快速复习”类笔记前，先判断目标文件是“纯公式表”还是“快速复习卡”。若是快速复习卡，按“定义/公式 + 口诀 + 易错判断 + 做题启动步骤 + 来源链接”抽取；避免过度压缩成只有公式，导致复习时不能直接启动做题。

### Related Rules
Pattern-Key: notes.quick_review_extract
Pattern-Key: notes.source_first_extract

---

## [LRN-20260721-001] correction

**Logged**: 2026-07-21T11:14:02+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/math

### Summary
写入含 LaTeX 的长 Markdown 时，除了 Python 字符串转义，还要防 JSON/exec 传参层提前解释反斜杠序列。

### Details
本次重排 [[考研数学/0-基础知识/高数必背公式.md]] 时，LaTeX 命令 `\boxed` 和 `\text` 在命令传递过程中分别触发了退格和制表符转义，说明“Python raw string”本身不覆盖 JSON/exec 外层转义风险。必须从输入源头避免裸写高风险反斜杠序列。

### Suggested Action
长段 Markdown/LaTeX 写入优先使用独立脚本文件、占位符替换或 `chr(92)` 构造反斜杠；写后同时做控制字符扫描与关键 LaTeX 命令回读检查，尤其检查 `\boxed`、`\text`、`\begin`、`\rvert`。

### Related Rules
Pattern-Key: write_verify.json_latex_escape
Pattern-Key: write_verify.latex_escape

---

### Resolution
2026-07-21：已同步到 `.learnings/RULES.md`。

## [LRN-20260721-002] best_practice

**Logged**: 2026-07-21T15:32:50+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/math/linear-algebra

### Summary
抽象数学题解析不能只给符号推导，要先解释“这一步在干什么”，再给坐标、列向量和计算细节。

### Details
用户反馈 [[线性代数/第一章：行列式/错题本.md]] 错题21原解析“构造 $A$ 在新基下的矩阵”看不懂。原版本虽然步骤正确，但偏教材式：直接定义 $v_1,v_2,v_3$、写 $AP=PB$、推出相似，缺少“新基是什么”“$B$ 的每一列为什么这么写”“为什么可以用 $B$ 代替 $A$ 算”的人话桥接。改写后按“先说人话含义 → 每个基向量逐列算坐标 → 解释 $AP=PB$ → 再计算行列式”的顺序，用户确认更清楚。

### Suggested Action
以后写考研数学题目解析，尤其是线代抽象矩阵、相似、特征值、基变换、坐标表示类题目时，默认采用“人话入口 + 分步坐标/对象解释 + 公式推导 + 一句话记忆”的结构。不要只写正确推导链；每出现一个抽象对象（如新基、表示矩阵、相似、$AP=PB$、$\lvert A-E\rvert$），都要先交代它在题里承担的作用。

### Related Rules
Pattern-Key: math.explain_human_bridge
Pattern-Key: linear_algebra.basis_coordinate_explain

### Resolution
2026-07-21：用户明确要求“以后都这样”，已同步到 `.learnings/RULES.md` 的 Do / Watch For 区。

---
