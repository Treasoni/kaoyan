---
name: kaoyan-english-vocab
description: This skill handles vocabulary organization and word lookup for 考研英语 (Chinese graduate entrance English exam). Use it when users want to extract vocabulary from PDF exports (墨墨/百词斩), generate real exam context articles, detect polysemy (rare word meanings), look up word information, or organize vocabulary cards.
version: 1.0.0
---

# 考研英语词汇整理技能 (Kaoyan English Vocab)

> 📁 详细代码实现见 [code.md](code.md)

## 技能概述

本技能专注于考研英语词汇的整理和查询，帮助用户：
1. **PDF词汇提取**：从单词APP（墨墨/百词斩等）导出的PDF中提取词汇
2. **词汇分类**：自动识别重点词汇、僻义词、一般词汇
3. **熟词僻义检测**：识别考研中的僻义陷阱并预警
4. **快速查词**：查询单词信息（含僻义预警）
5. **真题语境文章生成**：将目标词汇串联成真题风格的语境文章

**核心特色**：
- ⚠️ 僻义预警系统（Critical/Warning级别）
- 优先使用真题语境，非AI生成文章
- 自动生成结构化词汇卡片

---

## 触发条件

### 触发此技能当：

**词汇整理相关**：
- "整理考研英语单词" + 提供PDF
- "生成考研英语复习文章"
- "从PDF提取单词"
- "墨墨背单词导出"
- "百词斩导出"
- "真题语境文章"
- "外刊风格"
- "生成词汇表"

**查词相关**：
- "查单词"（在考研语境下）
- "查询单词"
- "word lookup" + 单词
- 单词 + "什么意思"（考研语境）

**僻义相关**：
- "熟词僻义"
- "僻义词"
- "陷阱词"
- "考研陷阱"
- "一词多义"

### 不触发此技能当：
- 生成复习计划 → 使用 kaoyan-english-review
- 单词测试 → 使用 kaoyan-english-quiz
- 写作训练 → 使用 kaoyan-english-writing

---

## 核心功能

### 功能1: PDF词汇提取 + 语境文章

**输入**: 用户从单词APP（墨墨/百词斩等）导出的PDF

**处理流程**:
1. 读取PDF内容，提取单词列表
2. 为每个单词获取：音标、词性、释义、词频
3. **检测熟词僻义**：识别考研中的僻义陷阱
4. **优先检索真题语境**：真题语境池 → 外刊同源 → AI生成
5. 将单词串联成真题风格的语境文章
6. 在文章中高亮目标词汇

**输出**:
- Obsidian笔记：每日词汇记录（含僻义预警）
- 真题语境文章：包含目标词汇的连贯文章

### 功能2: 快速查词 + 僻义预警

**输入**: 单个单词或短语

**处理流程**:
1. 查询单词基本信息（音标、词性、释义）
2. **检测熟词僻义**：显示僻义预警级别
3. 提供真题例句（含僻义用法）
4. 显示常用搭配
5. 展示同义词/反义词/词族

**输出**: 紧凑的单词卡片（含⚠️僻义预警）

---

## 熟词僻义库

### Critical级别（高频陷阱）

| 单词 | 常见义 | **考研僻义** | 出现频率 |
|------|--------|-------------|----------|
| address | 地址 | **vt. 处理，解决** | 80% |
| school | 学校 | **n. 流派，学派** | 70% |
| novel | 新颖的 | **n. 长篇小说** | 65% |
| fine | 好的 | **n./v. 罚款** | 60% |
| reason | 原因 | **v. 推理，推论** | 55% |
| discipline | 纪律 | **n. 学科** | 50% |
| consume | 消费 | **vt. 毁灭，烧毁** | 40% |
| draft | 草稿 | **n. 征兵** | 35% |
| compound | 复合的 | **v. 加剧，恶化** | 30% |

### Warning级别（中等陷阱）

| 单词 | 常见义 | 考研僻义 | 出现频率 |
|------|--------|----------|----------|
| spring | 春天 | **v. 突然出现，涌现** | 40% |
| table | 桌子 | **v. 搁置，暂缓讨论** | 35% |
| book | 书 | **v. 预订** | 30% |

