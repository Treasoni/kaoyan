# Learnings

Self-improvement patterns, corrections, and knowledge gaps.

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

## [LRN-20260801-004] best_practice

**Logged**: 2026-08-01T13:00:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: docs/linear-algebra/quick-reference

### Summary
用户对必背定理提供自己的理解时，先验证逻辑正确性，再压缩为「机制本质 + 方向结论」，用 `> [!note]-` 折叠块嵌入必背页对应结论附近，不搬完整推导，不动原结论行与易错提醒。

### Details
用户对「延长与缩短」定理给出方程视角三段推理（$s$ 个向量 = $s$ 个未知数、$n$ 维 = $n$ 个方程；延长向量组 = 给方程组加方程 = 约束变强；加方程缩小解集、减方程放大解集，从而解释「延相关⟹缩相关、缩无关⟹延无关」）。我验证逻辑正确后，没有整段搬进必背页，而是提取机制本质（「延长 = 加方程 = 约束变强」）与两条方向结论，以默认折叠的 `> [!note]-` 块放在 §8.5 常用结论速查表之后，原表格行「反向不一定」的易错提醒保留不动。

### Suggested Action
遇到用户主动提供对定理/公式的个人理解时：(1) 先用方程/代入视角验证其逻辑正确性；(2) 只提取「机制本质 + 方向结论」，不搬运完整推导；(3) 用 `> [!note]-` 折叠块嵌入必背页对应结论附近（表格后/小节末）；(4) 不破坏已有结论行与易错提醒，折叠块与结论行互补。

### Related Rules
Pattern-Key: notes.theorem_intuition_embed
Pattern-Key: notes.quick_review_extract
Pattern-Key: obsidian.proof_collapsible
Pattern-Key: math.explain_human_bridge

### Resolution
2026-08-01：用户确认同步后，已更新 `.learnings/RULES.md` 的 Do 区（「用户对定理/公式提供个人理解时，先验证逻辑正确性，再压缩为机制本质 + 方向结论，用 `> [!note]-` 折叠块嵌入必背页对应结论附近；不搬完整推导，不动原结论行与易错提醒」）与 Watch For 区（`notes.theorem_intuition_embed`）。

---
