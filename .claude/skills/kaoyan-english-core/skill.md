---
name: kaoyan-english-core
description: This skill manages the core infrastructure for 考研英语 (Chinese graduate entrance English exam) vocabulary learning, including MemOS integration for persistent storage, dispatch signal processing, memory compression mode, unified error tracking, and dynamic phase-based vocabulary targeting.
version: 1.0.0
---

# 考研英语核心协调技能 (Kaoyan English Core)

## 技能概述

本技能是考研英语词汇学习的核心协调层，负责：
1. **MemOS集成管理**：用户画像、词汇卡片持久化、复习历史记录
2. **调度信号处理**：接收并处理来自kaoyan-plan的调度信号
3. **记忆压缩模式**：当其他科目欠账时激活英语时间压缩
4. **统一错误模型**：英语错误记录的学科标签管理
5. **动态权重响应**：根据考试倒计时阶段调整词汇学习目标

**设计原则**：
- 其他英语技能通过本技能访问MemOS
- 当MemOS不可用时自动降级
- 提供统一的错误记录和追踪接口

---

## 触发条件

### 触发此技能当：

**用户画像相关**：
- "英语学习配置"
- "更新英语画像"
- "英语水平设置"
- "考研英语配置"

**状态检查相关**：
- "英语状态"
- "英语进度"
- "英语欠账检查"
- "英语疲劳检查"
- "词汇欠账"
- "待复习词汇"

**调度信号相关**：
- "英语调度信号"
- "英语压缩模式"
- "英语复习模式"

### 不触发此技能当：
- 词汇整理/查词 → 使用 kaoyan-english-vocab
- 生成复习计划 → 使用 kaoyan-english-review
- 单词测试 → 使用 kaoyan-english-quiz
- 写作训练 → 使用 kaoyan-english-writing

---

## MemOS集成

### 核心原则
- **增强功能**: MemOS集成是可选增强，不影响基础功能使用
- **优雅降级**: 当MemOS不可用时，自动降级为无状态模式
- **数据持久化**: 词汇学习记录、用户画像、复习历史均持久化存储

### MemOS功能特性
1. **用户画像追踪**: 记录英语水平、考试信息、学习偏好
2. **词汇卡片持久化**: SM-2算法状态永久保存
3. **复习历史记录**: 完整的复习会话历史
4. **测试结果追踪**: 测试成绩和错误分析
5. **词汇疲劳追踪**: 防止学习倦怠的智能提醒
6. **欠账熔断机制**: 超过200个待复习词时自动触发复习模式
7. **画像刷新机制**: 30天未更新时提示确认学习配置

### 降级行为
当MemOS不可用时：
- ✅ 基础功能正常工作
- ❌ 不保存学习历史到持久存储
- ❌ 不进行跨设备同步
- ❌ 不启用智能追踪（疲劳、欠账熔断等）

---

## 数据模型

### 用户画像 (User Profile)

```yaml
user_profile:
  user_id: string
  conversation_id: string
  created_at: datetime
  updated_at: datetime

  profile:
    exam_date: date
    exam_type: enum (english_1 | english_2)
    target_score: int
    current_level: enum (basic | intermediate | advanced)

  vocabulary_base:
    total_words: int
    mastered_count: int
    reviewing_count: int
    new_count: int

  preferences:
    daily_new_word_target: int (default 50)
    review_focus: enum (balanced | polysemy_priority | writing_priority)
    learning_style: enum (context_first | rote_first)
    polysemy_sensitivity: enum (high | medium | low)

  mental_history:
    - date: date
      status: enum (energized | normal | tired | burned_out)
      vocabulary_fatigue: float (0.0-1.0)
      trigger: string

  refresh_config:
    last_refreshed: date
    auto_refresh_interval: int
    pending_refresh: boolean
```

### 复习记录 (Review Record)

```yaml
review_record:
  record_id: string
  user_id: string
  date: date
  created_at: datetime

  session_info:
    words_reviewed: int
    new_words: int
    duration_minutes: int

  results:
    correct_count: int
    incorrect_count: int
    polysemy_errors: int

  phase_context:
    current_phase: string
    days_to_exam: int
```

### 词汇卡片 (Word Card)

```yaml
word_card:
  word: string
  user_id: string
  created_at: datetime
  updated_at: datetime

  # SM-2基础字段
  ease_factor: float (default 2.5)
  interval: int
  review_count: int
  next_review: date
  correct_count: int
  incorrect_count: int
  forgetting_rate: float

  # 考研适配字段
  exam_date: date
  current_phase: string
  phase_factor: float
  days_to_exam: int
  adjusted_interval: int

  # 僻义预警字段
  polysemy_alert: bool
  warning_level: string (critical | warning | attention)
  exam_frequency: string
  rare_meanings: array
  common_meanings: array
```

---

## 核心函数