---

## 真题语境检索策略

> 📁 详细实现见 [code.md](code.md) 的 `generate_context_article` 函数

### 检索优先级

1. **真题语境池** → 优先使用近5年真题
2. **外刊同源库** → The Economist, The Guardian
3. **AI生成** → 模拟真题风格（最后选项）

### 文章要求

- ✅ 必须包含用户提供的**所有目标单词**
- ✅ 文章译文放在文章**下面**
- ✅ 风格模拟考研真题阅读理解

---

## 词汇卡片格式

### 完整版格式

```markdown
---
# 基础信息
word: "address"
pronunciation: "/əˈdres/"
part_of_speech: "verb/noun"
difficulty: "important"
frequency: 5
first_seen: "2025-01-15"

# 僻义预警
polysemy_alert: true
warning_level: "critical"
exam_frequency: "80%"
rare_meanings:
  - meaning: "处理；解决；着手处理"
    part_of_speech: "vt."
    common_collocations: ["address the problem", "address an issue", "address concerns"]
common_meanings:
  - meaning: "地址；称呼"
    part_of_speech: "n./vt."

# 真题语境
real_exam_contexts:
  - year: 2022
    paper: "英语一"
    section: "完形填空"
    sentence: "The committee failed to **address** the concerns raised by the public."
    sentence_translation: "委员会未能处理公众提出的关切。"
    other_core_words: ["committee", "concern", "raise"]

# 标签与分类
tags: ["动词", "高频", "僻义critical", "写作必备"]
exam_years: [2018, 2020, 2022]
---

# address

## 基本信息
**音标**: /əˈdres/
**词性**: vt./n.
**难度**: ⭐⭐⭐⭐⭐

## ⚠️ 僻义预警 [critical]

> [!danger] 陷阱提示
> 此词在考研中 **80%** 考查僻义"处理"，而非常见义"地址"

**考研常考僻义**: vt. 处理；解决；着手处理

### 真题例句
> [!example] 2022年真题 完形填空
> The committee failed to **address** the concerns raised by the public.

> [!example] 2020年真题 阅读理解
> We must **address** the root causes of inequality.

### 常用搭配
- address the problem - 解决问题
- address an issue - 处理议题
- address concerns - 处理关切

## 常见义（对比）
n. 地址； vt. 称呼

⚠️ 易错点：在阅读中遇到此词时，首先考虑"处理"义

## 写作应用

### 高级替换
- **初级**: solve/deal with the problem
- **高级**: **address** the problem

### 写作例句
> The government must **address** the problem of inequality.
> (政府必须处理不平等问题。)

## 词族
- addressee (n.) - 收件人
- addresser (n.) - 发言人
```

---

## 文件组织结构

```
考研英语/
├── 📚 重点词汇库/                # 单独文件
│   ├── exemplify.md
│   ├── address.md               # 带僻义预警
│   └── ...
│
├── 📖 一般词汇库/                # 汇总存储
│   ├── A组词汇.md
│   └── ...
│
├── 📝 每日词汇/
│   ├── Day-001-2025-01-15.md
│   └── ...
│
├── 📚 真题语境池/                # 真题例句库
│   ├── 英语一/
│   │   ├── 阅读理解/
│   │   ├── 完形填空/
│   │   └── 翻译/
│   └── 英语二/
│       └── ...
│
├── 📰 外刊同源库/                # 外刊例句库
│   ├── The Economist/
│   └── The Guardian/
│
└── ⚠️ 熟词僻义库/                # 僻义词索引
    ├── critical级别.md
    ├── warning级别.md
    └── 完整列表.md
```

---

## 模板

### 模板1: 每日词汇

