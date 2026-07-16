# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260713-004] best_practice

**Logged**: 2026-07-13T18:59:30+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
专业课笔记中的图片必须补充读图说明，不能只放图

### Details
用户指出“这里只给图不行啊，我又不知道你这个图是干嘛的”。当前模电笔记 `05-二极管结构参数与伏安特性.md` 原来连续嵌入了二极管结构图和伏安特性曲线图，但图片下方缺少“这张图说明什么、应该抓什么、做题怎么用”的解释。后续已为 4 张图分别补充 callout：点接触型结构、面接触/符号、伏安曲线三大工作区、①②③ 区域含义。

### Suggested Action
整理教材截图、结构图、曲线图进入 Obsidian 笔记时，每张关键图后至少补一句“图的作用 + 关键标注/坐标/区域 + 考研做题结论”。尤其是伏安曲线、电路图、结构图，不能只嵌入图片，要让未来复习时不看原教材也知道图在服务哪个知识点。

---


## [LRN-20260713-005] best_practice

**Logged**: 2026-07-13T19:01:43+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
专业课公式必须补充符号说明，不能只放公式

### Details
用户选中 PN 结伏安公式 `i_D=I_S\left(e^{v_D/(nV_T)}-1\right)` 后追问“你这里公式符号指的是啥？”。这说明笔记中只给公式和少量结论仍然不够，尤其是模电/电路类公式，复习时需要知道每个符号的物理含义、正方向约定、单位/典型值，以及这条公式在做题中主要用于理解还是用于手算。

本次已在 `考研专业课/模拟电子技术/详细笔记/01-二极管及其基本电路/04-PN结形成与单向导电.md` 中为该公式补充符号表，解释 `i_D`、`I_S`、`e`、`v_D`、`n`、`V_T`，并说明常温下 `V_T\approx26\mathrm{mV}`、正偏指数增长、反偏未击穿时约为 `-I_S`。

### Suggested Action
以后整理专业课笔记时，凡是首次出现核心公式，必须紧跟“符号含义”小表或列表：至少说明变量名称、物理意义、方向/极性约定、常用数值/单位、做题时的近似用法。不要只放公式再直接给结论。

---


## [LRN-20260714-006] correction

**Logged**: 2026-07-14T20:47:44+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
用户提供多页手写图示时，必须先审计图示覆盖率，不能用少量概括图替代原有推导链。

### Details
本次整理“二极管微变等效电路”时，用户提供了 5 页手写笔记，其中分别包含指数关系与符号、$700\mathrm{mV}$ 偏置、Q 点切线、直流/交流拆分、完整例题等图示。初稿仅用 2 张概括性重绘图替代，虽然覆盖了核心结论，却丢失了用户通过逐步作图建立的推导节奏；用户明确指出“我的笔记中画了这么多图，到你这就没几个了？”。后续已将 5 张手写原图按原顺序嵌入正文，并保留 2 张规范重绘图作为辅助。

### Suggested Action
处理多页手写笔记前，先建立“原图页/关键图 → 笔记章节”的覆盖清单。默认逐页保留用户的原始图示，并为每张图附上读图说明；规范重绘图只用于补充清晰度、方向和等效关系，不能压缩或取代原有图示链。

### Related Rules
Pattern-Key: docs.visual_source_coverage

---

## [LRN-20260715-007] best_practice

**Logged**: 2026-07-15T17:04:04+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
写入含 LaTeX 的索引表格行时，也必须使用 quoted heredoc 或纯文本拼接并回读控制字符

### Details
本次连续整理高数积分学错题 11.1、11.2、11.3 到 `考研数学/高数-一元函数积分学/错题本.md` 和 `错题题目.md`。在写入错题93索引行时，Python 字符串中的 `\frac`、`\textrm`、`\big` 被解释为控制字符（form feed、tab、backspace），造成索引行残留不可见字符。虽然正文通过 quoted heredoc 最终正确写入，但索引行也同样属于 Markdown/LaTeX 高风险写入区域，不能用普通 Python 字符串草率拼接。

### Suggested Action
以后凡是写入包含 LaTeX 命令的 Markdown，不只正文，索引表格行也要采用 quoted heredoc、Python raw string，或避免在索引表格中放复杂 LaTeX 命令。写入后必须扫描控制字符、奇数 `$`、表格管道符冲突，并回读目标段落确认 `\frac`、`\text`、`\big` 等没有被转义污染。

### Related Rules
Pattern-Key: write_verify.latex_escape

---

## [LRN-20260716-008] best_practice

**Logged**: 2026-07-16T09:53:40+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
章节笔记提炼为必背笔记时，应只保留快速复习可直接调用的结论

### Details
本次用户给出线性代数第一章行列式的三篇章节笔记，目标是更新 `线性代数/必背知识.md`，用于后续快速复习。最终筛选时没有照搬历史背景、方程组推导、沙路法则完整图示和完整例题，而是保留了二阶/三阶行列式公式、余子式与代数余子式、五大性质、零行列式结论、展开定理、展开定理推论和行列式计算策略，并添加来源链接方便回查原章节。

### Suggested Action
以后从章节详笔记提炼“必背/速查/快速复习”类笔记时，优先写“定义 + 公式 + 性质 + 口诀 + 易错点 + 做题步骤 + 来源链接”；长推导、历史背景、完整例题和课堂解释保留在原章节笔记中，不要挤占速查笔记空间。

---

## [LRN-20260716-009] best_practice

**Logged**: 2026-07-16T09:53:40+08:00
**Priority**: high
**Status**: pending
**Area**: ops

### Summary
初始化或修复学习文件时，避免用含撇号的复杂 inline printf 命令

### Details
本次执行 digest 阶段时，尝试用一行 shell 命令在 `.learnings/RULES.md` 不存在时创建默认内容，其中字符串包含 `Don't` 的撇号，导致 zsh 引号提前闭合并触发错误。由于命令中同时存在重定向，最终造成 `.learnings/RULES.md` 被截空。随后已根据本轮启动时注入的规则内容，用 quoted heredoc 恢复 RULES，并回读确认无控制字符。

### Suggested Action
以后初始化或修复 `.learnings/`、规则文件、Markdown 配置文件时，不要把含撇号、反斜杠或 Markdown 符号的多行内容塞进 inline `printf`。优先使用 quoted heredoc、Python `Path.write_text()` 的 raw string，或先判断文件是否存在再单独写入；涉及重定向的命令写完后必须立刻回读行数和关键内容。

### Related Rules
Pattern-Key: ops.shell_quote_redirect

---