### 函数1: load_user_context_from_memory

从MemOS加载用户上下文，失败时返回None触发降级。

```python
def load_user_context_from_memory(user_input):
    """从MemOS加载用户上下文

    Returns:
        dict: 用户上下文信息，包含用户画像、词汇库等
        None: MemOS不可用时触发降级
    """
    try:
        results = search_memory(
            query=f"#user_profile #user_{user_input.get('user_id')}",
            top_k=10
        )
        return parse_memory_to_english_context(results)
    except Exception as e:
        log_warning(f"MemOS unavailable: {e}")
        return None


def parse_memory_to_english_context(memory_results):
    """将MemOS结果解析为英语学习上下文"""
    if not memory_results:
        return create_default_user_context()

    context = {
        "user_profile": extract_user_profile(memory_results),
        "vocabulary_cards": extract_word_cards(memory_results),
        "review_history": extract_review_records(memory_results),
        "mental_history": extract_mental_state(memory_results)
    }

    return context
```

### 函数2: save_word_card_to_memory

保存词汇卡片到MemOS，含降级处理。

```python
def save_word_card_to_memory(word_card, user_id):
    """保存词汇卡片到MemOS

    Args:
        word_card: 词汇卡片对象
        user_id: 用户ID
    """
    try:
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "word_card",
                    "data": word_card.to_dict()
                },
                "tags": [
                    "#word_card",
                    f"#word_{word_card.word}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )
        log_info(f"Saved word card: {word_card.word}")
    except Exception as e:
        log_warning(f"Failed to save word card {word_card.word}: {e}")
        # 降级：不影响主流程，仅不保存
```

### 函数3: record_review_session

记录复习会话到MemOS，使用upsert逻辑避免冗余。

```python
def record_review_session(user_id, session_data):
    """记录复习会话到MemOS（upsert逻辑）

    Args:
        user_id: 用户ID
        session_data: 复习会话数据
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")

        # 先查找今日已有记录
        today_session = search_memory(
            query=f"#review_session_current #user_{user_id} #date_{today}",
            top_k=1
        )

        if today_session:
            # 标记旧版本为历史
            add_message(
                messages=[{
                    "role": "assistant",
                    "content": {
                        "type": "review_session",
                        "version": today_session[0].get("version"),
                        "status": "superseded",
                        "data": today_session[0].get("data")
                    },
                    "tags": [
                        "#review_session_history",
                        f"#date_{today}",
                        f"#user_{user_id}"
                    ]
                }],
                user_id=user_id
            )

        # 保存新会话为当前版本
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "review_session",
                    "version": f"v{datetime.now().strftime('%H%M')}",
                    "status": "current",
                    "data": session_data
                },
                "tags": [
                    "#review_session_current",
                    f"#date_{today}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )

        log_info(f"Recorded review session for {today}")
    except Exception as e:
        log_warning(f"Failed to record session: {e}")
```

### 函数4: check_context_freshness_english

检查用户画像是否需要刷新。

```python
def check_context_freshness_english(user_context, current_date):
    """检查英语学习画像是否需要刷新

    Args:
        user_context: 用户上下文
        current_date: 当前日期

    Returns:
        dict: 包含needs_refresh, reason, questions等信息
        None: 不需要刷新
    """
    profile = user_context.get("user_profile")
    if not profile:
        return None

    updated_at = profile.get("updated_at")
    days_since_update = (current_date - updated_at).days

    # 超过30天自动触发刷新询问
    if days_since_update > 30:
        return {
            "needs_refresh": True,
            "reason": f"画像已{days_since_update}天未更新",
            "questions": [
                "你的英语水平有变化吗？(基础/中级/高级)",
                f"每日新词目标需要调整吗？(当前: {profile.get('daily_new_word_target', 50)})",
                "复习重点需要调整吗？(均衡/僻义优先/写作优先)",
                f"僻义敏感度需要调整吗？(当前: {profile.get('polysemy_sensitivity', 'medium')})"
            ]
        }

    return {"needs_refresh": False}
```

### 函数5: check_vocabulary_debt_with_memory

检查词汇欠账，含熔断机制。

```python
def check_vocabulary_debt_with_memory(user_context):
    """检查词汇欠账（含熔断机制）

    Args:
        user_context: 用户上下文

    Returns:
        dict: 欠账状态和处理策略
    """
    # 计算逾期未复习的词汇数量
    overdue_words = calculate_overdue_words(user_context)
    DEBT_LIMIT = 200  # 200个词熔断阈值

    if overdue_words > DEBT_LIMIT:
        return {
            "type": "vocabulary_emergency",
            "overdue_count": overdue_words,
            "strategy": "recovery_only",
            "message": f"⚠️ 待复习词汇已达{overdue_words}个，超过安全阈值",
            "suggestion": "暂停新词学习，专注复习",
            "recovery_plan": generate_vocabulary_recovery_plan(overdue_words)
        }

    return {"type": "normal", "overdue_count": overdue_words}


def calculate_overdue_words(user_context):
    """计算逾期未复习的词汇数量"""
    vocabulary_cards = user_context.get("vocabulary_cards", [])
    today = date.today()

    overdue_count = 0
    for card in vocabulary_cards:
        next_review = card.get("next_review")
        if next_review and next_review < today:
            overdue_count += 1

    return overdue_count
```

