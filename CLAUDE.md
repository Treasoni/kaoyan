# 考研学习项目 - Agent 核心配置

## 1. 项目核心信息
- **项目名称**：考研学习项目
- **目标院校/专业**：湖南大学 / 控制工程与科学专硕
- **考试科目**：数学二、英语二、思想政治理论、822电子技术基础
- **考试日期**：2026年12月24日-25日

### 核心数据速查
| 数据类型 | 路径 | 权限 |
| --- | --- | --- |
| 高数教材 | `/Users/zhqznc/Documents/高数资料` | 只读 |
| 线代教材 | `/Users/zhqznc/Documents/线性代数资料` | 只读 |
| 当日计划 | `考研计划/每日计划/2026-MM-DD-每日计划.md` | 读/写 |
| 数学进度 | `考研数学/高数-极限与连续/📊 学习进度.md` | 读/写 |
| 英语进度 | `考研英语/📊 学习进度.md` | 读/写 |
| 专业课进度 | `考研专业课/📊 学习进度.md` | 读/写 |

<!-- prompt-cache-bootstrap:begin -->
## Prompt Cache

- Follow `.claude/rules/common/prompt-cache.md` for high-frequency prompt design.
- Keep stable instructions and output formats before dynamic user input, file excerpts, dates, IDs, and runtime state.
- Reuse canonical templates and load long context only when needed.
<!-- prompt-cache-bootstrap:end -->


---

## 2. 技能体系：少入口，多模块

### 2.1 分层原则
本项目不把所有技能平铺给日常任务使用，而采用“入口路由 + 领域模块 + 工具能力”的三层体系：

| 层级 | 定位 | 技能 |
| --- | --- | --- |
| L1 调度入口 | 日常学习只优先进入这些技能 | `/sync`、`/kaoyan-plan`、`/kaoyan-math`、`/kaoyan-english`、`/kaoyan-electronics`、`/understanding`、`/mistake-book` |
| L2 领域模块 | 由入口技能按需调用，用户也可显式直呼 | `*-core`、`*-notes`、`*-structure`、`*-vocab`、`*-review`、`*-quiz`、`*-writing`、`*-sop`、`*-circuit` |
| L3 工具技能 | 仅在文件格式、搜索、图示、Obsidian 管理等明确任务中启用 | `pdf`、`docx`、`obsidian-*`、`json-canvas`、`excalidraw-diagram`、`smart-search`、`parse-words`、`chapter-summary` 等 |

### 2.2 路由优先级
1. 用户显式点名技能时，优先执行该技能。
2. 用户提出“今天怎么学 / 安排计划 / 完成了什么”，进入 `/kaoyan-plan`。
3. 用户提出某科目的学习、笔记、题目、复习，先进入对应科目路由器：`/kaoyan-math`、`/kaoyan-english`、`/kaoyan-electronics`。
4. 用户要求验证推导、理解、截图讲解中的逻辑链，进入 `/understanding`。
5. 用户要求记录错题、提炼错题、重构错题本，进入 `mistake-*` 系列。
6. 用户要求解析高亮英语单词，进入 `/parse-words`；要求章节总结，进入 `/chapter-summary`。
7. 用户要求网页/最新信息/院校信息，进入 `smart-search` 或 `/kaoyan-info`，并优先用可靠来源。
8. 用户要求处理 PDF、Word、Obsidian、Canvas、Excalidraw 等格式时，才启用对应工具技能。

### 2.3 灵活性规则
- 默认采用最小输入模式：能从现有进度、计划、文件中推断时，不额外追问。
- 只有在会覆盖个人内容、删除文件、改变长期规则、或缺少关键事实会导致错误时才询问。
- 日常任务只加载入口技能和必要子模块，避免一次性读取大量技能。
- `core` 类技能默认视为后台基础设施，不作为普通学习入口，除非用户询问配置、状态、欠账、同步、跨学科关联。
- 新增能力时优先扩展现有入口或子模块；只有出现稳定、可复用、边界清楚的新工作流时才新建技能。

