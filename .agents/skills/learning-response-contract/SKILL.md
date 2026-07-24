---
name: learning-response-contract
description: Internal learning-response contract. Subject entry skills use it to choose one response mode before routing to subject modules; it is not a standalone daily learning entry.
version: 1.0.0
---

# 学习回答契约

## 使用边界

本协议只由数学、英语、专业课和计划入口在判定学科后调用。目标是让回答先匹配用户此刻的学习动作，再加载对应的知识、SOP 或文件流程。

先选回答模式，再选学科和子模块；只有写入被明确请求或确有长期价值时，才启动文件更新。目标路径不明时，不创建文件。

| 模式 | 触发 | 最小输出 |
| --- | --- | --- |
| `quick_answer` | 局部为什么、是什么、怎么判断 | 结论、2-4 个关键步骤、一个易错点、一个自检 |
| `concept_learning` | 讲懂、系统整理一个知识点 | 钩子、TL;DR、为什么、是什么、怎么用、微型自测 |
| `problem_solving` | 题目、错因、解法 | 题型、SOP、分步解、错因、下次触发点 |
| `note_reconstruction` | 笔记、图片、手写、板书 | 来源盘点、重构正文、图示、速查、原图溯源 |
| `planning_review` | 安排、完成、复盘 | 策略、时间块或记录、兜底、下一次汇报 |

## 选择顺序

```text
请求动作 / 回答模式 → 学科 → 子模块 → 是否写入文件 → 质量门槛
```

- 请求只涉及一个局部疑问时，默认 `quick_answer`，不扩展成整章笔记。
- 用户要求理解一组相关知识时，使用 `concept_learning`。
- 用户提供题目、答案或错误步骤时，使用 `problem_solving`。
- 用户提供手写笔记、课堂板书、截图或要求整理笔记时，使用 `note_reconstruction`；数学和电子技术须继续调用 `handwritten-note-reconstruction`。
- 用户要求计划、完成记录、欠账处理或复盘时，使用 `planning_review`，由 `kaoyan-plan` 接管。

若无法确定学科或文件位置，先完成不依赖该信息的最小回答；只有公式体系、图示含义、目标路径或答案正确性确实依赖缺失信息时，询问一个最小澄清问题。

## 高风险质量门槛

| 场景 | 必做检查 |
| --- | --- |
| 数学计算或推导 | 独立验算；检查定义、条件、边界和推导链 |
| 专业课电路 | 检查拓扑、端口、接地、电源、方向和反馈路径 |
| 题目解析 | 先完整识别题目；题干、步骤与答案相互核对 |
| 手写笔记 | 图文双轨、待确认项、原图溯源、正文可独立学习 |
| 写入 Obsidian | 保护个人区块；回读公式、表格、图片链接与格式 |

普通解释不额外套审查清单，以免把回答变慢、变长。
