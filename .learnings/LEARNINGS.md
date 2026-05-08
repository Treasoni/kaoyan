# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260506-002] knowledge_gap

**Logged**: 2026-05-06T07:00:00Z
**Priority**: medium
**Status**: promoted
**Area**: docs, config

### Summary
Obsidian (KaTeX) 不支持 `\iddots`，抗对角行列式须用 `\ddots` 替代

### Details
在 Obsidian 中（使用 KaTeX 渲染引擎），`\iddots`（逆对角线省略号，⋰）不被支持，渲染不出任何内容。
编写副对角行列式/副对角三角行列式时，须用 `\ddots`（⋱）替代。
虽然 `\ddots` 的视觉方向（从上到下、从左到右）与 `\iddots`（从下到上、从左到右）不同，但它是 KaTeX 下唯一可用的对角省略号命令，且在线性代数的矩阵表示中被广泛接受。

受影响场景：
- 副对角行列式：`\begin{vmatrix} & & & a_{1n} \\ & & a_{2,n-1} & \\ & \ddots & & \\ a_{n1} & & & \end{vmatrix}`
- 副对角三角行列式：同上

### Suggested Action
编写含 LaTeX 矩阵的文档时，避免使用 `\iddots`，一律用 `\ddots`。

### Metadata
- Source: user_feedback
- Related Files:
  - 考研英语/📅 学习日志.md
  - 考研英语/📊 学习进度.md
  - .claude/skills/kaoyan-plan/SKILL.md
- Tags: kaoyan-plan, progress-update, checklist

---

## [LRN-20260507-001] best_practice

**Logged**: 2026-05-07T11:40:00Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Obsidian Mermaid 图表中禁止使用 LaTeX 语法（$...$），须用纯文本替代

### Details
在 Obsidian 中使用 Mermaid 语法绘制状态图、时序图等图表时，`note` 注释块内禁止使用 LaTeX 数学语法（如 `$Q_2$`、`$\overline{R_{D1}}$`），否则渲染异常或显示不出来。

**错误示例：**
```mermaid
note right of 01
  此时 $Q_2=1$ 导致 $\overline{R_{D1}}=0$
  $FF_1$ 被异步清零锁定
end note
```

**正确示例：**
```mermaid
note right of 01
  此时 Q2=1 导致 RD1清零生效
  FF1 被异步清零锁定，电路自锁
end note
```

### Suggested Action
在 Mermaid 图表的 `note`、`title` 等文本节点中：
1. 避免使用 `$...$` 包裹公式
2. 直接使用下标符号（如 Q2 而非 $Q_2$）
3. 用汉字或英文描述替代特殊符号（如"清零"代替 $\overline{R_{D}}$）

### Metadata
- Source: user_feedback
- Related Files:
  - 考研专业课/数字电子技术/6-时序逻辑电路/错题本.md
- Tags: obsidian, mermaid, latex, markdown

---

## [LRN-20260507-002] correction

**Logged**: 2026-05-07T13:00:00Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
执行 /kaoyan-plan 完成报告时，线性代数进度文件（`线性代数/第一章：行列式/📊 学习进度.md`）也需要同步更新

### Details
当用户报告数学学习完成且涉及线性代数时（如"行列式全部内容+矩阵定义+特殊矩阵"），除了更新高数进度文件，还必须更新线性代数相应章节的进度文件。

**问题原因**：线性代数有自己的目录结构，与考研数学/高数-xxx 是独立路径，容易被忽略。

### Suggested Action
执行完 /kaoyan-plan 完成报告后，检查数学任务涉及的科目：
1. ✅ 高数进度文件：`考研数学/高数-xxx/📊 学习进度.md`
2. ⭐ **线性代数进度文件**：`线性代数/第X章：XXX/📊 学习进度.md` ← 容易遗漏

### Metadata
- Source: user_feedback
- Related Files:
  - 线性代数/第一章：行列式/📊 学习进度.md
  - 线性代数/第二章：矩阵/📊 学习进度.md
- Tags: kaoyan-plan, progress-update, checklist, linear-algebra
- Recurrence-Count: 1
- First-Seen: 2026-05-07
- See Also: LRN-20260506-003

### Resolution
- **Resolved**: 2026-05-07
- **Action Taken**: 已修改 SKILL.md，在"完成报告处理清单"和"数学完成报告更新步骤"中添加了⭐标记和明确提示，要求搜索 `线性代数/**/📊 学习进度.md` 路径

---

## [LRN-20260506-003] correction

**Logged**: 2026-05-06T14:30:00Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
执行 /kaoyan-plan 完成报告时，必须同步更新考研英语/📅 学习日志.md

### Details
当用户报告英语学习完成时（如 Day 051 第3次复习 + Day 066 新学），除了更新 📊 学习进度.md，还必须同步更新 📅 学习日志.md。

**问题原因**：更新清单中第 4 项容易被遗漏。

**历史记录**：
- 2026-05-06：首次记录此问题（LRN-20260506-003）
- 2026-05-07：**再次遗漏**，用户再次指出同一问题

### Suggested Action
执行完 /kaoyan-plan 完成报告后，逐一检查更新清单：
1. ✅ 每日计划 - 今日完成情况
2. ✅ 完成记录文件
3. ✅ 英语 📊 学习进度.md
4. ⭐ **英语 📅 学习日志.md** ← 容易遗漏
5. ⭐ **线性代数进度文件** ← 如有数学任务
6. ✅ 专业课 📊 学习进度.md
7. ✅ 专业课章节进度文件

