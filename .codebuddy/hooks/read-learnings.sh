#!/bin/bash
# PreToolUse hook: 在每个 agent 启动前读取错误记录和规则
# 输出到 stderr，这样 agent 能看到但不会污染工具返回值

LEARNINGS_DIR="/Users/zhqznc/Documents/考研复习/.learnings"

echo "=== 📚 历史错误与规则速查 ===" >&2

if [ -f "$LEARNINGS_DIR/RULES.md" ]; then
    echo "" >&2
    echo "--- RULES (高频规则) ---" >&2
    cat "$LEARNINGS_DIR/RULES.md" >&2
fi

if [ -f "$LEARNINGS_DIR/ERRORS.md" ]; then
    echo "" >&2
    echo "--- ERRORS (最近错误) ---" >&2
    # 只输出最近 5 条错误（避免输出过多）
    awk '/^## \[ERR-/{count++} count > 0' "$LEARNINGS_DIR/ERRORS.md" | head -80 >&2
fi

echo "=== 速查结束 ===" >&2

# 返回空 JSON，不阻止工具执行
echo "{}"
exit 0
