# Skill Invocation

## 技能列表
<!-- skill-registry:managed ["ask-matt","chapter-summary","claude-handoff","code-review","codebase-design","defuddle","diagnosing-bugs","digest","docx","domain-modeling","excalidraw-diagram","fix-table-pipe","git-guardrails-claude-code","grill-me","grill-with-docs","grilling","handoff","handwritten-note-reconstruction","implement","improve-codebase-architecture","json-canvas","kaoyan-electronics","kaoyan-electronics-circuit","kaoyan-electronics-core","kaoyan-electronics-diagram","kaoyan-electronics-sop","kaoyan-electronics-structure","kaoyan-english","kaoyan-english-core","kaoyan-english-quiz","kaoyan-english-review","kaoyan-english-vocab","kaoyan-english-writing","kaoyan-info","kaoyan-math","kaoyan-math-core","kaoyan-math-notes","kaoyan-math-structure","kaoyan-notes-update","kaoyan-plan","knowledge-base-organizer","knowledge-learning","knowledge-mindmap","learning-response-contract","loop-me","maintain-learnings","manifest-platform","math-graph","mcp-builder","migrate-to-shoehorn","mistake-book","mistake-extract","mistake-restructure","obsidian-bases","obsidian-cli","obsidian-markdown","opencli-adapter-author","opencli-autofix","opencli-browser","opencli-usage","parse-words","pdf","prompt-cache-optimizer","prototype","research","resolving-merge-conflicts","scaffold-exercises","security-secret-audit","setup-matt-pocock-skills","setup-pre-commit","setup-ts-deep-modules","skill-refactor","smart-search","sortspec-generator","sync","sync-skill-registry","tdd","teach","to-questionnaire","to-spec","to-tickets","triage","understanding","wait-what","wayfinder","wizard","word-template-generator","workflow-todo-state","writing-beats","writing-for-agents","writing-fragments","writing-shape"] -->