```markdown
# 每日词汇 - Day {day_number}

**日期**: {date}
**来源**: 墨墨背单词导出
**当前阶段**: {基础期/强化期/冲刺期/极限冲刺期}
**距离考试**: {days}天

---

## 重点词汇

| 单词 | 音标 | 词性 | 释义 | ⚠️僻义 | 💡记忆提示 | 📝常见搭配 |
|------|------|------|------|--------|----------|------------|
| exemplify | /ɪɡˈzemplɪfaɪ/ | v. | 举例说明 | | 词根: exempl(例子)+ify动词化 | exemplify the point |
| address | /əˈdres/ | vt./n. | 处理；地址 | [critical] | 搭配记忆: address the problem | address the issue, address concerns |

---

## ⚠️ 僻义预警

### address [critical]
- 常见义：地址
- **考研僻义（80%）**: 处理、解决
- 搭配：address the problem, address an issue

---

## 真题语境文章

{article_including_all_target_words}

> ⚠️ **词汇覆盖检查**: 本文已包含所有 {total_count} 个目标单词

---

## 📖 文章译文

{chinese_translation}

---

## 📖 阅读理解练习

### 模板2: 真题语境卡片

```markdown
---
context_source: "真题"
source_year: 2023
source_paper: "英语一"
source_type: "阅读理解"
source_section: "Text 3"
source_topic: "社会政策"
difficulty_level: "hard"
cefr_level: "C1"
word_count: 22
core_word_density: "5/22 (23%)"
---

## 真题语境: exemplify

> [!quote] 2023年英语一 阅读理解 Text 3
> The case of California's energy policy **exemplifies** how well-intentioned regulations can have unintended consequences when market dynamics are overlooked.

### 句式分析
- **结构**: 让步状语从句 + how引导宾语从句
- **外刊风格**: 经济学人式论证逻辑（例子→观点→深层分析）
- **词汇密度**: 5个考研核心词 / 22词 (23%)

### 同句其他核心词
- well-intentioned: 善意的
- regulation: 规章制度
- unintended: 意外的
- consequence: 后果
- overlook: 忽视

> ⚠️ **时效提醒**：此语境来自2023年真题，保证时效性和权威性
```

---

## 工作流程

```
[用户提供PDF]
      ↓
[提取单词列表]
      ↓
[检测熟词僻义]
      ↓
[识别重点词汇]
      ↓
┌─────┴─────┐
│           │
[检索真题语境] [生成词汇卡片]
│           │
└─────┬─────┘
      ↓
[生成语境文章]
      ↓
[保存到Obsidian]
```

---

## 熟词僻义检测

> 📁 详细实现见 [code.md](code.md) 的 `detect_polysemy` 函数

### 检测逻辑

1. 检索考研大纲词表
2. 对比大纲释义与常见释义
3. 计算语义重叠度
4. 重叠度 < 50% → 触发僻义预警

### 预警级别

| 级别 | 重叠度 | 说明 |
|------|--------|------|
| ⚠️ Critical | < 30% | 高频陷阱词，必须重点记忆 |
| ⚡ Warning | 30-50% | 中等陷阱词，需要留意 |

---

## 验证标准

1. ✅ 能够从PDF中提取单词列表
2. ✅ 能够识别并分类重点词汇、僻义词和一般词汇
3. ✅ **能够优先使用真题语境而非AI生成文章**
4. ✅ **能够正确检测和预警熟词僻义**
5. ✅ 能够快速查询单词信息（含僻义预警）
6. ✅ 能够生成结构化词汇卡片
7. ✅ 警告格式使用⚠️图标
8. ✅ 例题格式使用[!example] callout

---

## 限制条件

- 需要用户提供PDF文件或单词列表
- 查词功能依赖本地词汇库或在线词典
- 真题语境依赖于预建的真题例句库

---

## 技能集成

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-english-core | 保存词汇卡片到MemOS |
| obsidian-markdown | 创建词汇卡片笔记 |
| pdf | 读取PDF内容 |
| docx | 导出Word文档 |

### 被调用场景

| 调用者 | 场景 |
|--------|------|
| kaoyan-english-review | 获取单词信息生成复习计划 |
| kaoyan-english-quiz | 获取单词信息生成测试题 |
| kaoyan-english-writing | 获取单词信息用于写作训练 |

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
