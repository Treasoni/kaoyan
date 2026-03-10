# kaoyan-english-vocab 代码模块

本文档包含 kaoyan-english-vocab 技能的所有代码实现。

---

## 1. 真题语境检索策略

### 1.1 generate_context_article

生成语境文章，优先使用真题语境。

```python
def generate_context_article(word_list, user_preferences):
    """生成语境文章

    Args:
        word_list: 今日目标词汇
        user_preferences: 考试类型(英一/英二)、偏好主题等

    Returns:
        Article: 语境文章对象
    """
    contexts = []

    for word in word_list:
        # 1. 优先检索真题语境
        real_exam_context = search_real_exam_pool(
            word,
            exam_type=user_preferences.exam_type,
            recent_years=5  # 优先近5年
        )
        if real_exam_context:
            contexts.append(real_exam_context)
            continue

        # 2. 检索外刊同源语境
        journal_context = search_journal_pool(word)
        if journal_context:
            contexts.append(journal_context)
            continue

        # 3. 最后才用AI生成
        ai_context = generate_ai_context(
            word,
            style="The Economist",  # 明确指定外刊风格
            complexity=calculate_sentence_complexity(word)
        )
        ai_context.metadata.source = "AI生成(模拟)"
        contexts.append(ai_context)

    # 4. 将语境串联成"真题模拟材料"
    article = weave_contexts_into_article(contexts)

    return article


def search_real_exam_pool(word, exam_type, recent_years=5):
    """搜索真题语境池

    Args:
        word: 目标单词
        exam_type: 考试类型（英一/英二）
        recent_years: 优先近年真题

    Returns:
        Context: 真题语境对象，找不到返回None
    """
    # 搜索真题语境池
    pool_path = f"/考研英语/📚 真题语境池/{exam_type}/"

    # 按年份倒序搜索
    current_year = datetime.now().year
    for year in range(current_year, current_year - recent_years, -1):
        context = search_context_in_year_pool(word, pool_path, year)
        if context:
            return context

    return None


def search_journal_pool(word):
    """搜索外刊同源语境池

    Args:
        word: 目标单词

    Returns:
        Context: 外刊语境对象，找不到返回None
    """
    pool_path = "/考研英语/📰 外刊同源库/"

    # 搜索 The Economist, The Guardian 等
    for journal in ["The Economist", "The Guardian", "TIME"]:
        context = search_context_in_journal(word, pool_path, journal)
        if context:
            return context

    return None


def generate_ai_context(word, style="The Economist", complexity="medium"):
    """AI生成语境

    Args:
        word: 目标单词
        style: 文章风格
        complexity: 句式复杂度

    Returns:
        Context: AI生成的语境对象
    """
    return {
        "word": word,
        "sentence": f"[AI生成句子，风格：{style}]",
        "source": "AI生成(模拟)",
        "style": style,
        "complexity": complexity
    }


def weave_contexts_into_article(contexts):
    """将语境串联成文章

    Args:
        contexts: 语境列表

    Returns:
        Article: 完整文章
    """
    # 按主题或逻辑串联语境
    article = {
        "title": "真题模拟材料",
        "paragraphs": [],
        "word_count": 0,
        "source_stats": {
            "real_exam": 0,
            "journal": 0,
            "ai_generated": 0
        }
    }

    for ctx in contexts:
        # 统计来源
        if ctx.get("source") == "真题":
            article["source_stats"]["real_exam"] += 1
        elif "外刊" in ctx.get("source", ""):
            article["source_stats"]["journal"] += 1
        else:
            article["source_stats"]["ai_generated"] += 1

        # 构建段落
        article["paragraphs"].append(ctx.get("sentence", ""))
        article["word_count"] += len(ctx.get("sentence", "").split())

    return article
```

---

## 2. 熟词僻义检测算法

### 2.1 detect_polysemy

检测单词是否在考研中有僻义。