### 2.4 技能维护规则
- `SKILL.md` 是标准入口文件名；历史小写 `skill.md` 应逐步迁移为 `SKILL.md`。
- `SKILL.md` 超过 300 行、`code.md` 超过 400 行时，使用 `/skill-refactor` 拆分。
- 技能说明只写触发条件、路由决策、关键约束；长模板、代码、数据表放到 `code.md`、`templates/` 或 `references/`。
- 修改 Codex 侧项目架构、技能、命令、hook、MCP 或说明时，必须同步检查 Claude Code 侧对应结构。

详细技能地图见 `.claude/SKILL_SYSTEM.md`。

---

## 3. Codex / Claude Code 同步规则
- `AGENTS.md` 与 `CLAUDE.md` 必须保持核心规则一致。
- `.agents/skills` 与 `.claude/skills` 应保持等价能力；若某技能只能在单端实现，回复中必须说明差异、原因和替代方案。
- 更新技能、命令、hook、MCP、项目级说明后，必须做一致性检查。
- 不把临时学习经验直接提升到 `CLAUDE.md`；新经验只写入 `.learnings/RULES.md`，由启动注入机制加载。

---

## 4. 每日标准工作流
1. **Start**：执行 `/sync 拉取`，获取最新进度与错题上下文。
2. **Plan**：执行 `/kaoyan-plan`，结合疲劳度、可用时间、任务欠账生成课表。
3. **Study**：通过科目路由器进入数学、英语、专业课学习。
4. **Verify**：重要节点用 `/understanding` 验证逻辑链，必要时生成 `[!personal]` 记录。
5. **Update**：向 `/kaoyan-plan` 汇报完成情况，触发每日计划、完成记录、各科进度更新。
6. **End**：执行 `/sync 上传`，将学习状态、错题、关键经验落盘至 MemOS。

---

## 5. 时间与疲劳度调度算法

### 5.1 最小时间块
- 数学中高难度：不少于 1.5 小时，禁止碎片化。
- 英语阅读、专业课、数学概念：不少于 1.0 小时。
- 单词、政治选择题：可碎片化，建议 15-20 分钟。

### 5.2 疲劳度降级
疲劳度公式：`Fatigue = 主观感受(0.6) + 行为数据(0.4)`

| 疲劳度 | 策略 |
| --- | --- |
| `< 0.3` 精力很好 | 正常排期，休息占比 15% |
| `0.3-0.5` 正常 | 正常排期，休息占比 20% |
| `0.6-0.8` 有点累 | 削减 10%-20% 任务量，休息占比 25% |
| `> 0.8` 很累 | 削减 30%+ 任务量，开启长休息/休息日，休息占比 30%+ |

### 5.3 时段优先级
- 上午 08:00-12:00：数学、英语单词。
- 下午 14:00-18:00：英语阅读、专业课。
- 晚上 19:00-23:00：专业课、政治复盘。
- 23:00 后：仅复习，禁止排期新内容。

---

## 6. 数据安全与保护边界
严禁修改、覆盖或删除以下区块及包含此类特征的内容；更新时必须追加或跳过：
- `## 个人笔记` / `## My Insights`
- `## 随手记` / `## Quick Notes`
- `## 学习心得` / `## Learnings`
- `## 踩坑记录` / `## Pitfalls`
- `## 待探索` / `## TODO`
- 任何以 `> [!personal]` 开头的 callout 块

数学证明、推导类内容统一使用 `> [!note]-` 单一折叠块；写入包含表格的文件后检查 Obsidian Markdown 表格格式，表格内 LaTeX 绝对值使用 `\lvert...\rvert`，避免管道符破坏渲染。

---

## 7. 自学习与多 Agent 同步规则

### 7.1 经验库规则

