
# 2026-08-26 Learnings Maintenance

本次维护依据 .agents/skills/maintain-learnings/scripts/audit_learnings.py 审计；已修复源头、完成验证后归档活跃记录。

## [LRN-20260802-001] best_practice

**原摘要**：多 agent profile 的 SessionStart 经验注入曾重复注册。

**源头修复**：保留各 profile 的单一 read_learnings.py 注入入口；将 ops.hook_duplication 纳入 .learnings/RULES.md 的 Watch For。

**验证**：grep 枚举 .codex、.claude、.codebuddy 等 profile 的 hook 注册，确认每个 profile 只有一个实际 SessionStart 命令；规则模式已保留。

**处理结果**：已验证并归档。

## [LRN-20260805-001] best_practice

**原摘要**：必背笔记不能只保留公式结论，方法型内容必须能启动做题。

**源头修复**：.agents/skills/kaoyan-notes-update/SKILL.md 保留并强化“核心思想 + 操作模板 + 回读验证”要求；将 notes.conclusion_only_reject 纳入 Watch For。

**验证**：技能文件包含六要素骨架、方法型操作模板和验证清单；当前二次型模块已按该骨架写入。

**处理结果**：已验证并归档。

## [LRN-20260810-001] correction

**原摘要**：写作必背笔记前必须确认章节进度，避免引入尚未学习的向量空间等概念。

**源头修复**：保留 .learnings/RULES.md 中的 notes.knowledge_boundary 规则。

**验证**：当前规则明确要求读取章节进度，并限制未学章节术语。

**处理结果**：已验证并归档。

## [LRN-20260810-002] best_practice

**原摘要**：行向量组表示方向与解集包含方向容易写反。

**源头修复**：保留 .learnings/RULES.md 中的方向核验规则，并将 notes.solution_direction 纳入 Watch For。

**验证**：规则明确要求按“表示方向 → 约束强弱 → 解集大小”核验。

**处理结果**：已验证并归档。

## [LRN-20260826-001] correction

**原摘要**：当前 Obsidian vault 中，\(...\) 行内数学显示异常，应使用 $...$。

**源头修复**：在 .agents/skills/kaoyan-notes-update/SKILL.md 的格式约束和验证清单中加入 $...$ / $$...$$ 规则；在 .learnings/RULES.md 中加入 obsidian.inline_math_delimiter。

**验证**：目标笔记已无 \(...\)；行内公式改为 $...$，块公式分隔符成对，控制字符扫描通过。

**处理结果**：已验证并归档。

## [ERR-20260826-001] write_markdown_latex

**原摘要**：首次追加含 LaTeX 的 Markdown 命令因 JavaScript 普通字符串转义失败。

**源头修复**：在 .agents/skills/kaoyan-notes-update/SKILL.md 加入 String.raw + quoted heredoc / 外部脚本约束，并要求写后扫描控制字符。

**验证**：技能元数据检查通过；后续写入使用 String.raw、quoted heredoc 和控制字符扫描成功。

**处理结果**：已验证并归档。

## 工具修复：audit_learnings.py

审计脚本原先把 Summary、Details 等嵌套字段误识别为独立记录；已在 .agents/skills/maintain-learnings/scripts/audit_learnings.py 增加 ENTRY_HEADING_RE，仅以 LRN/ERR 记录标题切分经验条目。重新运行审计后，候选记录显示为真实记录 ID。

---
