# Rules

Compressed patterns from repeated learnings and errors.

---

## Do

- (5x) 表格内 LaTeX 绝对值用 `$\lvert A \rvert$`，范数用 `$\left\lVert A \right\rVert$`
- (2x) `/kaoyan-plan` 完成报告后必须更新：每日计划 → 完成记录 → 英语📊进度 → ⭐英语📅日志 → ⭐线代📊进度 → 专业课📊进度
- (2x) 删除 Obsidian 文件前先调用 safe-delete skill 清理悬空链接
- (2x) **证明/推导类内容统一使用 `> [!note]-` 单一折叠块**（默认折叠，可包含 `$$` 公式、列表、表格），不再使用嵌套 callout 结构。标题直接作为 callout 标题：`> [!note]- 标题内容`
- (4x) 处理用户手写笔记时，默认采用“主笔记提取重构 + 手写原图溯源”：正文提炼为结构化文字，并配清晰的标准图或 AI 重绘图；原图按对应段落保留，内容重复时可折叠为“手写来源”；每张关键图补“图的作用 + 关键标注/区域 + 做题结论”
- (3x) 写入含大量 LaTeX/反引号的 Markdown 时，优先使用 Python raw string、占位符替换或 quoted heredoc（如 `<<'EOF'`），写入后回读目标段落检查反斜杠和控制字符
- (1x) 写入或修改笔记前先快速浏览 `.learnings/RULES.md`，确认当前格式规范与高频错误
- (1x) 生成 wikilink 前先用 Glob 确认目标文件存在
- (1x) 错题归档按知识模块判断，不按表象判断
- (1x) sortspec 中文件夹只用文件夹名称，不展开子文件
- (1x) **写入笔记前验证数学内容正确性** — 公式、定理、推导必须先自行核验（对教材/推导/边界检查）再写入，不能“写完再看”
- (1x) **更新《🧪 高数必背自测（遮挡式）.md》前必须做覆盖率审计** — 对比源文件《高数必背公式.md》的 `## / ###` 章节，生成「缺失章节清单」，所有缺失项必须**补全或显式标注忽略原因**后才算更新完成
- (1x) 基于图片/截图修正题目时，先按图片重新识别题目并完整重算关键步骤，再写入解析
- (1x) 修改错题本题干、参数或选项后，同步检索并更新同目录 `错题题目.md`，完成后回读两处题干确认一致
- (1x) 用户质疑数学解析正确性时，优先用目标等式或代入法直接验算；相似变换题直接验算 `P^(-1)AP=B` 或 `AP=PB`
- (1x) 专业课核心公式首次出现后，紧跟变量符号说明：物理意义、方向/极性约定、单位/典型值、做题近似用法
- (1x) 必背/速查类笔记优先保留“定义 + 公式 + 性质 + 口诀 + 易错点 + 做题步骤 + 来源链接”，长推导和完整例题留在原章节
- (1x) 必背/速查类笔记先读取对应源笔记，按“源笔记原句/公式/步骤 → 精简压缩 → 必要补充”的顺序处理；补充内容必须与源笔记主线一致
- (1x) Markdown 区块替换优先用标题边界（如从 `## A` 到下一个 `## B`），不要用裸 `---` 作为唯一结束锚点
- (1x) 生成或更新学习内容时，先判断图示/图片描述是否更有利于学习；若能降低理解成本，就主动生成并嵌入图，并配“图的作用 + 关键标注 + 学习/做题结论”

- (1x) 学习笔记开头优先设置“符号速查/符号说明”区块：集中解释本节会用到的缩写、变量、端口、电压/电流方向、参数含义和做题用法，方便复习时先查符号。

- (1x) 好题/错题解析笔记先写完整题目卡片：题目原文、已知与所求、原题关键图/裁剪图、答案速览、SOP、分步解析、易错点；原题整图只作折叠溯源，不能替代正文关键图

- (1x) 写入题目解析前先确认目标笔记；用户给出路径时以该路径为唯一写入目标；若误写，必须移动到正确目标并清理原处后回读验证

- (1x) Obsidian Mermaid 节点文本含中文、比较符、括号、逗号或公式样内容时，用双引号包裹；比较符优先用 `≤`、`≥`、`＜`、`＞` 等显示符号。

## Don't