1. **任务前读取经验库**：执行任何任务前，先读取或参考会话启动时注入的经验库提醒：
   - `.learnings/RULES.md`：提炼后的铁律；
   - `.learnings/LEARNINGS.md`：学习心得；
   - `.learnings/ERRORS.md`：错误日志。

2. **错误不只记录，还要修源头**：如果同类错误反复出现，或某条规则已写入 `RULES.md` 但仍复发，使用 `maintain-learnings` 追溯并修改对应 skill、模板、hook、校验脚本或项目规则。修复并验证后，才归档或移除活跃记录。

3. **记录要短，规则要可执行**：学习记录写事实和根因；`RULES.md` 写简洁规则，例如“用 X 而非 Y”。不要把 `.learnings/` 变成冗长日志库。

4. **Hook 自动读取**：Codex / Claude Code 通过各自 hooks 目录运行 `read_learnings.py` 或 `read-learnings.sh`，在会话开始时注入经验库提醒。若 hook 配置不存在，先安装或合并 self-learning 模板中的 hook 配置。

### 7.2 多 Agent 自学习同步规则

- Codex profile 默认使用 `.agents/skills/`。
- Claude Code profile 默认使用 `.claude/skills/`。
- 通用 profile 默认使用 `.agent/skills/`；其他 agent 可使用项目自定义 skills 目录。
- 新增或更新任何共享 self-learning skill 后，必须确认相关 profile 都保留同等功能：

```bash
python3 .agents/skills/maintain-learnings/scripts/sync_platform_skills.py --root . --skill <skill>
```

- 如果报告另一侧缺失，先补齐另一侧再结束任务。
- Codex UI 元数据（如 `agents/openai.yaml`）只留在 `.agents/`。
- Claude Code 专属 hook / settings 只留在 `.claude/`。
- 其他 agent 的入口文件、Hook、工具权限和平台限制只留在各自 profile 中。
- 同步前必须比对差异，保留平台专属命令、Hook、工具说明和平台限制。

### 7.3 推荐触发语

- “记录一下这次学习”
- “把这次错误写进 learnings”
- “learnings 太多了，帮我维护”
- “这个错误又犯了，去修源头”
- “同步多 agent 的技能”

<!-- env-template:claude:begin -->
## Environment Variables

- Follow `.claude/rules/common/env.md` whenever creating, updating, migrating, or auditing `.env`, `.env.example`, or environment-variable documentation.
- Keep committed env templates minimal, project-specific, and free of real secrets or machine-local absolute paths.
- After env template changes, run `.claude/scripts/check-env-template.sh`. Use `--strict` when you want unused documented variables to fail the check.
<!-- env-template:claude:end -->



<!-- workflow-todo-state:start -->
## Workflow Todo State

Named workflow state files are the source of truth for every routed workflow.

- Workflow definitions live under `.claude/workflows/{workflow-id}/`.
- Workflow state files live under `workspace/workflow-runs/` and should be named after the task, for example `payment-refactor.workflow.md`.
- Before any action that changes project files, runs project commands, or calls external services, read `.claude/rules/workflow-routing.md` and match the user's original request against its triggers and exclusions.
- When a `Required: yes` workflow matches, read its `workflow.md`, create or resume its state file, and start the current phase before doing the work. Do not take the ordinary execution path instead.
- If the route is ambiguous, ask the user before acting.
- Read the active workflow state file before starting any phase; do not skip prerequisite phases.
- Change phase state only through `.claude/scripts/todo-state.sh`.
- Use one unique phase status line per phase, for example `> [P0] ⬜ 未开始`.
- On resume after interruption, inspect the YAML frontmatter and current phase before acting.
- Each workflow directory must contain a `routing.yaml`. After creating, changing, renaming, or deleting a workflow, run `.claude/scripts/sync-workflow-routing.sh`; the update is incomplete until `.claude/scripts/sync-workflow-routing.sh --check` passes.
<!-- workflow-todo-state:end -->
