# Day 编号计算规则

> **重要**：本技能使用 `kaoyan-english-core` 提供的共享Day编号计算函数。

## 计算步骤

1. **检查现有文件**：
   ```bash
   find 考研英语/📰 真题语境文章 -name "*.md" | sort | tail -5
   ```

2. **提取最大Day编号**：
   - 从文件名格式 `Day-XXX-YYYY-MM-DD.md` 提取 XXX
   - 例如：`Day-015-2026-03-14.md` → Day编号 = 15

3. **计算新Day编号**：
   - 新Day编号 = 最大Day编号 + 1
   - 例如：最大是 Day-015 → 新文件使用 Day-016

4. **文件命名格式**：
   - 真题文章：`Context-Day-{XXX}-{YYYY-MM-DD}.md`
   - 测试记录：`Quiz-Day-{XXX}-{YYYY-MM-DD}.md`
   - 词汇统计：`Statistics-Day-{XXX}-{YYYY-MM-DD}.md`
   - 写作输出：`Writing-Day-{XXX}-{YYYY-MM-DD}.md`

## 注意事项

- ❌ **禁止**硬编码 "Day-001"
- ✅ **必须**先检查现有文件再生成新编号
- ✅ 所有4类文件使用**相同的Day编号**

## 推荐做法（使用共享函数）

```python
# 使用共享函数获取验证后的Day编号
from kaoyan_english_core import get_validated_day_number, generate_day_filenames

# 获取Day编号（双重验证）
day_number = get_validated_day_number("2026-03-16")  # 返回：17

# 生成文件名
filenames = generate_day_filenames("2026-03-16", day_number)
# {
#     "context_article": "Context-Day-017-2026-03-16.md",
#     "statistics": "Statistics-Day-017-2026-03-16.md"
# }
```

## 核心函数位置

详细实现请参考：`.claude/skills/kaoyan-english-core/code.md` 第8节

## Day编号对应关系

| 日期 | Day编号 |
|------|---------|
| 2026-02-28 | Day 001 |
| 2026-03-01 | Day 002 |
| 2026-03-15 | Day 016 |
| 2026-03-16 | Day 017 |
| 2026-03-17 | Day 018 |

---

*更新日期: 2026-03-16*
