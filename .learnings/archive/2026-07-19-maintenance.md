# Learnings maintenance archive

---

## Maintenance archive — 2026-07-19 15:14-15:20

**Logged**: 2026-07-19T15:15:50+0800
**Scope**: `.learnings/` active record cleanup after source fixes.

### Fixes applied
- Updated `.agents/skills/kaoyan-math-notes/SKILL.md` with source-first extraction, structure-template requirement, original-method preservation, and Markdown/LaTeX write verification checklist.
- Updated `.claude/skills/kaoyan-math-notes/SKILL.md` with equivalent rules.
- Synchronized missing skill files: copied `templates/knowledge-point-template.md` to agents side and `code.md.backup` to Claude side.
- Verified both `kaoyan-math-notes` SKILL.md metadata and control-character scans.
- `sync_platform_skills.py --skill kaoyan-math-notes` now has no missing-file ERROR; remaining SKILL.md difference is a WARN due to Codex long-form vs Claude compact-form wording.

### Archived learning records

#### ## [LRN-20260718-001] best_practice

```markdown
## [LRN-20260718-001] best_practice

**Logged**: 2026-07-18T19:20:31+0800
**Priority**: medium
**Status**: resolved
**Area**: docs

### Summary
以后处理用户提供的手写笔记，默认采用“主笔记提取重构 + 保留手写原图溯源”的混合结构。

### Details
整理增强型 NMOS 的四页手写推导时，正文使用统一的三状态标准图承载“无沟道、感生沟道、漏端夹断前兆”的主线；四张手写原图按内容分配到对应章节的折叠来源区，并逐张补了图的作用与转写结论。用户随后明确确认，这应成为以后接收手写笔记时的默认组织方式：正文服务检索、复习和做题，原图保留推理、纠错痕迹和个人理解。

### Suggested Action
先建立“原图页/关键图 → 正文章节”的覆盖清单；正文提取为结构化文字，按需配标准图或 AI 重绘图；原图保留在对应段落，重复内容可折叠为“手写来源”，并保留每张关键图的读图结论。

### Related Rules
Pattern-Key: docs.handwritten_hybrid

### Resolution
2026-07-18T19:31:50+0800：用户明确确认将该混合方式设为后续手写笔记的默认规则，已同步到 `.learnings/RULES.md` 的 Do 与 Watch For。

---
```

#### ## [LRN-20260718-002] best_practice

```markdown
## [LRN-20260718-002] best_practice

**Logged**: 2026-07-18T19:30:35+0800
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
生成或更新学习内容时，应主动判断加入图示或图片描述是否更利于理解。

### Details
用户指出抽水做功这类内容只写公式不够直观。以后生成数学、专业课等学习笔记时，不能只按文字/公式输出；应先从学习效果角度判断是否需要图示：如果图能帮助定位变量、空间关系、变化趋势、易错方向或步骤流程，就应生成图并嵌入笔记，同时补充图的作用、关键标注和做题结论。

### Suggested Action
每次生成或更新学习内容前增加“图示价值判断”：若内容涉及几何位置、物理过程、函数/曲线、流程、结构关系、电路或容易混淆的变量方向，就主动生成 SVG/Excalidraw/数学图像等合适图片并嵌入 Obsidian 笔记；图片旁必须配“图的作用 + 关键标注 + 学习/做题结论”。

### Related Rules
Pattern-Key: docs.proactive_visual_learning

### Resolution
2026-07-18：用户明确要求将该做法作为以后生成内容的习惯，已同步到 `.learnings/RULES.md` 的 Do 与 Watch For。

---

---
```

#### ## [LRN-20260719-001] best_practice

```markdown
## [LRN-20260719-001] best_practice

**Logged**: 2026-07-19T14:51:56+0800
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
结构识别型必背/速查笔记不能压缩到只剩公式，必须保留最小结构模板或图示。

### Details
整理线性代数“递推型行列式”到《必背知识》时，初版只保留了递推公式、结论和易错点。用户指出这会导致复习时“不懂”：递推型行列式属于结构识别型知识，考场启动依赖先认出异爪型、三对角型、四角剥皮型等模板，而不是只背 $D_n=pD_{n-1}+qD_{n-2}$。随后已补充异爪型模板、三对角模板和四角剥皮图示，并为图示配“图的作用 + 关键标注 + 做题结论”。

### Suggested Action
以后更新必背/速查类笔记时，先判断知识点是“纯公式型”还是“结构识别型”。纯公式型可只保留公式、条件和易错点；结构识别型必须保留最小识别模板、启动口诀和必要图示，避免过度压缩导致复习时无法认题。

### Related Rules
Pattern-Key: notes.structure_template_required
```

#### ## [LRN-20260719-002] correction

```markdown
## [LRN-20260719-002] correction

**Logged**: 2026-07-19T15:08:30+0800
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
用户提供原图或资料做法时，笔记应优先还原原图主方法，不能擅自换成另一种可行但非原资料的解法。

### Details
整理线性代数“递推型行列式”例题 13“四角剥皮型 $2n$ 阶行列式”时，原图体现的是分块矩阵法：通过同序重排行和列，把矩阵化为 $n$ 个 $2\times2$ 块对角矩阵，得到 $(ad-bc)^n$。初版笔记却先写成“按第一行展开 + 剥皮递推”的做法。虽然结论正确，但与用户资料中的主思路不一致，导致用户追问“图中的做法不是用分块矩阵的做法吗”。随后已将分块矩阵法改为主方法，剥皮递推法降级为备用理解。

### Suggested Action
以后根据用户提供的图片、截图、教材页或原笔记整理内容时，先识别并保留“原资料主方法/主线索”。如果另有更通用或更简单的方法，只能作为“备用方法/补充理解”呈现；不得用替代方法覆盖原图思路。写入后回读标题和方法选择提示，确认主次关系与资料来源一致。

### Related Rules
Pattern-Key: docs.source_method_alignment

---

---
```

