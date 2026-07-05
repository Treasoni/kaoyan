#!/bin/bash
# SessionStart hook: 将 .learnings/RULES.md 注入 AI 系统上下文
# stdout → AI context（注入给模型）
# stderr → UI display（展示给用户）

LEARNINGS_DIR="/Users/zhqznc/Documents/考研复习/.learnings"

echo "=== 📚 历史错误与规则速查 ===" >&2

if [ -f "$LEARNINGS_DIR/RULES.md" ]; then
    # stdout：注入给 AI 阅读
    echo "<learnings_rules>"
    cat "$LEARNINGS_DIR/RULES.md"
    echo "</learnings_rules>"
    # stderr：展示给用户
    echo "" >&2
    echo "--- RULES (高频规则) ---" >&2
    cat "$LEARNINGS_DIR/RULES.md" >&2
fi

if [ -f "$LEARNINGS_DIR/ERRORS.md" ]; then
    echo "" >&2
    echo "--- ERRORS (最近错误) ---" >&2
    awk '/^## \[ERR-/{count++} count > 0' "$LEARNINGS_DIR/ERRORS.md" | head -80 >&2
fi

echo "=== 速查结束 ===" >&2

# 返回空 JSON，不阻止工具执行
echo "{}"
exit 0