- (5x) 表格单元格内 LaTeX 不要用 `$|A|$`、`$\Vert A \Vert$`、`$\left| A \right|$` — 管道符会被 Markdown 误解析
- (3x) 不要用 Python 普通三引号字符串或未加引号 heredoc 写入含 `\begin`、`\rvert`、反引号等 Markdown/LaTeX 内容
- (1x) 单层 callout 内**允许**使用 `$$` 块级公式（证明/推导场景：`> [!note]-` 折叠块本身就是允许 `$$` 的标准用法）。但 `$$` 不要紧跟 `[!type]` 后面 — 会被当作 callout 标题而非数学公式
- (1x) 不要凭空猜测 wikilink 路径
- (1x) 不要只替换图片题的题干而沿用旧解析；新旧答案偶然一致也可能隐藏验秩矩阵、过程或边界条件错误
- (1x) 不要用含撇号、反斜杠或 Markdown 符号的复杂 inline `printf` 搭配重定向初始化/修复学习文件，避免引号破裂导致文件被截空
- **不要将新规则提升到项目入口文件（AGENTS.md / CLAUDE.md）** — 新规则仅写入 `.learnings/RULES.md`，由 hook 在 agent 启动时注入

- (1x) Mermaid 节点标签中不要裸写 `<`、`<=`、`>`、`>=` 或未加引号的 `VGS(off)` 这类括号表达式，避免 Obsidian/Mermaid 解析异常。

## Watch For

- (5x) 表格内 LaTeX 管道符冲突（Pattern-Key: table.pipe_in_math）— 高频复发
- (4x) Markdown/LaTeX 写入转义污染（Pattern-Key: write_verify.latex_escape）— `\begin`、`\rvert`、反引号、heredoc、Python 字符串和索引表格行都要重点回读
- (2x) 完成报告更新清单中“英语📅日志”和“线代📊进度”容易遗漏
- (2x) Obsidian 证明/推导使用 `> [!note]-` 单一折叠块（Pattern-Key: obsidian.proof_collapsible）— 默认折叠；callout 内允许 `$$` 块级公式；表格前后留空行
- (5x) 图示覆盖率不足（Pattern-Key: docs.visual_source_coverage）— 多页手写笔记/教材图/曲线特性图进入笔记前先做“原图页/关键图 → 笔记章节”覆盖清单；特性曲线、负载线、Q 点漂移类知识应主动配图
- (1x) 手写笔记混合重构（Pattern-Key: docs.handwritten_hybrid）— 正文以结构化提炼和标准图/AI 重绘图服务复习，原图留在对应段落或折叠“手写来源”保留推理、纠错和个人理解
- (1x) 数学笔记内容准确性验证（Pattern-Key: math.content_verify）— 公式/定理/推导写入前必须独立验证
- (1x) 自测文件覆盖率遗漏（Pattern-Key: quiz.coverage_audit）— 更新自测前必须对比源文件章节列表
- (1x) 图片纠正题目后的完整重算（Pattern-Key: image_problem.recompute）— 按图片重新识别题目、重算关键步骤并回读渲染结果
- (1x) 错题本与练习入口题干同步（Pattern-Key: mistake.index_sync）— 修改错题本后检查 `错题题目.md`
- (1x) 数学解析质疑后的直接验算（Pattern-Key: math.direct_substitution_check）— 优先验算目标等式，不只口头确认
- (1x) 专业课公式符号说明遗漏（Pattern-Key: electronics.formula_symbol_explain）— 首次出现核心公式时检查变量、方向、单位、近似用法是否齐全
- (1x) 速查笔记过度搬运详解（Pattern-Key: notes.quick_review_extract）— 必背/速查文件避免塞入历史背景、完整推导和完整例题
- (1x) 源笔记优先抽取（Pattern-Key: notes.source_first_extract）— 更新必背/速查笔记前先读对应章节源笔记，避免凭空换符号、替换原主方法或另写一套表达
- (1x) shell 引号与重定向风险（Pattern-Key: ops.shell_quote_redirect）— 初始化/修复 `.learnings/` 等规则文件时避免复杂 inline printf，写后立刻回读行数和关键内容
- (1x) Markdown 区块替换边界误伤（Pattern-Key: markdown.section_replace_boundary）— 表格分隔线和水平线都含 `---`，批量替换时优先用标题边界并回读目标段
- (1x) 主动图示化学习内容（Pattern-Key: docs.proactive_visual_learning）— 几何位置、物理过程、函数曲线、流程结构、电路、变量方向易混内容，优先考虑补图而非只写文字公式
- (1x) 笔记开头符号说明遗漏（Pattern-Key: notes.symbol_quick_reference）— 专业课/数学等符号密集笔记写入前，先检查开头是否有符号速查；不要把符号解释分散到正文首次出现处。
- (1x) 好题解析题目卡片缺失（Pattern-Key: problem_note.complete_card）— 图片题必须检查题干、已知所求、电路图/曲线图等关键图是否在正文可见；原题整图只作折叠溯源
- (1x) 题目解析目标路径误判（Pattern-Key: note_update.target_path_confirm）— 题目/例题/好题/错题优先写入好题解析或错题文件；用户显式路径最高优先级
- (1x) Mermaid 节点标签转义（Pattern-Key: obsidian.mermaid_node_label_escape）— 中文节点、条件判断、括号和比较符要先加引号并替换裸 `<`/`<=`。