#### 未分类

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this… | Ask which skill or flow fits your situat… |
| `chapter-summary` | 整理考研数学/专业课章节笔记，生成结构化总结文件。**触发词**："章节总结"、"整理章节"、"汇总这一章"、"章节笔记"、"数学���记总结"、"整理数… | 章节总结、整理章节、汇总这一章、章节笔记、数学���记总结、整理数学笔记、做一个总结、总结一下这一章 |
| `claude-handoff` | Hand the current conversation off to a fresh background agent that picks up t… | Hand the current conversation off to a f… |
| `code-review` | Review the changes since a fixed point (commit, branch, tag | review since X |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to desi… | Shared vocabulary for designing deep mod… |
| `defuddle` | Extract clean markdown content from web pages using Defuddle CLI | Extract clean markdown content from web … |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user s… | diagnose、debug this |
| `digest` | 自我学习阶段。回顾本次学习会话，记录学习心得和错误到 .learnings/，当文件超阈值时自动压缩去重，更新 RULES.md | 自我学习阶段 |
| `docx` | "Use this skill whenever the user wants to create, read, edit | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation. |
| `domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin do… | Build and sharpen a project's domain mod… |
| `excalidraw-diagram` | Generate Excalidraw diagrams from text content. Supports three output modes -… | Excalidraw、画图、流程图、思维导图、可视化、diagram、标准Excalidraw、standard excalidraw |
| `fix-table-pipe` | 修复 Markdown 表格渲染问题，包括：(1) Callout 块内表格前缺少空行； | 表格格式错误、表格显示异常、表格渲染问题、Callout 表格 |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard | Set up Claude Code hooks to block danger… |
| `grill-me` | A relentless interview to sharpen a plan or design. | A relentless interview to sharpen a plan… |
| `grill-with-docs` | A relentless interview to sharpen a plan or design | A relentless interview to sharpen a plan… |
| `grilling` | Grill the user relentlessly about a plan, decision | Grill the user relentlessly about a plan… |
| `handoff` | Compact the current conversation into a handoff document for another agent to… | Compact the current conversation into a … |
| `handwritten-note-reconstruction` | Internal cross-subject protocol for reconstructing handwritten study notes | Internal cross-subject protocol for reco… |
| `implement` | "Implement a piece of work based on a spec or set of tickets." | Implement a piece of work based on a spec or set of tickets. |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities | Scan a codebase for deepening opportunit… |
| `json-canvas` | Create and edit JSON Canvas files (.canvas) with nodes, edges, groups | Create and edit JSON Canvas files (.canv… |
| `kaoyan-electronics` | 822电子技术基础考研学习入口。用于湖南大学822专业课的新学、题型训练、错题回收、章节复盘、模电/数电进度推进。默认围绕“章节输入 -> 题型SOP -… | 章节输入 -> 题型SOP -> 错题归因 -> 进度更新 |
| `kaoyan-electronics-circuit` | 822电子技术基础电路图与电路题分析模块。用于图片/文字电路识别、模电静态/动态分析、数电逻辑/时序分析、电路图生成、微变等效图生成 | 822电子技术基础电路图与电路题分析模块 |
| `kaoyan-electronics-core` | 822电子技术基础核心协调模块。用于专业课进度、欠账、阶段策略、错题标签、MemOS同步、模电/数电优先级和与kaoyan-plan的完成汇报联动。 | 822电子技术基础核心协调模块 |
| `kaoyan-electronics-diagram` | Use when generating, redrawing, correcting, exporting | Use when generating, redrawing, correcti… |
| `kaoyan-electronics-sop` | 822电子技术基础题型SOP模块。用于模电/数电高频题型训练、解题步骤、检查清单、错题归因和考研答题模板。 | 822电子技术基础题型SOP模块 |
| `kaoyan-electronics-structure` | 822电子技术基础知识结构与章节复盘模块。用于模电/数电章节定位、前置知识判断、高频题型映射、学习顺序建议、章节卡片和进度骨架生成。 | 822电子技术基础知识结构与章节复盘模块 |
| `kaoyan-english` | 考研英语入口路由器。用于英语二词汇、阅读高亮词、复习计划、单词测试、写作输出训练和英语学习状态检查。默认只加载一个最匹配子模块：vocab、review、… | 考研英语入口路由器 |
| `kaoyan-english-core` | This skill manages the core infrastructure for 考研英语 (Chinese graduate entranc… | This skill manages the core infrastructu… |
| `kaoyan-english-quiz` | This skill handles vocabulary quizzes and testing for 考研英语 (Chinese graduate … | This skill handles vocabulary quizzes an… |
| `kaoyan-english-review` | This skill handles review planning and progress tracking for 考研英语 (Chinese gr… | This skill handles review planning and p… |
| `kaoyan-english-vocab` | This skill handles vocabulary organization and word lookup for 考研英语 (Chinese … | This skill handles vocabulary organizati… |
| `kaoyan-english-writing` | This skill handles writing output training for 考研英语 (Chinese graduate entranc… | This skill handles writing output traini… |
| `kaoyan-info` | This skill should be used when the user asks to collect graduate entrance exa… | This skill should be used when the user … |
| `kaoyan-math` | 考研数学入口路由器。用于数学二学习中的概念理解、笔记生成、推导补全、题目讲解、知识结构查询、进度/欠账检查。默认只加载一个最匹配子模块：notes、str… | 考研数学入口路由器 |
| `kaoyan-math-core` | This skill manages the core infrastructure for 考研数学 (Chinese graduate entranc… | This skill manages the core infrastructu… |
| `kaoyan-math-notes` | This skill handles note generation and updates for 考研数学 (Chinese graduate ent… | This skill handles note generation and u… |
| `kaoyan-math-structure` | This skill provides knowledge point structure templates and module organizati… | This skill provides knowledge point stru… |
| `kaoyan-notes-update` | 向必背/速查类笔记（如《线性代数必背知识》）补充新内容的标准流程。 | 复习知识点、会做题，不只背结论、识别特征→核心思想→操作模板→公式→口诀→易错点、补充必背知识/往必背笔记加内容/更新速查/这里如何补充进第X节 |
| `kaoyan-plan` | Generate and maintain 考研 study plans, daily schedules, weekly reviews | 今天怎么学、安排计划、完成了什么、补计划、周复盘 |
| `knowledge-base-organizer` | This skill should be used when the user asks to organize documents | This skill should be used when the user … |
| `knowledge-learning` | This skill should be used when the user asks to learn about a topic | This skill should be used when the user … |
| `knowledge-mindmap` | 自动分析知识点目录结构，生成 Excalidraw 格式的详细思维导图。 | 知识点思维导图、生成思维导图、知识结构图、目录结构图 |
| `learning-response-contract` | Internal learning-response contract. Subject entry skills use it to choose on… | Internal learning-response contract |
| `loop-me` | Grill me about specs for the workflows I want to build, within this workspace. | Grill me about specs for the workflows I… |
| `maintain-learnings` | 维护 .learnings/ 经验库，把过多或反复出现的学习记录、错误日志、规则失效问题聚类诊断，追溯并修改对应 skill、模板、hook、校验脚本或项目规则； | 维护 .learnings/ 经验库，把过多或反复出现的学习记录、错误日志、规则… |
| `manifest-platform` | Install, configure, migrate, and validate a portable manifest registry for ag… | Install, configure, migrate, and validat… |
| `math-graph` | 使用 Python + Matplotlib 生成教科书级别的数学函数图像。 | 使用 Python + Matplotlib 生成教科书级别的数学函数图像 |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that ena… | Guide for creating high-quality MCP (Mod… |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. U… | Migrate test files from `as` type assert… |
| `mistake-book` | This skill helps users quickly organize mistakes/errors into subject-specific… | 整理错题、记错题、错题笔记、把这道题记到错题本 |
| `mistake-extract` | 错题精华提炼技能。从指定模块的错题本中提取核心口诀、避坑要点、关键认知、解题方法模板、检查清单、核心陷阱、常见错误模式，生成结构化提炼笔记。 | "错题精华"、"提炼错题"、"精华提炼"、"错题提炼"、"提取精华"、"生成精华本"、"错题精华总结" |
| `mistake-restructure` | 错题本结构优化技能。自动分析错题关联、按知识点分类索引、生成关联网络图。 | "重构错题本"、"整理错题结构"、"优化错题索引" |
| `obsidian-bases` | Create and edit Obsidian Bases (.base files) with views, filters, formulas | Create and edit Obsidian Bases (.base fi… |
| `obsidian-cli` | Interact with Obsidian vaults using the Obsidian CLI to read, create, search | Interact with Obsidian vaults using the … |
| `obsidian-markdown` | Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts | Create and edit Obsidian Flavored Markdo… |
| `opencli-adapter-author` | Use when writing an OpenCLI adapter for a new site or adding a new command to… | Use when writing an OpenCLI adapter for … |
| `opencli-autofix` | Automatically fix broken OpenCLI adapters when commands fail. Load this skill… | Automatically fix broken OpenCLI adapter… |
| `opencli-browser` | Use when an agent needs to drive a real Chrome window via opencli — inspect a… | Use when an agent needs to drive a real … |
| `opencli-usage` | Use at the start of any OpenCLI session — this is the top-level map of what `… | what can opencli do?、how do I find the right command? |
| `parse-words` | This skill should be used when the user asks to parse highlighted English wor… | This skill should be used when the user … |
| `pdf` | Use this skill whenever the user wants to do anything with PDF files. This in… | Use this skill whenever the user wants t… |
| `prompt-cache-optimizer` | 审计并优化 LLM 提示缓存命中率、输入 token、延迟与调用成本。 | 优化缓存命中、降低 token 成本、审计 LLM 调用、提示词缓存优化、优化 AI 调用费用 |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the user wa… | Build a throwaway prototype to answer a … |
| `research` | Investigate a question against high-trust primary sources and capture the fin… | Investigate a question against high-trus… |
| `resolving-merge-conflicts` | "Use when you need to resolve an in-progress git merge/rebase conflict." | Use when you need to resolve an in-progress git merge/rebase conflict. |
| `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions | Create exercise directory structures wit… |
| `security-secret-audit` | Audit a Git repository for exposed API keys, tokens, passwords, private keys | Audit a Git repository for exposed API k… |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills — set up its issue tracker | Configure this repo for the engineering … |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking | Set up Husky pre-commit hooks with lint-… |
| `setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep modu… | Wire dependency-cruiser into a TypeScrip… |
| `skill-refactor` | 技能自动化重构器 - 自动提取代码到code.md、拆分过长内容、优化技能结构。 | 重构技能、拆分技能、技能代码分离、优化技能结构 |
| `smart-search` | 基于 opencli 命令的智能搜索路由器。当用户想要搜索、查询、查找或研究信息时 | 基于 opencli 命令的智能搜索路由器 |
| `sortspec-generator` | \| | \| |
| `sync` | This skill should be used when the user asks to sync study progress with MemOS | This skill should be used when the user … |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bug… | red-green-refactor |
| `teach` | Teach the user a new skill or concept, within this workspace. | Teach the user a new skill or concept, w… |
| `to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else … | Turn a decision you can't fully answer i… |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue… | Turn the current conversation into a spe… |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet t… | Break a plan, spec, or the current conve… |
| `triage` | Move issues and external PRs through a state machine of triage roles — catego… | Move issues and external PRs through a s… |
| `understanding` | This skill should be used when the user wants to verify whether their underst… | This skill should be used when the user … |
| `wait-what` | Stop. That last message did not land — re-pitch it. | Stop |
| `wayfinder` | Plan a huge chunk of work — more than one agent session can hold — as a share… | Plan a huge chunk of work — more than on… |
| `wizard` | Generate an interactive bash wizard that walks a human through steps only the… | Generate an interactive bash wizard that… |
| `word-template-generator` | This skill should be used when the user wants to process Word document templa… | This skill should be used when the user … |
| `workflow-todo-state` | Create or retrofit reusable named workflow state machines for multi-step agen… | Create or retrofit reusable named workfl… |
| `writing-beats` | Writing, exploit — assemble raw material into a journey of beats | Writing, exploit — assemble raw material… |
| `writing-for-agents` | Writing documents for agents. Use when creating or editing skills | Writing documents for agents |
| `writing-fragments` | Writing, explore — mine raw fragments, no structure yet. | Writing, explore — mine raw fragments, n… |
| `writing-shape` | Writing, exploit — shape raw material into an article, paragraph by paragraph. | Writing, exploit — shape raw material in… |

#### 工具发现

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `sync-skill-registry` | 技能注册表同步工具。扫描任意 agent skill 目录中的 */SKILL.md 并自动更新对应 skill-invocation.md 中的技能列表… | 同步注册表、更新技能列表、sync skill registry、update skill registration、刷新技能列表、同步技能表格 |

### 1. 分析意图

根据用户请求选择最合适的可复用 skill 或模板。