```python
def detect_polysemy(word):
    """检测单词是否在考研中有僻义

    Args:
        word: 目标单词

    Returns:
        PolysemyAlert: 僻义预警对象
        None: 无僻义
    """
    # 1. 检索考研大纲词表
    outline_entry = search_exam_outline(word)

    # 2. 对比大纲释义与常见释义
    common_meanings = get_common_dictionary_meanings(word)
    exam_meanings = outline_entry.meanings

    # 3. 计算语义重叠度
    overlap = calculate_semantic_overlap(common_meanings, exam_meanings)

    # 4. 判断是否存在僻义
    if overlap < 0.5:  # 重叠度低于50%，存在显著僻义
        return PolysemyAlert(
            word=word,
            alert_type="critical" if overlap < 0.3 else "warning",
            rare_meanings=[m for m in exam_meanings if m not in common_meanings],
            common_meanings=common_meanings,
            exam_frequency=calculate_exam_frequency(word)
        )

    return None


def calculate_semantic_overlap(meanings1, meanings2):
    """计算两个释义集合的语义重叠度

    Args:
        meanings1: 释义集合1
        meanings2: 释义集合2

    Returns:
        float: 重叠度 (0.0-1.0)
    """
    if not meanings1 or not meanings2:
        return 0.0

    # 简化实现：计算释义关键词交集比例
    words1 = set()
    for m in meanings1:
        words1.update(m.lower().split())

    words2 = set()
    for m in meanings2:
        words2.update(m.lower().split())

    # 移除停用词
    stopwords = {"the", "a", "an", "of", "to", "in", "for", "and", "or"}
    words1 -= stopwords
    words2 -= stopwords

    if not words1 or not words2:
        return 0.0

    intersection = words1 & words2
    union = words1 | words2

    return len(intersection) / len(union)


def calculate_exam_frequency(word):
    """计算单词在考研中的出现频率

    Args:
        word: 目标单词

    Returns:
        str: 频率等级 (high/medium/low)
    """
    # 查询历年真题词频
    frequency_data = query_exam_frequency_database(word)

    if frequency_data >= 5:
        return "high"
    elif frequency_data >= 2:
        return "medium"
    else:
        return "low"
```

---

## 3. 熟词僻义库数据

### 3.1 Critical级别（高频陷阱）

```yaml
POLYSEMY_CRITICAL:
  - word: "address"
    common_meaning: "地址"
    rare_meaning: "vt. 处理，解决"
    exam_frequency: "80%"
    collocations: ["address the problem", "address an issue", "address concerns"]

  - word: "school"
    common_meaning: "学校"
    rare_meaning: "n. 流派，学派"
    exam_frequency: "70%"
    collocations: ["school of thought", "different schools"]

  - word: "novel"
    common_meaning: "新颖的"
    rare_meaning: "n. 长篇小说"
    exam_frequency: "65%"
    collocations: ["historical novel", "novel writer"]

  - word: "fine"
    common_meaning: "好的"
    rare_meaning: "n./v. 罚款"
    exam_frequency: "60%"
    collocations: ["impose a fine", "fine sb for sth"]

  - word: "reason"
    common_meaning: "原因"
    rare_meaning: "v. 推理，推论"
    exam_frequency: "55%"
    collocations: ["reason with sb", "reasoning ability"]

  - word: "discipline"
    common_meaning: "纪律"
    rare_meaning: "n. 学科"
    exam_frequency: "50%"
    collocations: ["academic discipline", "various disciplines"]

  - word: "consume"
    common_meaning: "消费"
    rare_meaning: "vt. 毁灭，烧毁"
    exam_frequency: "40%"
    collocations: ["be consumed by", "consume time"]

  - word: "draft"
    common_meaning: "草稿"
    rare_meaning: "n. 征兵"
    exam_frequency: "35%"
    collocations: ["military draft", "draft dodger"]

  - word: "compound"
    common_meaning: "复合的"
    rare_meaning: "v. 加剧，恶化"
    exam_frequency: "30%"
    collocations: ["compound the problem", "compound interest"]
```

### 3.2 Warning级别（中等陷阱）