#### ## [LRN-20260719-003] correction

```markdown
## [LRN-20260719-003] correction

**Logged**: 2026-07-19T15:10:19+0800
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
更新必背/速查笔记时，应优先抽取和压缩用户已有源笔记内容，不要先凭空改写一套表达。

### Details
整理《线性代数必背知识》的“递推型行列式”时，三对角型递推的特征方程部分初版用了新符号和自行组织的说法。用户提醒“尽可能用我现有的笔记中的内容”。随后回到源笔记《1.4.5-递推型行列式.md》，抽取其中“二阶递推的特征方程模板”和“解法二：特征方程法（考场推荐）”的原有表达，改回源笔记使用的符号、通用模板、二重根通解和代初值过程。

### Suggested Action
以后更新必背/速查类笔记时，先读取对应章节源笔记，按“源笔记原句/公式/步骤 → 精简压缩 → 必要补充”的顺序处理。只有源笔记缺少识别模板、做题启动步骤或必要图示时，才进行补充；补充内容应与源笔记主线保持一致，避免替换用户原有笔记体系。

### Related Rules
Pattern-Key: notes.source_first_extract

### Resolution
2026-07-19T15:13:21+0800：用户确认同步。已将 `notes.source_first_extract` 写入 `.learnings/RULES.md` 的 Do 与 Watch For：必背/速查类笔记必须先读取对应源笔记，按“源笔记原句/公式/步骤 → 精简压缩 → 必要补充”的顺序处理。
```

### Archived error records

#### ## [ERR-20260719-001] write_verify

```markdown
## [ERR-20260719-001] write_verify

**Logged**: 2026-07-19T15:10:19+0800
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
写入含 LaTeX 反斜杠的 Markdown 时发生转义污染，并出现一次 shell 引号失败。

### Error
```text
zsh: unmatched '
LaTeX 转义污染：\theta 被写成制表符 + heta；\boxed 被写成退格控制字符 + oxed；cases 换行反斜杠数量也被写错。
```

### Context
在把源笔记中的三对角型递推特征方程法压缩写入《线性代数必背知识.md》时，先用 shell 命令提取含中文括号和引号的标题导致引号失败；随后写入含 \theta、\boxed、\begin{cases} 的 Markdown 时出现转义污染。最终通过回读目标段落、扫描控制字符、逐行修复反斜杠数量解决。

### Suggested Action
写入含 LaTeX 命令的 Markdown 时，优先从源文件读取原文片段再做最小替换；写入脚本中使用 raw string、占位符或 `chr(92)` 生成反斜杠。每次写入后必须回读目标段落，并扫描控制字符，重点检查 \theta、\boxed、\begin、\rvert、cases 换行符。

### Related Rules
Pattern-Key: write_verify.latex_escape
```



---

## 2026-07-19 20:02 maintain-learnings：笔记开头符号速查

### 原活跃记录

## [LRN-20260719-004] best_practice

**Logged**: 2026-07-19T19:58:08+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/notes

### Summary
学习笔记中的符号应在笔记开头统一说明，方便查找和复习。

### Details
用户在更新 FET 核心思想笔记后明确反馈：“笔记中的符号要在笔记开头说明，方便我查找和复习”。这说明符号密集型笔记不能只在正文首次出现处零散解释；应在标题和导航后放一个“符号速查/符号说明”区块，把端口、变量、参数、缩写、方向/极性约定和做题用法集中起来。

### Suggested Action
后续整理专业课、数学等符号密集笔记时，默认在笔记开头加入“符号速查”折叠块或小节；先列出本节会出现的关键符号，再进入正文。尤其是电路/模电笔记，要把 G/D/S/B、$v_{GS}$、$i_D$、$g_m$、阈值电压、方向约定等放在开头，便于复习前快速查表。

### Resolution
已同步到 `.learnings/RULES.md` 的 Do 与 Watch For：新增 Pattern-Key `notes.symbol_quick_reference`。

### Related Rules
Pattern-Key: notes.symbol_quick_reference

---


### 修复源头

- `.agents/skills/kaoyan-electronics/SKILL.md` / `.claude/skills/kaoyan-electronics/SKILL.md`：新增专业课笔记落盘约束，符号密集时标题和导航后必须放 `> [!abstract]- 符号速查`。
- `.agents/skills/kaoyan-electronics-structure/SKILL.md` / `.claude/skills/kaoyan-electronics-structure/SKILL.md`：章节卡片输出格式新增“符号速查”。
- `.agents/skills/kaoyan-electronics/scripts/templates/knowledge_card_electronics.md` / `.claude/skills/kaoyan-electronics/scripts/templates/knowledge_card_electronics.md`：模电、数电标准模板新增符号速查 callout。
- `.agents/skills/kaoyan-electronics-structure/references/card-templates.md` / `.claude/skills/kaoyan-electronics-structure/references/card-templates.md`：结构模块的卡片生成模板新增符号速查 callout。

### 验证方式

- skill 元数据检查通过：`kaoyan-electronics`、`kaoyan-electronics-structure` 在 `.agents/skills` 与 `.claude/skills` 均有合法 frontmatter。
- 模板检查通过：4 个卡片模板文件均包含 `> [!abstract]- 符号速查`。
- 多 Agent 同步检查通过：`sync_platform_skills.py --skill kaoyan-electronics` 与 `--skill kaoyan-electronics-structure` 均返回 OK。

### 处理结果

已修复并归档，活跃 `.learnings/LEARNINGS.md` 中移除此详细记录；简短铁律保留在 `.learnings/RULES.md`。