**根本解决方案**：在 SKILL.md 的完成报告处理清单中，将"英语 📅 学习日志.md"和"线性代数进度文件"明确标注为**必须更新**，并放在清单前部以提高优先级。

### Metadata
- Source: user_feedback
- Related Files:
  - 考研英语/📅 学习日志.md
  - 考研英语/📊 学习进度.md
  - .claude/skills/kaoyan-plan/SKILL.md
- Tags: kaoyan-plan, progress-update, checklist
- Recurrence-Count: 2
- First-Seen: 2026-05-06
- Last-Seen: 2026-05-07
- See Also: LRN-20260506-001 (关于线代进度文件也需要更新)

---

## [LRN-20260506-002] knowledge_gap

**Logged**: 2026-04-25T00:00:00Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
错题被错误归档到一元函数积分学模块，实际应归入多元函数微分学模块

### Details
用户纠正：关于 $f(x,y)=\int_0^{xy} e^{-xt^2}\,dt$ 的错题属于多元函数微分学，不应追加到 `考研数学/高数-一元函数积分学/错题本.md` 和 `错题题目.md`。这是模块归档错误/路径判断错误。后续处理应先清理错误写入，再写入 `考研数学/高数-多元函数微分学/错题本.md` 和 `错题题目.md`。

### Suggested Action
处理错题归档时，优先按题目所属知识模块判断目标目录，而不是仅按积分表象判断。

### Metadata
- Source: user_feedback
- Related Files: 考研数学/高数-一元函数积分学/错题本.md, 考研数学/高数-一元函数积分学/错题题目.md, 考研数学/高数-多元函数微分学/错题本.md, 考研数学/高数-多元函数微分学/错题题目.md
- Tags: correction, routing, module-classification

---

## [LRN-20260508-001] correction

**Logged**: 2026-05-08T10:20:00Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Markdown 表格内 LaTeX 绝对值符号管道符冲突第三次复发——写入 `$|A|$` 到表格导致列错位

### Details
尽管 CLAUDE.md 已明确记录 "表格内 LaTeX 防管道符冲突" 规则（第 2 条），本次在 `线性代数/第二章：矩阵/错题本.md` 的第 137-141 行表格中，仍错误地写入了 `$|A|$` 和 `$|B|$`，导致：
1. 表格被管道符 `|` 误解析为 10+ 列
2. 第 2 行（命题 ④）完全错位，内容被割裂
3. 需要额外的 fix-table-pipe 修复流程

**复发根因**：CLAUDE.md 的规则是"被动查阅"式说明，在快速生成内容时容易被忽略，尤其当注意力集中在整理知识点逻辑而非格式规范时。

### Suggested Action
1. ✅ 已在 CLAUDE.md 记录规则（已有）
2. ⭐ **额外防护**：每次在表格单元格内写 LaTeX 行内公式时，必须立即检查是否包含竖线符号 `|` —— 这是一种自动化的肌肉记忆，不应依赖事后检查
3. ⭐ **心理检查表**：生成表格前默念一次："表格内禁止裸管道符"

### Metadata
- Source: user_feedback
- Area: docs
- Related Files: 线性代数/第二章：矩阵/错题本.md
- Tags: obsidian, markdown, table, latex, pipe-conflict, recurrence
- See Also: LRN-20260501-001 (原始条目, Pattern-Key: table.pipe_in_math)
- Recurrence-Count: 1
- First-Seen: 2026-05-08

---

## [LRN-20260501-001] best_practice

**Logged**: 2026-05-01T00:00:00Z
**Priority**: high
**Status**: promoted
**Area**: docs

### Summary
Markdown 表格内 LaTeX 公式中的 `|` 管道符会被误解析为表格分隔符，必须用 `\vert` / `\Vert` 替代

### Details
在 Obsidian Markdown 表格中写 LaTeX 公式时：
1. `$|x|$` 中的 `|` 会被 markdown 解析器识别为表格列分隔符，导致表格结构损坏、列数异常
2. `$\left\| ... \right\|$` 中的 `\|` 虽然 LaTeX 语义不同（双竖线/范数），但源代码中仍包含字面量 `|`，同样会被破坏表格
3. 正确的做法是：
   - 单个绝对值：用 `\vert` 替代 `|`，即 `$\vert x \vert$`
   - 双竖线（范数）：用 `\Vert` 替代 `\|`，即 `$\left\Vert \dfrac{y}{y'} \right\Vert$`
   - 已使用 `\left| ... \right|` 的代码不受影响，因为 `\left|` 是一个整体 token

### Suggested Action
生成包含表格的 .md 文件时，检查所有 LaTeX 公式单元格：
1. 搜索 `$|` 或 `\|` 模式
2. 替换为 `$\vert` / `\Vert`
3. 显示公式块（`$$...$$`）不受此限制，只在行内公式且位于表格内时需要注意

### Metadata
- Source: user_feedback
- Related Files:
  - 考研数学/微分方程/4-微分方程的综合应用/几何应用.md
  - 线性代数/第二章：矩阵/错题本.md (2026-05-08 复发)
- Tags: obsidian, markdown, table, latex, pipe-conflict
- Pattern-Key: table.pipe_in_math
- Recurrence-Count: 3
- First-Seen: 2026-05-01
- Last-Seen: 2026-05-08

---