### 函数6: check_vocabulary_fatigue_intervention

检查词汇学习疲劳，提供干预建议。

```python
def check_vocabulary_fatigue_intervention(user_context):
    """检查是否需要词汇疲劳干预

    Args:
        user_context: 用户上下文

    Returns:
        dict: 干预方案
        None: 无需干预
    """
    mental_history = user_context.get("mental_history", [])

    if len(mental_history) < 3:
        return None

    recent_days = mental_history[-3:]
    tired_count = sum(
        1 for d in recent_days
        if d.get("vocabulary_fatigue", 0) > 0.6
    )

    if tired_count >= 3:
        avg_fatigue = sum(
            d.get("vocabulary_fatigue", 0.5) for d in recent_days
        ) / len(recent_days)

        return {
            "intervention_needed": True,
            "mode": "vocabulary_relief",
            "avg_fatigue": avg_fatigue,
            "actions": [
                "减少新词量50%",
                "增加真题语境阅读",
                "暂停僻义词训练",
                "增加写作应用练习"
            ]
        }

    return None
```

---

## 调度信号处理

### 检查调度信号

从kaoyan-plan接收调度信号并执行相应动作。

```python
def check_dispatch_signals(user_id):
    """检查来自kaoyan-plan的调度信号"""
    try:
        signals = search_memory(
            query=f"#dispatch_signal #target_kaoyan-english #user_{user_id}",
            top_k=5
        )

        pending = []
        for signal in signals:
            if not signal.get("processed"):
                pending.append(signal)

        return pending
    except Exception as e:
        log_warning(f"Failed to check dispatch signals: {e}")
        return []


def process_dispatch_signal(signal):
    """处理调度信号"""
    action = signal.get("action")
    context = signal.get("context", {})

    if action == "vocabulary_review_mode":
        mode = context.get("mode", "light")
        duration = context.get("duration", "30min")
        return {
            "mode": "light_review",
            "duration": duration,
            "focus": "polysemy_words",
            "instructions": f"进入轻量词汇复习模式（{duration}），仅复习僻义词"
        }

    elif action == "memory_compression_mode":
        return activate_memory_compression_mode(context)

    elif action == "polysemy_focus":
        count = context.get("count", 20)
        return {
            "mode": "polysemy_focus",
            "word_count": count,
            "instructions": f"进入僻义词专项训练模式，复习{count}个僻义词"
        }

    elif action == "weekly_error_analysis":
        return {
            "mode": "weekly_review",
            "aggregate": context.get("aggregate", True)
        }

    return None
```

### 支持的调度动作

| 动作名 | 说明 | 上下文参数 |
|--------|------|------------|
| `vocabulary_review_mode` | 轻量词汇复习 | `{mode, duration}` |
| `memory_compression_mode` | 记忆压缩模式 | `{compress_hours, transfer_to}` |
| `polysemy_focus` | 僻义词专项 | `{focus, count}` |
| `weekly_error_analysis` | 周日错误分析 | `{aggregate}` |

---

## 记忆压缩模式

当kaoyan-plan检测到其他科目欠账时，可触发英语记忆压缩模式。

```python
def activate_memory_compression_mode(context):
    """激活记忆压缩模式

    Args:
        context: 压缩上下文，包含compress_hours, transfer_to等

    Returns:
        压缩后的学习计划
    """
    compress_hours = context.get("compress_hours", 1)
    transfer_to = context.get("transfer_to", "math")

    return {
        "mode": "memory_compression",
        "original_hours": get_planned_english_hours(),
        "compressed_hours": compress_hours,
        "transfer_to": transfer_to,
        "strategy": {
            "reduce_new_words": True,           # 减少新词量
            "focus_polysemy_only": True,        # 只复习僻义词
            "skip_context_article": True,       # 跳过语境文章生成
            "use_quick_review": True            # 使用快速复习模式
        },
        "message": f"⚠️ 英语时间压缩{compress_hours}小时，转移至{transfer_to}"
    }
```

### 压缩模式下的调整

| 功能 | 正常模式 | 压缩模式 |
|------|----------|----------|
| 每日新词 | 50个 | 20个 |
| 复习重点 | 均衡 | 仅僻义词+高频词 |
| 语境文章 | 生成 | 跳过 |
| 测试 | 完整 | 仅快速测试 |
| 写作训练 | 包含 | 跳过 |

