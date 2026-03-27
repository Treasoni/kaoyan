---
name: kaoyan-math
description: This skill routes mathematics learning requests to specialized sub-skills for 考研数学 (Chinese graduate entrance math exam) preparation, including note generation with LaTeX formatting, knowledge point structure templates, and core infrastructure with MemOS integration for persistent mistake tracking and cross-device synchronization.
---

# 考研数学技能路由器 (Kaoyan Math Router)

## 技能架构

```
kaoyan-math (路由器)
    ↓ 识别意图后调用
    ├─→ kaoyan-math-core      (核心协调层：MemOS集成、调度信号、错误模型)
    ├─→ kaoyan-math-notes     (笔记生成更新：LaTeX格式、知识点模板)
    └─→ kaoyan-math-structure (知识点结构：高数/线代/概率模块)
```

---

## 子技能速查

| 子技能 | 功能描述 | 触发关键词 |
|--------|----------|------------|
| **kaoyan-math-notes** | 笔记生成+更新 | "生成考研数学笔记"、"更新数学笔记"、"我对XX不理解"、"听课时不理解" |
| **kaoyan-math-structure** | 知识点结构 | "数学知识点结构"、"高数目录"、"极限章节结构"、"知识点关系图" |
| **kaoyan-math-core** | 核心协调层 | "数学学习配置"、"数学状态"、"数学欠账检查"、"跨学科关联" |

---

## 使用示例

### 示例1: 笔记生成
**用户输入**："这是我的极限笔记，帮我生成考研学习笔记"
→ 路由到 `kaoyan-math-notes`

### 示例2: 笔记更新
**用户输入**："我对洛必达法则的条件不太理解"
→ 路由到 `kaoyan-math-notes`

### 示例3: 知识点结构
**用户输入**："高数极限章节的知识点结构是什么？"
→ 路由到 `kaoyan-math-structure`

### 示例4: 状态检查
**用户输入**："检查我的数学学习进度"
→ 路由到 `kaoyan-math-core`

---

## 直接调用子技能

用户也可以直接调用子技能，跳过路由器：
- 使用 `kaoyan-math-notes` 生成极限笔记
- 使用 `kaoyan-math-structure` 查看高数目录
- 使用 `kaoyan-math-core` 检查学习状态

---

## 协同技能

| 技能 | 协同场景 |
|------|----------|
| kaoyan-plan | 提供每日计划时间分配，发送调度信号 |
| kaoyan-electronics | 跨学科知识关联（数学→电子技术） |
| obsidian-markdown | 创建Obsidian笔记 |

---

*最后更新: 2026-03-27*
