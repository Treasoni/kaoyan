# kaoyan-plan 核心算法模块

本文档包含 kaoyan-plan 技能的所有核心算法实现。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 目录

1. [主规划算法 v3.0 (MemOS集成版)](#主规划算法v30-memos集成版)
2. [主规划算法 v2.1 (降级兼容版)](#主规划算法v21-降级兼容版)
3. [主规划算法 (自适应版)](#主规划算法自适应版)
4. [辅助函数](#辅助函数)
   - [疲劳度计算](#疲劳度计算)
   - [时段偏好](#时段偏好)
   - [欠账检测](#欠账检测)
   - [画像刷新检查](#画像刷新检查)
   - [心理干预检查](#心理干预检查)

---

## 主规划算法（v3.0 MemOS集成版）

```python
def generate_daily_plan_v3(user_input, mode="minimal", previous_plan=None):
    """
    根据用户输入模式生成计划（含MemOS记忆集成）

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划
    """

    # 1. MemOS: 读取用户上下文 (可降级)
    user_context = safe_load_context(user_input)

    # 1.5 v3.1: 检查画像新鲜度 (context_refresh机制)
    profile_refresh = check_context_freshness(user_context, datetime.now())
    if profile_refresh and profile_refresh.get("needs_refresh"):
        # 返回画像刷新询问，等待用户确认后再继续
        return generate_profile_refresh_question(profile_refresh)

    # 1.6 v3.1: 检查心理状态是否需要干预
    mental_intervention = check_mental_health_intervention(user_context)
    if mental_intervention and mental_intervention.get("intervention_needed"):
        # 标记为心理调节模式，后续生成计划时应用
        user_input["mental_mode"] = mental_intervention.get("mode")

    # 2. 检查任务欠账（v3.1增强: 含熔断机制）
    debt_result = check_task_debt_with_memory(previous_plan, user_input, user_context)
    if debt_result:
        # v3.1: 检查是否触发熔断
        if debt_result.get("type") == "debt_emergency":
            return generate_emergency_recovery_plan(debt_result)
        return generate_debt_handling_plan(user_input, debt_result.get("tasks"))

    # 3. 检查周日复盘（增强: 从MemOS读取本周数据）
    if is_sunday(today):
        return generate_sunday_review_plan_with_memory(user_input, user_context)

    # 4. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input, user_context)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input, user_context)
    else:
        user_data = merge_user_input_with_memory(user_input, user_context)

    # 5. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 6. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 7. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_input.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 8. 分配时段到科目（含最小块时长检查）
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue,
        min_block_check=True
    )

    # 9. MemOS: 保存计划 (可降级)
    safe_save_plan(plan, user_input, mode)

    return plan
```

### v3.0 辅助函数

```python
def safe_load_context(user_input):
    """从MemOS加载用户上下文，失败时返回None触发降级"""
    try:
        results = search_memory(
            conversation_id=user_input.get("conversation_id"),
            user_id=user_input.get("user_id"),
            query=f"用户画像配置 学习进度记录",
            top_k=10
        )
        return parse_memory_results_to_context(results)
    except Exception as e:
        log_warning(f"MemOS unavailable, using defaults: {e}")
        return None


def safe_save_plan(plan, user_input, mode):
    """保存生成的计划（v3.1增强: upsert with tag逻辑）"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        user_id = user_input.get("user_id")

        # v3.1: 先尝试查找今日已有计划
        today_plan = search_memory(
            query=f"#daily_plan_current {user_id} {today}",
            top_k=1
        )

        if today_plan:
            # 更新: 标记旧版本为历史，保存新版本为当前
            old_plan = today_plan[0]
            add_message(
                messages=[{
                    "role": "assistant",
                    "content": {
                        "type": "daily_plan",
                        "version": old_plan.get("version", "v1"),
                        "status": "superseded",
                        "data": old_plan.get("data"),
                        "superseded_at": datetime.now().isoformat()
                    },
                    "tags": ["#daily_plan_history", f"#date_{today}"]
                }],
                user_id=user_id
            )

        # 保存新计划为当前版本
        add_message(
            conversation_id=user_input.get("conversation_id"),
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "daily_plan",
                    "mode": mode,
                    "version": f"v{datetime.now().strftime('%H%M')}",
                    "status": "current",
                    "data": plan.to_dict(),
                    "timestamp": datetime.now().isoformat()
                },
                "tags": ["#daily_plan_current", f"#date_{today}"]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to save plan to memory: {e}")


def check_task_debt_with_memory(previous_plan, user_input, user_context):
    """检查任务欠账（增强版：从MemOS读取昨日计划）"""
    # 如果提供了previous_plan参数，直接使用
    if previous_plan:
        return check_task_debt(previous_plan, user_input.get("completed_tasks"))

    # 否则尝试从MemOS读取昨日计划
    if user_context:
        yesterday_plan = user_context.get("yesterday_plan")
        if yesterday_plan:
            return check_task_debt(yesterday_plan, user_input.get("completed_tasks"))

    return []


def generate_sunday_review_plan_with_memory(user_input, user_context):
    """生成周日复盘计划（增强版：从MemOS读取本周数据）"""
    weekly_stats = None
    if user_context:
        weekly_stats = user_context.get("weekly_progress")

    return {
        "type": "sunday_review",
        "date": today,
        "weekly_stats": weekly_stats,
        "tasks": [
            {"time": "19:00-19:30", "task": "本周完成度统计", "required": True},
            {"time": "19:30-20:00", "task": "数学错题重做", "required": True},
            {"time": "20:00-20:30", "task": "英语错题重做", "required": True},
            {"time": "20:30-21:00", "task": "专业课错题重做", "required": True},
            {"time": "21:00-21:30", "task": "政治错题重做", "required": True},
            {"time": "21:30-22:00", "task": "进度对齐检查", "required": True},
            {"time": "22:00-23:00", "task": "下周计划调整", "required": True}
        ]
    }


def record_task_completion(user_id, completed_tasks, planned_tasks):
    """记录任务完成情况到MemOS"""
    try:
        stats = calculate_completion_stats(completed_tasks, planned_tasks)
        add_message(
            conversation_id=user_id,
            messages=[{
                "role": "user",
                "content": {
                    "type": "task_completion",
                    "data": stats
                }
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to record completion: {e}")


def load_weekly_data_for_review(user_id):
    """加载本周数据用于周日复盘"""
    try:
        results = search_memory(
            query=f"本周学习记录 {user_id}",
            top_k=20
        )
        return aggregate_weekly_stats(results)
    except Exception:
        return None


def parse_memory_results_to_context(memory_results):
    """解析MemOS搜索结果为用户上下文"""
    context = {
        "user_profile": None,
        "yesterday_plan": None,
        "weekly_progress": None,
        "historical_stats": None
    }

    for result in memory_results:
        content_type = result.get("content", {}).get("type")
        if content_type == "user_profile":
            context["user_profile"] = result.get("content", {}).get("data")
        elif content_type == "daily_plan" and is_yesterday(result.get("timestamp")):
            context["yesterday_plan"] = result.get("content", {}).get("data")
        elif content_type == "task_completion" and is_this_week(result.get("timestamp")):
            if not context["weekly_progress"]:
                context["weekly_progress"] = []
            context["weekly_progress"].append(result.get("content", {}).get("data"))

    return context


def calculate_completion_stats(completed_tasks, planned_tasks):
    """计算任务完成统计"""
    total_planned = sum(t.get("planned_duration", 0) for t in planned_tasks)
    total_actual = sum(t.get("actual_duration", 0) for t in completed_tasks)
    completion_rate = (total_actual / total_planned * 100) if total_planned > 0 else 0

    return {
        "total_planned_hours": total_planned,
        "total_actual_hours": total_actual,
        "completion_rate": completion_rate,
        "debt_hours": max(0, total_planned - total_actual)
    }


def aggregate_weekly_stats(weekly_records):
    """汇总本周统计数据"""
    if not weekly_records:
        return None

    aggregated = {
        "math": {"planned": 0, "actual": 0},
        "english": {"planned": 0, "actual": 0},
        "major": {"planned": 0, "actual": 0},
        "politics": {"planned": 0, "actual": 0}
    }

    for record in weekly_records:
        for subject in aggregated.keys():
            aggregated[subject]["planned"] += record.get(f"{subject}_planned", 0)
            aggregated[subject]["actual"] += record.get(f"{subject}_actual", 0)

    # 计算完成率和欠账
    for subject in aggregated.keys():
        planned = aggregated[subject]["planned"]
        actual = aggregated[subject]["actual"]
        aggregated[subject]["rate"] = (actual / planned * 100) if planned > 0 else 0
        aggregated[subject]["debt"] = max(0, planned - actual)

    return aggregated


def log_warning(message):
    """记录警告日志"""
    pass


def is_yesterday(timestamp_str):
    """判断时间戳是否为昨天"""
    try:
        from datetime import datetime, timedelta
        timestamp = datetime.fromisoformat(timestamp_str)
        yesterday = datetime.now() - timedelta(days=1)
        return timestamp.date() == yesterday.date()
    except:
        return False


def is_this_week(timestamp_str):
    """判断时间戳是否为本周"""
    try:
        from datetime import datetime
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_end = week_start + timedelta(days=6)
        return week_start.date() <= timestamp.date() <= week_end.date()
    except:
        return False
```

---

## 主规划算法（v2.1 降级兼容版）

当MemOS不可用时，系统会降级使用v2.1.0算法：

```python
def generate_daily_plan(user_input, mode="minimal", previous_plan=None):
    """
    根据用户输入模式生成计划（含实战补丁，无MemOS降级版）

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划
    """

    # 1. 检查任务欠账（实战补丁1）
    debt_tasks = check_task_debt(previous_plan, user_input.get("completed_tasks"))

    if debt_tasks:
        # 欠账处理
        return generate_debt_handling_plan(user_input, debt_tasks)

    # 2. 检查是否周日（实战补丁2）
    if is_sunday(today):
        return generate_sunday_review_plan(user_input)

    # 3. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input)
    else:
        user_data = user_input

    # 4. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 5. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 6. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_input.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 7. 分配时段到科目（含最小块时长检查）
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue,
        min_block_check=True  # 实战补丁3
    )

    return plan


def check_task_debt(previous_plan, completed_tasks):
    """
    检查任务欠账（实战补丁1）

    返回:
        欠账任务列表
    """
    if not previous_plan:
        return []

    debt_tasks = []
    for task in previous_plan.tasks:
        if task not in completed_tasks:
            debt_tasks.append(task)

    return debt_tasks


def generate_debt_handling_plan(user_input, debt_tasks):
    """
    生成补课计划（实战补丁1）

    欠账处理策略：
    - 轻微（<1h）：碎片时间补
    - 中等（1-3h）：压缩低优先任务
    - 严重（>3h）：建议补课日
    """
    total_debt_hours = sum(task.duration for task in debt_tasks)

    if total_debt_hours < 1:
        strategy = "fragment"
    elif total_debt_hours < 3:
        strategy = "compress"
    else:
        strategy = "recovery_day"

    # 生成AI询问
    question = format_debt_question(debt_tasks, total_debt_hours, strategy)

    # 返回补课计划选项
    return {
        "type": "debt_handling",
        "debt_tasks": debt_tasks,
        "total_hours": total_debt_hours,
        "strategy": strategy,
        "question": question,
        "options": generate_debt_options(debt_tasks, strategy)
    }


def generate_sunday_review_plan(user_input):
    """
    生成周日复盘计划（实战补丁2）

    强制包含：
    - 本周完成度统计
    - 2小时错题重做
    - 进度对齐检查
    """
    return {
        "type": "sunday_review",
        "date": today,
        "tasks": [
            {"time": "19:00-19:30", "task": "本周完成度统计", "required": True},
            {"time": "19:30-20:00", "task": "数学错题重做", "required": True},
            {"time": "20:00-20:30", "task": "英语错题重做", "required": True},
            {"time": "20:30-21:00", "task": "专业课错题重做", "required": True},
            {"time": "21:00-21:30", "task": "政治错题重做", "required": True},
            {"time": "21:30-22:00", "task": "进度对齐检查", "required": True},
            {"time": "22:00-23:00", "task": "下周计划调整", "required": True}
        ]
    }


def check_min_block_duration(slot, subject):
    """
    检查时段是否满足科目最小时长要求（实战补丁3）

    如果不满足，自动替换为可碎片化的科目
    """
    min_duration = get_min_block_duration(subject)

    if slot.duration < min_duration:
        # 不满足，自动替换
        return suggest_fragment_subject(slot.duration)

    return subject


def get_min_block_duration(subject):
    """获取科目最小时长要求"""
    requirements = {
        "数学": 1.5,      # 需要90分钟以上进入状态
        "英语阅读": 1.0,  # 需要完整文章语境
        "专业课": 1.0,    # 需要深度思考
        "单词": 0.25,     # 15分钟即可
        "政治选择": 0.33, # 20分钟即可
        "错题复习": 0.5   # 30分钟即可
    }
    return requirements.get(subject, 1.0)


def suggest_fragment_subject(duration):
    """为碎片时段建议合适的科目"""
    if duration <= 0.25:  # 15分钟以内
        return "单词"
    elif duration <= 0.5:  # 30分钟以内
        return "政治选择题"
    else:  # 30-60分钟
        return "错题复习"
```

---

## 主规划算法（自适应版）

```python
def generate_daily_plan(user_input, mode="minimal"):
    """
    根据用户输入模式生成计划

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")

    返回:
        每日计划
    """

    # 1. 根据模式确定数据丰富度
    if mode == "minimal":
        # 极简模式：使用默认值
        user_data = apply_defaults(user_input)
    elif mode == "standard":
        # 标准模式：考虑考试日期
        user_data = enrich_with_exam_info(user_input)
    else:
        # 高级模式：使用完整数据
        user_data = user_input

    # 2. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 3. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 4. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_data.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0  # 默认精力良好

    # 5. 分配时段到科目
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue
    )

    return plan
```

---

## 辅助函数

### 疲劳度计算

```python
def calculate_mixed_fatigue(self_report, behavior_data=None):
    """
    混合疲劳度计算

    参数:
        self_report: 用户主观感受
        behavior_data: 行为数据（可选）

    返回:
        疲劳度 (0.0-1.0)
    """
    # 主观感受权重 0.6
    self_report_map = {
        "精力很好": 0.0,
        "正常": 0.3,
        "有点累": 0.6,
        "很累": 0.9
    }
    subjective = self_report_map.get(self_report, 0.3)

    # 行为数据权重 0.4
    if behavior_data:
        behavioral = calculate_behavior_fatigue(behavior_data)
    else:
        behavioral = 0.0

    return subjective * 0.6 + behavioral * 0.4
```

### 时段偏好

```python
def get_slot_preferences(chronotype):
    """
    根据作息类型返回时段偏好

    参数:
        chronotype: "morning_person" | "night_person" | "normal"

    返回:
        时段偏好字典
    """
    if chronotype == "night_person":
        return {
            "morning": ["单词", "轻松内容"],
            "afternoon": ["英语阅读", "专业课"],
            "evening": ["数学", "高难度内容"],
            "late_night": ["适度复习"]
        }
    else:  # 默认晨型人
        return {
            "morning": ["数学", "英语单词"],
            "afternoon": ["英语阅读", "专业课"],
            "evening": ["专业课", "政治", "复盘"],
            "late_night": ["仅复习"]
        }
```

### 欠账检测（v3.1增强版）

```python
def check_task_debt_with_memory(previous_plan, user_input, user_context):
    """
    检查任务欠账（v3.1增强版：含熔断机制）

    参数:
        previous_plan: 昨日计划
        user_input: 用户输入
        user_context: 用户上下文

    返回:
        欠账任务信息 或 熔断信息
    """
    debt_tasks = []

    # 如果提供了previous_plan参数，直接使用
    if previous_plan:
        debt_tasks = check_task_debt(previous_plan, user_input.get("completed_tasks"))
    # 否则尝试从MemOS读取昨日计划
    elif user_context:
        yesterday_plan = user_context.get("yesterday_plan")
        if yesterday_plan:
            debt_tasks = check_task_debt(yesterday_plan, user_input.get("completed_tasks"))

    if not debt_tasks:
        return None

    # v3.1: 熔断检查
    total_debt_hours = calculate_total_debt_hours(user_context, debt_tasks)
    DEBT_LIMIT = 10  # 10小时熔断阈值

    if total_debt_hours > DEBT_LIMIT:
        return {
            "type": "debt_emergency",
            "total_hours": total_debt_hours,
            "strategy": "recovery_only",
            "message": f"⚠️ 欠账已达{total_debt_hours}小时，超过安全阈值（{DEBT_LIMIT}小时）",
            "suggestion": "暂停所有新内容，专注补账",
            "tasks": generate_recovery_plan(total_debt_hours)
        }

    return {
        "type": "debt_warning",
        "tasks": debt_tasks,
        "total_hours": total_debt_hours
    }


def calculate_total_debt_hours(user_context, current_debt_tasks):
    """计算总欠账时长（含历史累计）"""
    current_debt = sum(task.get("duration", 0) for task in current_debt_tasks)

    # 从用户上下文中获取历史累计欠账
    historical_debt = 0
    if user_context and user_context.get("weekly_progress"):
        for record in user_context.get("weekly_progress", []):
            historical_debt += record.get("debt_hours", 0)

    return current_debt + historical_debt


def generate_recovery_plan(total_debt_hours):
    """生成紧急恢复计划（熔断触发后使用）"""
    recovery_tasks = [
        {
            "subject": "数学",
            "duration": min(total_debt_hours * 0.4, 4),
            "task": "【补账】数学错题重做 + 未完成练习",
            "priority": 1
        },
        {
            "subject": "专业课",
            "duration": min(total_debt_hours * 0.3, 3),
            "task": "【补账】专业课复习",
            "priority": 2
        },
        {
            "subject": "英语",
            "duration": min(total_debt_hours * 0.2, 2),
            "task": "【补账】英语阅读补做",
            "priority": 3
        },
        {
            "subject": "政治",
            "duration": min(total_debt_hours * 0.1, 1),
            "task": "【补账】政治选择题补做",
            "priority": 4
        }
    ]

    return recovery_tasks


def generate_emergency_recovery_plan(debt_result):
    """生成紧急恢复计划（熔断模式）"""
    return {
        "type": "emergency_recovery",
        "total_debt_hours": debt_result.get("total_hours"),
        "message": debt_result.get("message"),
        "suggestion": debt_result.get("suggestion"),
        "recovery_plan": debt_result.get("tasks"),
        "notice": "⚠️ 今日暂停所有新内容学习，专注补账。欠账降至安全阈值后自动恢复正常模式。"
    }
```

### 画像刷新检查

```python
def check_context_freshness(user_context, current_date):
    """
    检查用户画像是否需要刷新（v3.1 context_refresh机制）

    参数:
        user_context: 用户上下文（含用户画像）
        current_date: 当前日期

    返回:
        None 或 刷新询问信息字典
    """
    if not user_context:
        return None

    profile = user_context.get("user_profile")
    if not profile:
        return None

    # 检查画像更新时间
    updated_at = profile.get("updated_at")
    if not updated_at:
        return None

    try:
        from datetime import datetime
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        days_since_update = (current_date - updated_at.date()).days

        # 超过30天自动触发刷新询问
        if days_since_update > 30:
            refresh_config = profile.get("refresh_config", {})
            auto_refresh_interval = refresh_config.get("auto_refresh_interval", 30)

            if days_since_update > auto_refresh_interval:
                return {
                    "needs_refresh": True,
                    "reason": f"画像已{days_since_update}天未更新",
                    "days_since_update": days_since_update,
                    "current_chronotype": profile.get("profile", {}).get("chronotype", "未知"),
                    "current_sensitivity": profile.get("preferences", {}).get("fatigue_sensitivity", "未知"),
                    "questions": [
                        "你的作息类型有变化吗？(晨型人/夜型人/正常)",
                        "科目优先级需要调整吗？",
                        "疲劳敏感度有变化吗？(高/中/低)"
                    ]
                }
    except Exception as e:
        log_warning(f"Failed to check context freshness: {e}")

    return {"needs_refresh": False}


def generate_profile_refresh_question(refresh_info):
    """生成画像刷新询问"""
    return {
        "type": "profile_refresh",
        "reason": refresh_info.get("reason"),
        "days_since_update": refresh_info.get("days_since_update"),
        "current_settings": {
            "chronotype": refresh_info.get("current_chronotype"),
            "fatigue_sensitivity": refresh_info.get("current_sensitivity")
        },
        "questions": refresh_info.get("questions"),
        "message": f"⚠️ {refresh_info.get('reason')}，为了提供更准确的计划，请确认以下设置是否有变化："
    }
```

### 心理干预检查

```python
def check_mental_health_intervention(user_context):
    """
    检查是否需要心理干预（v3.1 mental_status追踪）

    参数:
        user_context: 用户上下文

    返回:
        None 或 干预信息字典
    """
    if not user_context:
        return None

    profile = user_context.get("user_profile")
    if not profile:
        return None

    mental_history = profile.get("mental_history", [])
    if not mental_history or len(mental_history) < 3:
        return None

    # 检查最近3天的状态
    recent_days = mental_history[-3:]
    tired_count = sum(1 for d in recent_days if d.get("status") in ["tired", "burned_out"])

    if tired_count >= 3:
        # 分析压力水平
        avg_stress = sum(d.get("stress_level", 0.5) for d in recent_days) / len(recent_days)

        # 找出触发原因
        triggers = [d.get("trigger") for d in recent_days if d.get("trigger")]
        common_trigger = max(set(triggers), key=triggers.count) if triggers else "持续学习"

        return {
            "intervention_needed": True,
            "mode": "psychological_adjustment",
            "tired_days": tired_count,
            "avg_stress": avg_stress,
            "common_trigger": common_trigger,
            "actions": [
                "在计划开头添加鼓励语",
                "强制安排休息活动",
                "减少学习量30%"
            ]
        }

    return None


def record_mental_status(user_id, mental_status, stress_level, trigger=None):
    """记录用户心理状态到MemOS"""
    try:
        from datetime import datetime

        add_message(
            messages=[{
                "role": "user",
                "content": {
                    "type": "mental_status_update",
                    "data": {
                        "date": datetime.now().date().isoformat(),
                        "status": mental_status,
                        "stress_level": stress_level,
                        "trigger": trigger
                    }
                },
                "tags": ["#mental_status", f"#date_{datetime.now().strftime('%Y-%m-%d')}"]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to record mental status: {e}")
```

---

## 时间块切分算法

```python
def split_large_time_block(duration, subject):
    """
    将长时间块自动切分为高效的小时间块

    参数:
        duration: 原始时长（分钟）
        subject: 科目类型

    返回:
        切分后的时间块列表
    """
    # 数学等高强度科目：45分钟一块
    if subject in ["数学", "专业课"]:
        block_duration = 45
        break_duration = 15
    # 英语阅读等中等强度：60分钟一块
    elif subject in ["英语阅读"]:
        block_duration = 60
        break_duration = 15
    # 单词等低强度：可直接延续
    else:
        return [{"type": "continuous", "duration": duration}]

    blocks = []
    remaining = duration

    while remaining > 0:
        if remaining <= block_duration:
            blocks.append({"type": "study", "duration": remaining})
            break
        else:
            blocks.append({"type": "study", "duration": block_duration})
            blocks.append({"type": "break", "duration": break_duration})
            remaining -= (block_duration + break_duration)

    return blocks
```

**示例**：
```
原计划：14:00-17:00 数学（连续3小时）
↓ 自动切分为高效时间块
14:00-14:45 | 数学 | 第1块（45分钟）
14:45-15:00 | ☕ 休息 | 15分钟
15:00-15:45 | 数学 | 第2块（45分钟）
15:45-16:00 | ☕ 休息 | 15分钟
16:00-16:45 | 数学 | 第3块（45分钟）
16:45-17:00 | ☕ 休息 | 15分钟
```

---

> 📋 **返回主文档**: [skill.md](skill.md)