---

## 动态权重响应

根据考试倒计时阶段自动调整词汇学习策略。

```python
def get_phase_vocabulary_target(days_to_exam):
    """根据阶段获取词汇学习目标"""

    if days_to_exam > 300:        # 基础期
        return {
            "daily_new_words": 50,
            "review_ratio": 0.3,
            "focus": "词汇积累",
            "polysemy_weight": 1.0
        }

    elif days_to_exam > 180:      # 强化期
        return {
            "daily_new_words": 40,
            "review_ratio": 0.5,
            "focus": "僻义词+真题语境",
            "polysemy_weight": 1.2
        }

    elif days_to_exam > 90:       # 十月强化期
        return {
            "daily_new_words": 30,
            "review_ratio": 0.6,
            "focus": "僻义词强化",
            "polysemy_weight": 1.5
        }

    elif days_to_exam > 30:       # 冲刺期
        return {
            "daily_new_words": 10,
            "review_ratio": 0.9,
            "focus": "高频词+僻义词",
            "polysemy_weight": 2.0
        }

    else:                         # 极限冲刺
        return {
            "daily_new_words": 0,
            "review_ratio": 1.0,
            "focus": "全部复习",
            "polysemy_weight": 2.0
        }
```

### 阶段策略表

| 阶段 | 天数 | 每日新词 | 复习比例 | 僻义权重 |
|------|------|----------|----------|----------|
| 基础期 | >300 | 50 | 30% | 1.0x |
| 强化期 | 180-300 | 40 | 50% | 1.2x |
| 十月强化期 | 90-180 | 30 | 60% | 1.5x |
| 冲刺期 | 30-90 | 10 | 90% | 2.0x |
| 极限冲刺 | <30 | 0 | 100% | 2.0x |

---

## 统一错误模型

### 学科标签

所有错误记录添加学科标签以支持跨技能聚合。

```python
def save_unified_english_mistake(mistake_data, user_id):
    """保存英语错误记录（统一格式）"""
    mistake_data["subject"] = "english"

    # 英语专用错误类型
    if mistake_data.get("type") == "polysemy_error":
        mistake_data["tags"].append("#polysemy_critical")

    try:
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "unified_mistake_record",
                    "data": mistake_data
                },
                "tags": [
                    "#mistake_record",
                    "#subject_english",
                    f"#word_{mistake_data.get('word', '')}",
                    f"#mistake_type_{mistake_data.get('type', 'unknown')}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to save mistake: {e}")
```

### 英语专用错误类型

| 错误类型 | 说明 | 标签 |
|----------|------|------|
| `polysemy_error` | 多义词错误 | `#polysemy_critical` |
| `collocation_error` | 搭配错误 | `#collocation` |
| `condition_omission` | 条件遗漏 | `#condition` |
| `concept_confusion` | 概念混淆 | `#concept` |

---

## MemOS标签系统

| 标签 | 用途 | 唯一性 |
|------|------|--------|
| `#user_profile` | 用户画像 | 每用户1条 |
| `#word_card` | 词汇卡片 | 每词每用户1条 |
| `#word_{word}` | 单词索引 | 可多条（不同用户） |
| `#review_session_current` | 今日当前复习会话 | 每用户每日1条 |
| `#review_session_history` | 历史复习会话归档 | 多条 |
| `#date_{YYYY-MM-DD}` | 日期索引 | 多条 |
| `#test_result` | 测试记录 | 多条 |
| `#dispatch_signal` | 调度信号 | 多条 |
| `#mistake_record` | 错误记录 | 多条 |
| `#subject_english` | 英语学科标签 | 多条 |

---

## 验证标准

1. ✅ 能够从MemOS加载用户上下文
2. ✅ 能够保存词汇卡片到MemOS
3. ✅ 能够记录复习会话（含upsert逻辑）
4. ✅ 能够检查用户画像新鲜度
5. ✅ 能够检查词汇欠账并触发熔断
6. ✅ 能够检测词汇疲劳并建议干预
7. ✅ 能够接收和处理调度信号
8. ✅ 能够激活记忆压缩模式
9. ✅ 能够根据阶段调整词汇目标
10. ✅ MemOS不可用时优雅降级
11. ✅ 统一错误模型学科标签正确

---

## 限制条件

- MemOS集成是可选的，不可用时不影响基础功能
- 调度信号依赖kaoyan-plan发送
- 记忆压缩模式需要kaoyan-plan触发

---

## 技能集成

### 被调用的技能

| 技能 | 调用场景 |
|------|----------|
| kaoyan-english-vocab | 保存词汇卡片 |
| kaoyan-english-review | 读取历史数据、保存复习记录 |
| kaoyan-english-quiz | 记录测试结果 |
| kaoyan-english-writing | 保存写作记录 |

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-plan | 发送调度信号 |

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
