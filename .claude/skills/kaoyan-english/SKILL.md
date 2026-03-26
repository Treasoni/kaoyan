---
name: kaoyan-english
description: This skill routes English vocabulary learning requests to specialized sub-skills for 考研英语 (Chinese graduate entrance English exam) preparation. It handles vocabulary organization from PDF exports, spaced repetition schedules, quizzes, polysemy (rare word meanings) detection, word lookup, and writing output practice with MemOS integration for persistent tracking.
version: 4.1.0
---

# 考研英语技能路由器 (Kaoyan English Router)

## 技能概述

本技能是考研英语学习的**路由入口**，负责识别用户意图并路由到对应的子技能：

```
kaoyan-english (路由器)
    ↓ 识别意图后调用
    ├─→ kaoyan-english-core     (核心协调层：MemOS集成、调度信号)
    ├─→ kaoyan-english-vocab    (词汇整理+查词+PDF提取)
    ├─→ kaoyan-english-review   (复习计划+统计追踪)
    ├─→ kaoyan-english-quiz     (单词测试)
    └─→ kaoyan-english-writing  (写作输出训练)
```

## v4.1.0 更新说明

**重要变更**：当用户提供单词表文件路径时，**默认执行完整的词汇处理流程**，不再询问用户！

完整流程包括：
1. ✅ 按词族分类
2. ✅ 按考频分级（⭐至⭐⭐⭐）
3. ✅ 自动生成四类笔记：
   - 📊 词汇统计（Statistics-Day-XXX）
   - 📰 真题语境文章（Context-Day-XXX）
   - 📝 测试记录（Quiz-Day-XXX）
   - ✍️ 写作输出（Writing-Day-XXX）

---

## 子技能速查

| 子技能 | 功能描述 | 触发关键词 |
|--------|----------|------------|
| **kaoyan-english-vocab** | 词汇整理+查词 | "整理单词"、"查单词"、"生成词汇表"、"PDF导出"、"真题语境文章"、"处理单词表"、"格式化单词"、"分类单词" |
| **kaoyan-english-review** | 复习计划+统计 | "复习计划"、"间隔重复"、"学习统计"、"今日复习"、"词汇统计" |
| **kaoyan-english-quiz** | 单词测试 | "单词测试"、"词汇quiz"、"测试单词"、"词义测试"、"僻义测试" |
| **kaoyan-english-writing** | 写作输出训练 | "写作替换"、"写作训练"、"高级词汇"、"汉译英"、"词义辨析" |
| **kaoyan-english-core** | 核心协调层 | "英语学习配置"、"英语状态"、"英语欠账检查"、"英语疲劳检查" |

---

## 路由逻辑

当用户请求涉及考研英语词汇学习时，本技能会：

1. **分析用户意图**：识别用户想要完成的具体任务
2. **选择子技能**：根据意图匹配最合适的子技能
3. **调用子技能**：将用户请求传递给对应的子技能处理
4. **返回结果**：将子技能的处理结果返回给用户

### ⚠️ 默认行为（重要）

**当用户提供单词表文件路径时，默认执行完整的词汇处理流程：**

1. ✅ 按词族分类
2. ✅ 按考频分级（⭐至⭐⭐⭐）
3. ✅ 自动生成四类笔记：
   - 📊 词汇统计（Statistics-Day-XXX）
   - 📰 真题语境文章（Context-Day-XXX）
   - 📝 测试记录（Quiz-Day-XXX）
   - ✍️ 写作输出（Writing-Day-XXX）

**禁止询问用户想要什么处理方式，直接执行上述完整流程！**

### 意图分类规则