```yaml
POLYSEMY_WARNING:
  - word: "spring"
    common_meaning: "春天"
    rare_meaning: "v. 突然出现，涌现"
    exam_frequency: "40%"
    collocations: ["spring up", "spring from"]

  - word: "table"
    common_meaning: "桌子"
    rare_meaning: "v. 搁置，暂缓讨论"
    exam_frequency: "35%"
    collocations: ["table a proposal", "table the motion"]

  - word: "book"
    common_meaning: "书"
    rare_meaning: "v. 预订"
    exam_frequency: "30%"
    collocations: ["book a ticket", "book in advance"]
```

---

## 4. 快速查词函数

### 4.1 lookup_word

快速查询单词信息，含僻义预警。

```python
def lookup_word(word, exam_type="english_2"):
    """快速查询单词信息

    Args:
        word: 目标单词
        exam_type: 考试类型

    Returns:
        dict: 单词信息卡片
    """
    # 1. 获取基本信息
    basic_info = get_basic_word_info(word)

    # 2. 检测僻义
    polysemy_alert = detect_polysemy(word)

    # 3. 获取真题例句
    real_exam_examples = get_real_exam_examples(word, exam_type)

    # 4. 获取搭配
    collocations = get_common_collocations(word)

    # 5. 获取词族
    word_family = get_word_family(word)

    return {
        "word": word,
        "pronunciation": basic_info.get("pronunciation"),
        "part_of_speech": basic_info.get("part_of_speech"),
        "meanings": basic_info.get("meanings"),
        "polysemy_alert": polysemy_alert,
        "real_exam_examples": real_exam_examples,
        "collocations": collocations,
        "word_family": word_family
    }


def format_word_card(word_info):
    """格式化单词卡片输出

    Args:
        word_info: 单词信息字典

    Returns:
        str: Markdown格式的单词卡片
    """
    card = f"""# {word_info['word']}

## 基本信息
**音标**: {word_info.get('pronunciation', 'N/A')}
**词性**: {word_info.get('part_of_speech', 'N/A')}
"""

    # 僻义预警
    if word_info.get('polysemy_alert'):
        alert = word_info['polysemy_alert']
        icon = "⚠️" if alert.alert_type == "critical" else "⚡"
        card += f"""
## {icon} 僻义预警 [{alert.alert_type}]

> [!danger] 陷阱提示
> 此词在考研中 **{alert.exam_frequency}** 考查僻义

**考研常考僻义**: {', '.join(alert.rare_meanings)}

### 常用搭配
"""
        for col in alert.collocations:
            card += f"- {col}\n"

    # 真题例句
    if word_info.get('real_exam_examples'):
        card += "\n### 真题例句\n"
        for example in word_info['real_exam_examples'][:3]:
            card += f"""> [!example] {example['year']}年真题 {example['section']}
> {example['sentence']}
"""

    return card
```

---

## 5. PDF词汇提取函数

### 5.1 extract_words_from_pdf

从PDF中提取单词列表。

```python
def extract_words_from_pdf(pdf_path, app_type="momo"):
    """从PDF中提取单词列表

    Args:
        pdf_path: PDF文件路径
        app_type: APP类型（momo/baici）

    Returns:
        list: 单词列表
    """
    # 读取PDF内容
    content = read_pdf(pdf_path)

    # 根据APP类型选择解析器
    if app_type == "momo":
        words = parse_momo_format(content)
    elif app_type == "baici":
        words = parse_baici_format(content)
    else:
        words = parse_generic_format(content)

    return words


def parse_momo_format(content):
    """解析墨墨背单词导出格式"""
    words = []
    lines = content.split('\n')

    for line in lines:
        # 墨墨格式: 单词 [音标] 释义
        match = re.match(r'^(\w+)\s*\[([^\]]+)\]\s*(.+)$', line.strip())
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": match.group(2),
                "meaning": match.group(3).strip()
            })

    return words


def parse_baici_format(content):
    """解析百词斩导出格式"""
    words = []
    lines = content.split('\n')

    for line in lines:
        # 百词斩格式可能不同
        match = re.match(r'^(\w+)\s+(.+)$', line.strip())
        if match:
            words.append({
                "word": match.group(1),
                "meaning": match.group(2).strip()
            })

    return words
```

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
