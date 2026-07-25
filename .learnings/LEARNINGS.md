# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260721-004] best_practice

**Logged**: 2026-07-21T19:34:00+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/study-route

### Summary
补充学习笔记时，必须保证内容插入后的学习路线顺畅、合理，而不只是局部内容完整。

### Details
本次把“放大的根源”整理进 BJT 笔记时，初始插入到了 NPN 放大区小节下，导致层级暗示错误：读者会误以为“放大的根源”只是 BJT 工作区的附属内容。用户指出排版不对后，重新调整为“先讲放大的总思想，再讲 BJT 器件基础，再讲工作区判断，最后给最低掌握标准”。由此确认：补充笔记时必须先看整章学习路线和前后依赖，而不是只把新内容塞进看似相关的小节。

### Suggested Action
以后补充或扩写笔记前，先做“学习路线检查”：明确当前补充内容属于前置概念、核心定义、推导证明、题型方法、例题错题还是复盘总结；再确认它应该放在章节开头、中段推导、题型区还是总结区。写入后回读标题树，检查顺序是否符合“为什么学 → 学什么 → 怎么判断/计算 → 易错点 → 最低掌握标准”。若不顺畅，优先重排结构再结束。

### Related Rules
Pattern-Key: notes.learning_route_coherence
Pattern-Key: markdown.heading_tree_review

### Resolution
2026-07-21：已同步到 `.learnings/RULES.md` 的 Do / Watch For 区。

---


## [LRN-20260721-005] best_practice

**Logged**: 2026-07-21T19:30:02+08:00
**Priority**: medium
**Status**: pending
**Area**: docs/obsidian/markdown-table

### Summary
Markdown 表格即使列数和语法正确，也可能因为列太多、公式与中文混排过宽而在 Obsidian 中显示不佳。

### Details
本次“四类放大倍数”表格原本有 6 列：输入量、输出量、名称、定义式、单位、等效受控源直觉。检查后发现每行列数一致，也没有 LaTeX 管道符或控制字符污染；问题主要是宽表在 Obsidian 阅读视图中容易被压缩错位。后续将 6 列合并为 4 列，把输入/输出/受控源解释合并到“读法与受控源直觉”列，显示更稳定，也更适合复习阅读。

### Suggested Action
以后写入 Obsidian 表格时，不只检查 Markdown 语法和管道符，还要检查阅读宽度：如果表格超过 4 列，或单元格同时包含中文长句、行内公式和英文缩写，应优先改成短表、列表或分组表；复习型笔记优先保证移动端/窄窗阅读顺畅，而不是保留信息密度最高的宽表。

### Related Rules
Pattern-Key: table.readability_width
Pattern-Key: obsidian.table_layout_review

---

## [LRN-20260723-001] best_practice

**Logged**: 2026-07-23T09:17:03+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/quick-review

### Summary
更新必背/速查类笔记时，不能只筛公式；凡是对用户学习、复习、做题有帮助的 SOP、流程、判断准则和易错检查都要优先提炼放入。

### Details
本次整理“条件最值与拉格朗日乘数法”时，首次判断过度受“速查页别太长”约束影响，只把“闭区域最值问题 SOP（两步走，最后比大小）”弱化为一般提醒，没有把它作为核心内容放入。用户指出后确认：闭区域最值 SOP 能直接防止漏查内部驻点、漏查端点、只用拉格朗日、比错对象等高频错误，属于比单纯公式更重要的复习型知识。

### Suggested Action
以后从章节笔记抽取内容到必背/速查页时，先按“对学习/复习/做题是否有帮助”判断价值：高价值对象包括定义、公式、性质、口诀、SOP、启动步骤、题型流程、判断准则、易错检查清单、候选点完整策略。不要因为内容不是公式或略长就降权；应压缩成速查版并放入，而不是遗漏。

### Related Rules
Pattern-Key: notes.review_value_extraction
Pattern-Key: notes.quick_review_extract

### Resolution
2026-07-23：已同步到 `.learnings/RULES.md` 的 Do / Watch For 区。

---


## [LRN-20260724-001] correction

**Logged**: 2026-07-24T20:05:52+08:00
**Priority**: high
**Status**: pending
**Area**: docs/obsidian/handwritten-notes

### Summary
处理手写图片笔记时，必须先识别图片真实主题和电路拓扑，再决定写入哪个笔记与章节。

### Details
本次整理模电手写图时，先被当前笔记文件名“分压式射极偏置”带偏，把图片内容误归入分压式射极偏置。用户指出后重新查看图片，确认三张手写图实际在讲“直接耦合”和“阻容耦合”：直接耦合中输入源进入基极偏置回路、静态点会互相牵连；阻容耦合中输入/输出通过电容隔直通交，静态时电容开路、交流时电容近似短路。错误根因是没有先逐张识别图片标题、关键文字、电路拓扑和知识点归属，就直接按当前 note 名称改写笔记。

### Suggested Action
以后处理用户手写图片、截图或教材图并写入笔记前，先完成“图片识别卡”：1. 抄出图片标题/关键词；2. 识别电路拓扑、元件和信号路径；3. 判断它属于哪个知识点/章节；4. 若图片内容与当前笔记标题不一致，先说明不一致并写入更合适的笔记，不能强行按当前文件名归类。

### Related Rules
Pattern-Key: image_note.semantic_routing_before_write

---


## [LRN-20260725-001] best_practice

**Logged**: 2026-07-25T21:29:41+08:00
**Priority**: high
**Status**: pending
**Area**: docs/obsidian/handwritten-notes

### Summary
手写笔记写入后，必须主动回看整篇标题树和学习路线，判断新增内容是否应升为独立模块，而不只是局部追加正确。

### Details
本次整理“固定偏置共射电路图解法”手写笔记时，先正确识别了静态 Q 点、动态电压放大倍数、输入/输出负载线和反相结论，也补画了标准图。但第一次写入时只做了局部落点判断，把“图解法看电压放大倍数”挂成 `5.5.1`，像是 `R_C` 输出公式的附属内容。用户追问“为什么放入笔记时不帮我重新排版”后，才将它升成独立的 `5.6` 模块，并拆成输入侧、输出侧、放大倍数符号三段。

### Suggested Action
以后处理手写笔记并写入已有章节时，完成内容追加后必须执行“标题树回看”：1. 列出当前章节标题；2. 判断新增内容是前置概念、静态分析、动态分析、题型方法、易错点还是总结；3. 若新增内容承担新的学习阶段，应主动升为独立模块并顺号；4. 更新开头学习顺序说明；5. 回读确认阅读路线符合“先定对象/状态 → 再看变化过程 → 最后总结做题结论”。

### Related Rules
Pattern-Key: notes.learning_route_coherence
Pattern-Key: markdown.heading_tree_review
Pattern-Key: handwritten_note.post_insert_relayout

---
