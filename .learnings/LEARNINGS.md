# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

---

## [LRN-20260727-001] best_practice

**Logged**: 2026-07-27T20:03:47+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/handwritten-notes

### Summary
处理用户多页手写笔记时，必须逐页展示与识别，不能只给一张总结图或把原图全部折叠到来源里。

### Details
本次整理“图解法分析共射电压放大倍数”三页手写笔记时，先把内容整理进笔记并生成了标准总结图，但最终汇报和笔记呈现偏向一张重绘图，导致用户质疑“三张图为什么只给一张，是否完整看懂”。复核后确认三页实际承担不同逻辑层：第 1 页是固定偏置共射电路的静态基础，第 2 页是输入负载线随交流输入平移，第 3 页是输出特性族线、反相波形与 $A_u=-10$。最终补救方案是在正文中加入“5.6.0 三页手写图识别卡”，每页原图直接可见，并配视觉盘点、解决的问题、公式链、做题结论和待确认项，再接标准重绘图与公式总结。

### Suggested Action
以后处理用户多页手写笔记、截图或教材图并写入笔记时，默认采用“逐页识别卡 → 标准图/重绘图 → 公式链 → 做题结论 → 标题树回看”的结构：每一页原图都要在正文中直接对应一个知识层，写清视觉盘点、该页解决的问题、关键公式/逻辑链、待确认项和做题结论；原图不能只折叠为来源，也不能被一张总结图替代。完成后回读标题树，确认新增内容符合学习顺序。

### Related Rules
Pattern-Key: handwritten_note.page_card_mapping
Pattern-Key: docs.visual_source_coverage
Pattern-Key: notes.learning_route_coherence

### Resolution
2026-07-27：已同步到 `.learnings/RULES.md` 的 Do / Watch For 区。

---

## [LRN-20260728-001] correction

**Logged**: 2026-07-28T21:36:33+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/electronics/diagrams

### Summary
专业课标准电路图必须先核对标准画法和节点网表，再生成或嵌入笔记。

### Details
整理“固定偏置共射动态指标”手写笔记时，先生成了一张总结图，但图中左上角微变等效电路把基极节点和集电极节点误连，相当于把输入端和输出端短在一起；同时输出电压端口画法也容易被看成上下短接。用户指出“图画错了”后，复核确认这是拓扑错误，不是排版问题。随后改为先查 MIT OCW、Purdue、Berkeley 等标准资料中的共射小信号等效与戴维南端口画法，再按节点关系重画：$r_{be}$ 接 b-e，受控源 $\beta i_b$ 与 $R_C$ 接 c-e，输出端用两个开口端子标 $u_o$。

### Suggested Action
以后生成或整理专业课标准电路图、微变等效图、输出电阻测试图时，先查教材/高校课件的标准画法，再写节点网表卡：输入端、输出端、电源与地、关键节点、受控源控制量、每个元件两端。画完后逐项核对拓扑：BJT 的 b/c/e 节点不能误连，输出端口不能被短接，受控源应按规则保留，求 $R_o$ 时独立源置零但受控源不随手删除。用户质疑图时，先承认并重核拓扑，不先辩解。

### Related Rules
Pattern-Key: electronics.diagram_topology_verify
Pattern-Key: docs.proactive_visual_learning

### Resolution
2026-07-28：已同步到 `.learnings/RULES.md` 的 Do / Don't / Watch For 区。

---
## [LRN-20260801-001] best_practice

**Logged**: 2026-08-01T12:00:00+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/linear-algebra/mistake-book

### Summary
错题去重策略：新错题与已有好题本质相同（仅记法/参数不同）时，不新增编号条目，用折叠关联注释挂到已有条目下。

### Details
用户提供「设 $A^{m-1}\alpha \neq 0$，$A^{m}\alpha = 0$，证明 $\alpha, A\alpha, \cdots, A^{m-1}\alpha$ 线性无关」，验证后确认与已有好题07（零化特性）本质相同，只是记法 $k \leftrightarrow m$。用户选择「不新增，关联好题07」。做法是在好题07下加 `> [!note]- 📎 同题变体：课本例 1（$m$ 记法）` 折叠注释，说明与本题本质相同、方法/避坑/口诀完全复用，不重复记录。另一个例「循环累加型」($\beta_i = \alpha_i + \alpha_{i+1}$ 循环) 与已有好题04/05 的「累加型」本质不同（加号循环 vs 减号循环），确认后新增好题28。

### Suggested Action
记录错题前先检索同目录已有好题是否覆盖同一知识点/同一题型：本质相同仅记法不同 → 折叠关联不新增；本质不同（换结构、换方法）→ 新增编号条目。归档按「知识模块 + 题型本质」双重判断，不只按表象。

### Related Rules
Pattern-Key: mistake.dedup_link

### Resolution
2026-08-01：已同步到 `.learnings/RULES.md` 的 Watch For 区（`mistake.dedup_link`）。

---

## [LRN-20260801-002] best_practice

**Logged**: 2026-08-01T12:05:00+08:00
**Priority**: high
**Status**: resolved
**Area**: docs/obsidian/wikilink-repair

### Summary
大规模修复悬空 wikilink 用 Python 脚本的安全模式：建立「题号/描述→真实笔记」映射、before==after 计数校验、写前备份、写后复审计。

### Details
第四章错题本（错题本.md + 错题题目.md）历史遗留 90 处悬空 wikilink（7 类旧链接）。用 `/tmp/audit_links.py` 全库审计、`/tmp/fix_links.py` 批量替换。映射分两种上下文：索引行（callout 内 `> - [NN](#...`）按题号映射；正文 bullet（`- [[OLD]] — 描述`）按冒号后描述语义映射。脚本用 before==after 计数校验，只有替换次数==原有次数才写入，避免部分替换残留；写前备份到 /tmp，写后复审计到 0 处。

### Suggested Action
遇到批量悬空链接时：先写审计脚本（basename/path 后缀匹配 Obsidian 解析规则）统计；再写修复脚本（区分索引行/正文两类上下文分别映射）；用 before==after 校验 + 备份 + 复审计闭环，不要手动逐条替换。

### Related Rules
Pattern-Key: obsidian.stale_wikilink

### Resolution
2026-08-01：已同步到 `.learnings/RULES.md` 的 Do / Watch For 区（批量修复闭环 + `obsidian.stale_wikilink`）。

---

## [LRN-20260801-003] knowledge_gap

**Logged**: 2026-08-01T12:10:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: docs/obsidian/vault-structure

### Summary
错题本系统性旧链接：笔记文件夹重构后错题本链接未同步，第四章错题本遗留 90 处悬空 wikilink；其他章节可能同类。

### Details
第四章错题本大量使用「章节名式」wikilink（`[[4.1 向量组及其线性相关性]]`、`[[4.3 线性方程组]]` 等），而实际文件夹是「编号式」（`4.1-向量的基本概念`、`4.3-线性相关、线性无关与线性表示`）。推测是文件夹从章节名重构为编号格式后，错题本历史链接未同步更新。本次仅修复第四章，第一、二章错题本可能存在同类问题。

### Suggested Action
建议对全库错题本做一次悬空 wikilink 审计（复用 audit_links.py 的思路），发现同类问题批量修复；生成 wikilink 前务必 Glob 确认目标。

### Related Rules
Pattern-Key: obsidian.stale_wikilink

### Resolution
2026-08-01：已同步到 `.learnings/RULES.md` 的 Do / Watch For 区（批量修复闭环 + `obsidian.stale_wikilink`）。

---
