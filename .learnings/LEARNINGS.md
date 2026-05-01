# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260425-001] correction

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
- Related Files: 考研数学/微分方程/4-微分方程的综合应用/几何应用.md
- Tags: obsidian, markdown, table, latex, pipe-conflict
- Pattern-Key: table.pipe_in_math

---