```python
# 伪代码
def route_english_request(user_input):
    """路由英语学习请求"""

    # 0. 【最高优先级】检测文件路径 - 默认执行完整词汇处理流程
    if is_file_path(user_input) or is_directory_path(user_input):
        # 自动执行完整的词汇处理流程，不询问用户
        return execute_full_vocab_workflow(user_input)

    # 1. 词汇整理/查词相关 - 执行完整流程
    if any(keyword in user_input for keyword in [
        "整理单词", "查单词", "PDF导出", "真题语境文章",
        "墨墨背单词", "百词斩", "熟词僻义",
        "处理单词表", "格式化单词", "分类单词",
        "整理单词表", "单词表整理", "单词整理",
        "格式化单词表", "分类单词表"
    ]):
        return execute_full_vocab_workflow(user_input)  # 执行完整流程

    # 2. 复习计划/统计相关
    elif any(keyword in user_input for keyword in [
        "复习计划", "间隔重复", "学习统计", "今日复习",
        "词汇统计", "倒计时复习"
    ]):
        return invoke_skill("kaoyan-english-review", user_input)

    # 3. 测试相关
    elif any(keyword in user_input for keyword in [
        "单词测试", "词汇quiz", "测试单词", "词义测试",
        "僻义测试", "搭配测试"
    ]):
        return invoke_skill("kaoyan-english-quiz", user_input)

    # 4. 写作训练相关
    elif any(keyword in user_input for keyword in [
        "写作替换", "写作训练", "高级词汇", "汉译英",
        "词义辨析", "作文用词"
    ]):
        return invoke_skill("kaoyan-english-writing", user_input)

    # 5. 核心配置相关
    elif any(keyword in user_input for keyword in [
        "英语学习配置", "英语状态", "英语欠账检查",
        "英语疲劳检查", "英语进度"
    ]):
        return invoke_skill("kaoyan-english-core", user_input)

    # 6. 通用英语学习请求 - 默认执行完整流程
    elif "英语" in user_input or "English" in user_input or "单词" in user_input:
        # 默认执行完整词汇处理流程
        return execute_full_vocab_workflow(user_input)

    # 7. 默认：执行完整词汇处理流程（不再询问）
    else:
        return execute_full_vocab_workflow(user_input)


def execute_full_vocab_workflow(user_input):
    """执行完整的词汇处理流程"""

    # 步骤1: 整理和格式化单词表
    #   - 读取用户提供的单词表文件
    #   - 按词族分类
    #   - 按考频分级（⭐至⭐⭐⭐）
    #   - 添加记忆方法（词根词缀法）
    #   - 补充词组搭配
    #   - 标记僻义预警
    #   - 更新原始文件

    # 步骤2: 生成四类笔记
    #   - 📊 词汇统计（Statistics-Day-XXX-YYYY-MM-DD.md）
    #   - 📰 真题语境文章（Context-Day-XXX-YYYY-MM-DD.md）
    #   - 📝 测试记录（Quiz-Day-XXX-YYYY-MM-DD.md）
    #   - ✍️ 写作输出（Writing-Day-XXX-YYYY-MM-DD.md）

    # 步骤3: 更新学习进度
    #   - 更新 考研英语/📊 学习进度.md

    return "完整词汇处理流程执行完成"


def is_file_path(user_input):
    """检测是否为文件路径"""
    # 匹配模式：
    # - 考研英语/英语单词/2026-3-26
    # - 考研英语/英语单词/2026-3-26.md
    # - 包含 "/" 且看起来像路径
    return "/" in user_input or user_input.endswith(".md")


def is_directory_path(user_input):
    """检测是否为目录路径"""
    return "/" in user_input and not user_input.endswith(".md")
```

---

## 使用示例

### 示例1: 提供单词表路径（默认行为）

**用户输入**：`考研英语/英语单词/2026-3-26`

**执行流程**:
1. 检测到文件路径
2. **自动执行完整词汇处理流程**（不询问）
3. 生成5个文件：
   - 整理后的单词表
   - 词汇统计
   - 真题语境文章
   - 测试记录
   - 写作输出

### 示例2: 词汇整理

**用户输入**："我整理了一批考研单词，想生成复习文章"

**路由流程**:
1. 识别关键词："整理单词"、"复习文章"
2. **执行完整词汇处理流程**

### 示例3: 复习计划

**用户输入**："帮我生成今天的英语复习计划"

**路由流程**:
1. 识别关键词："复习计划"、"今天"
2. 匹配子技能：`kaoyan-english-review`
3. 调用子技能处理请求

### 示例4: 单词测试

**用户输入**："测试一下我最近学的单词"

**路由流程**:
1. 识别关键词："测试"、"单词"
2. 匹配子技能：`kaoyan-english-quiz`
3. 调用子技能处理请求

### 示例5: 写作训练

**用户输入**："我想练习写作词汇替换"

**路由流程**:
1. 识别关键词："写作"、"词汇替换"
2. 匹配子技能：`kaoyan-english-writing`
3. 调用子技能处理请求

---

## 直接调用子技能

用户也可以直接调用子技能，跳过路由器：

```markdown
# 直接调用示例
- 使用 kaoyan-english-vocab 查询单词 "address"
- 使用 kaoyan-english-review 生成今日复习计划
- 使用 kaoyan-english-quiz 进行词义测试
- 使用 kaoyan-english-writing 练习写作替换
- 使用 kaoyan-english-core 检查词汇欠账
```

---

## 技能集成

### 子技能依赖关系

```
kaoyan-english (路由器)
    ↓
    ├─→ kaoyan-english-core (MemOS集成，被其他技能调用)
    │        ↓
    │        ├─→ kaoyan-english-vocab (调用core保存词汇卡片)
    │        ├─→ kaoyan-english-review (调用core读取历史数据)
    │        ├─→ kaoyan-english-quiz (调用core记录测试结果)
    │        └─→ kaoyan-english-writing (调用core保存写作记录)
```

### 协同技能

| 技能 | 协同场景 |
|------|----------|
| kaoyan-plan | 提供每日计划时间分配，发送调度信号 |
| obsidian-markdown | 创建和管理Obsidian笔记 |
| pdf | 读取PDF单词导出 |
| docx | 生成Word文档导出 |

---

## 验证标准

1. ✅ 能够正确识别用户意图
2. ✅ 能够路由到正确的子技能
3. ✅ 子技能功能完整（不丢失原功能）
4. ✅ 用户使用体验不变
5. ✅ 支持直接调用子技能
6. ✅ **提供文件路径时，默认执行完整流程，不询问用户**

---

## 文件路径

### 子技能文件

- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-core/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-vocab/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-review/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-quiz/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-writing/skill.md`

---

*创建日期: 2026-02-26*
*最后更新: 2026-03-26 (v4.1.0 修改默认行为：提供文件路径时自动执行完整流程)*
*维护者: Claude Code + 用户协作*
