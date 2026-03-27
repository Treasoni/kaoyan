---
name: kaoyan-english-vocab
description: This skill handles vocabulary organization and word lookup for 考研英语 (Chinese graduate entrance English exam). Use it when users want to extract vocabulary from PDF exports (墨墨/百词斩), generate real exam context articles, detect polysemy (rare word meanings), look up word information, or organize vocabulary cards.
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

### ⚠️ 默认行为（重要）

**当用户提供单词表文件时，默认执行完整的词汇处理流程：**

1. ✅ **按词族分类**
2. ✅ **按考频分级**（⭐至⭐⭐⭐）
3. ✅ **自动生成四类笔记**：
   - 📊 词汇统计（Statistics-Day-XXX-YYYY-MM-DD.md）
   - 📰 真题语境文章（Context-Day-XXX-YYYY-MM-DD.md）
   - 📝 测试记录（Quiz-Day-XXX-YYYY-MM-DD.md）
   - ✍️ 写作输出（Writing-Day-XXX-YYYY-MM-DD.md）

**禁止询问用户想要什么处理方式，直接执行上述完整流程！**

---

## 📁 详细模块文档

| 模块 | 文件 | 内容 |
|------|------|------|
| 代码实现 | [code.md](code.md) | 核心函数实现 |
| 输出路径规范 | [docs/output-paths.md](docs/output-paths.md) | 四类笔记存放位置 |
| 编码规范 | [docs/encoding.md](docs/encoding.md) | 避免乱码 |
| 表格规范 | [docs/markdown-table.md](docs/markdown-table.md) | Markdown表格格式 |
| Day编号计算 | [docs/day-number.md](docs/day-number.md) | Day编号规则 |
| 熟词僻义库 | [data/polysemy-database.md](data/polysemy-database.md) | 僻义预警数据 |
| 每日词汇模板 | [templates/daily-vocabulary.md](templates/daily-vocabulary.md) | 每日词汇格式 |
| 真题语境模板 | [templates/context-card.md](templates/context-card.md) | 语境卡片格式 |
| 词汇卡片模板 | [templates/word-card.md](templates/word-card.md) | 完整卡片格式 |
| 整理版模板 | [templates/formatted-wordlist.md](templates/formatted-wordlist.md) | 单词表格式 |

---

## 触发条件

### 触发此技能当：

**词汇整理相关**：
- "整理考研英语单词" + 提供PDF/单词表
- "生成考研英语复习文章"
- "从PDF提取单词"
- "墨墨背单词导出"
- "百词斩导出"
- "真题语境文章"
- "外刊风格"
- "生成词汇表"
- "处理单词表" + 提供单词表文件
- "格式化单词"
- "分类单词"

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

### ⚠️ 执行顺序（重要！）

当用户提供单词表时，**必须按以下顺序执行**：

```
[用户提供单词表]
      ↓
[步骤0: 整理和格式化原始单词表] ← 必须首先执行！
      ↓
[步骤1: 检测熟词僻义]
      ↓
[步骤2: 生成四类学习笔记]
```

### 功能0: 整理和格式化单词表（必须步骤）⚠️

**输入**: 用户提供的原始单词表（可能是从PDF/图片转换，格式混乱）

**处理流程**:
1. **格式统一化**：统一标题格式、清理多余符号、修复截断释义
2. **添加记忆方法（必须！所有单词！）**：词根词缀法、联想记忆法、谐音记忆法等
3. **补充词组搭配**：每个单词至少2-3个常用搭配
4. **按词族分类**：将同源词归类
5. **按考研重点分类**：⭐⭐⭐ 高频词、⭐⭐ 中频词、⭐ 低频词
6. **僻义预警标记**：🔴 Critical / 🟡 Warning
7. **写作词汇标注**：标注可替代的简单词汇
8. **更新原始文件**：直接覆盖用户的原始单词表文件

> 📋 详细模板见 [templates/formatted-wordlist.md](templates/formatted-wordlist.md)

### 功能1: PDF词汇提取 + 语境文章

**输入**: 用户从单词APP（墨墨/百词斩等）导出的PDF

**处理流程**:
1. 读取PDF内容，提取单词列表
2. **整理和格式化单词表**（执行功能0）
3. 为每个单词获取：音标、词性、释义、词频
4. **检测熟词僻义**：识别考研中的僻义陷阱
5. **优先检索真题语境**：真题语境池 → 外刊同源 → AI生成
6. 将单词串联成真题风格的语境文章
7. 在文章中高亮目标词汇

**输出**:
- **整理后的单词表**：覆盖原始文件
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

## 真题语境检索策略

> 📁 详细实现见 [code.md](code.md) 的 `generate_context_article` 函数

### 检索优先级

1. **真题语境池** → 优先使用近5年真题
2. **外刊同源库** → The Economist, The Guardian
3. **AI生成** → 模拟真题风格（最后选项）

### 文章要求

- ✅ 必须包含用户提供的**所有目标单词**
- ✅ **译文位置**：紧接在原文之后，词汇解析表之前（便于对照阅读）
- ✅ 风格模拟考研真题阅读理解

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
> 📋 数据来源见 [data/polysemy-database.md](data/polysemy-database.md)

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
9. ✅ **记忆方法覆盖率100%**：每个单词都必须有记忆方法块
10. ✅ **记忆方法格式正确**：使用 `> 🧠 **记忆方法**` callout 格式

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
*版本: 1.2.0*
*最后更新: 2026-03-27（拆分文档结构）*
