# Rules

Compressed patterns from repeated learnings and errors.

---

## Do

- (5x) 表格内 LaTeX 绝对值用 `$\lvert A \rvert$`，范数用 `$\left\lVert A \right\rVert$`
- (2x) `/kaoyan-plan` 完成报告后必须更新：每日计划 → 完成记录 → 英语📊进度 → ⭐英语📅日志 → ⭐线代📊进度 → 专业课📊进度
- (2x) 删除 Obsidian 文件前先调用 safe-delete skill 清理悬空链接
- (1x) 生成 wikilink 前先用 Glob 确认目标文件存在
- (1x) 错题归档按知识模块判断，不按表象判断
- (1x) **证明/推导类内容统一使用 `> [!note]-` 单一折叠块**（默认折叠，可包含 `$$` 公式、列表、表格），不再使用嵌套 callout 结构。标题直接作为 callout 标题：`> [!note]- 标题内容`
- (1x) sortspec 中文件夹只用文件夹名称，不展开子文件
- (1x) **写入笔记前验证数学内容正确性** — 公式、定理、推导必须先自行核验（对教材/推导/边界检查）再写入，不能"写完再看"
- (1x) **更新《🧪 高数必背自测（遮挡式）.md》前必须做覆盖率审计** — 对比源文件《高数必背公式.md》的 `## / ###` 章节，生成「缺失章节清单」，所有缺失项必须**补全或显式标注忽略原因**后才算更新完成

## Don't

- (5x) 表格单元格内 LaTeX 不要用 `$|A|$`、`$\Vert A \Vert$`、`$\left| A \right|$` — 管道符会被 Markdown 误解析
- (1x) 单层 callout 内**允许**使用 `$$` 块级公式（证明/推导场景：`> [!note]-` 折叠块本身就是允许 `$$` 的标准用法）。但 `$$` 不要紧跟 `[!type]` 后面 — 会被当作 callout 标题而非数学公式
- (1x) 不要凭空猜测 wikilink 路径
- **不要将新规则提升到 CLAUDE.md** — 新规则仅写入 `.learnings/RULES.md`，由 hook 在 agent 启动时注入

## Watch For

- (5x) 表格内 LaTeX 管道符冲突（Pattern-Key: table.pipe_in_math）— 高频复发
- (2x) 完成报告更新清单中"英语📅日志"和"线代📊进度"容易遗漏
- (2x) Obsidian 证明/推导使用 `> [!note]-` 单一折叠块（Pattern-Key: obsidian.proof_collapsible）— 默认折叠；callout 内允许 `$$` 块级公式；表格前后留空行
- (1x) 数学笔记内容准确性验证（Pattern-Key: math.content_verify）— 公式/定理/推导写入前必须独立验证
- (1x) 自测文件覆盖率遗漏（Pattern-Key: quiz.coverage_audit）— 更新自测前必须对比源文件章节列表
