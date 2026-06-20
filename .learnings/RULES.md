# Rules

Compressed patterns from repeated learnings and errors.

---

## Do

- (4x) 表格内 LaTeX 绝对值用 `$\lvert A \rvert$`，范数用 `$\left\lVert A \right\rVert$`
- (2x) `/kaoyan-plan` 完成报告后必须更新：每日计划 → 完成记录 → 英语📊进度 → ⭐英语📅日志 → ⭐线代📊进度 → 专业课📊进度
- (2x) 删除 Obsidian 文件前先调用 safe-delete skill 清理悬空链接
- (1x) 生成 wikilink 前先用 Glob 确认目标文件存在
- (1x) 错题归档按知识模块判断，不按表象判断
- (1x) **证明/推导类内容使用嵌套 callout 结构**：外层 `> [!example]+ 标题`（`+` 默认折叠）作为可折叠入口，内层用 `> [!proof]` / `> [!tip]` / `> [!note]` 嵌套承载具体内容；标题本身是折叠块的一部分，**不要**把 H3 标题与 callout 并列摆放
- (1x) sortspec 中文件夹只用文件夹名称，不展开子文件

## Don't

- (4x) 表格单元格内 LaTeX 不要用 `$|A|$`、`$\Vert A \Vert$`、`$\left| A \right|$` — 管道符会被 Markdown 误解析
- (1x) **单层 callout 内不要用 `$$` 块级公式**，应移到 callout 外面（避免单层 callout 内多行 `$$` 渲染异常）
- (1x) 嵌套 callout 的**内层**允许 `$$` 块级公式（证明/推导场景的标准用法）
- (1x) Callout 内 `$$` 不要紧跟 `[!type]` 后面 — 会被当作 callout 标题而非数学公式
- (1x) 不要凭空猜测 wikilink 路径
- **不要将新规则提升到 CLAUDE.md** — 新规则仅写入 `.learnings/RULES.md`，由 hook 在 agent 启动时注入

## Watch For

- (4x) 表格内 LaTeX 管道符冲突（Pattern-Key: table.pipe_in_math）— 高频复发
- (2x) 完成报告更新清单中"英语📅日志"和"线代📊进度"容易遗漏
- (1x) Obsidian 单层 callout 内多行 `$$` 数学块渲染问题（Pattern-Key: obsidian.callout_math）
- (1x) Obsidian 嵌套 callout 结构用于证明/推导（Pattern-Key: obsidian.proof_collapsible）— 注意外层用 `+` 默认折叠，内层子 callout 用 `-` 或无标记
