---
name: kaoyan-english
description: This skill routes English vocabulary learning requests to specialized sub-skills for 考研英语 (Chinese graduate entrance English exam) preparation. It handles vocabulary organization from PDF exports, spaced repetition schedules, quizzes, polysemy (rare word meanings) detection, word lookup, and writing output practice with MemOS integration for persistent tracking.
---

# 考研英语技能路由器 (Kaoyan English Router)

## 技能架构

```
kaoyan-english (路由器)
    ↓ 识别意图后调用
    ├─→ kaoyan-english-core     (核心协调层：MemOS集成、调度信号)
    ├─→ kaoyan-english-vocab    (词汇整理+查词+PDF提取)
    ├─→ kaoyan-english-review   (复习计划+统计追踪)
    ├─→ kaoyan-english-quiz     (单词测试)
    └─→ kaoyan-english-writing  (写作输出训练)
```

---

## 默认行为（重要！）

**当用户提供单词表文件路径时，默认执行完整的词汇处理流程：**

1. ✅ 按词族分类
2. ✅ 按考频分级（⭐至⭐⭐⭐）
3. ✅ 自动生成四类笔记：
   - 📊 词汇统计
   - 📰 真题语境文章
   - 📝 测试记录
   - ✍️ 写作输出

**禁止询问用户想要什么处理方式，直接执行上述完整流程！**

---

## 子技能速查

| 子技能 | 功能描述 | 触发关键词 |
|--------|----------|------------|
| **kaoyan-english-vocab** | 词汇整理+查词 | "整理单词"、"查单词"、"生成词汇表"、"PDF导出"、"真题语境文章" |
| **kaoyan-english-review** | 复习计划+统计 | "复习计划"、"间隔重复"、"学习统计"、"今日复习" |
| **kaoyan-english-quiz** | 单词测试 | "单词测试"、"词汇quiz"、"测试单词"、"僻义测试" |
| **kaoyan-english-writing** | 写作输出训练 | "写作替换"、"写作训练"、"高级词汇"、"汉译英" |
| **kaoyan-english-core** | 核心协调层 | "英语学习配置"、"英语状态"、"英语欠账检查" |

---

## 使用示例

### 示例1: 提供单词表路径（默认行为）
**用户输入**：`考研英语/英语单词/2026-3-26`
→ **自动执行完整词汇处理流程**（不询问）

### 示例2: 复习计划
**用户输入**："帮我生成今天的英语复习计划"
→ 路由到 `kaoyan-english-review`

### 示例3: 单词测试
**用户输入**："测试一下我最近学的单词"
→ 路由到 `kaoyan-english-quiz`

### 示例4: 写作训练
**用户输入**："我想练习写作词汇替换"
→ 路由到 `kaoyan-english-writing`

---

## 直接调用子技能

用户也可以直接调用子技能，跳过路由器：
- 使用 `kaoyan-english-vocab` 查询单词
- 使用 `kaoyan-english-review` 生成今日复习计划
- 使用 `kaoyan-english-quiz` 进行词义测试
- 使用 `kaoyan-english-writing` 练习写作替换

---

## 协同技能

| 技能 | 协同场景 |
|------|----------|
| kaoyan-plan | 提供每日计划时间分配，发送调度信号 |
| obsidian-markdown | 创建和管理Obsidian笔记 |
| pdf | 读取PDF单词导出 |

---

*最后更新: 2026-03-27*
