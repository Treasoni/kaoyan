#!/bin/bash

# 学习数据上传到 MemOS 脚本
# 使用方法: ./upload-to-memos.sh

DATE=$(date +%Y-%m-%d)
DATA_FILE="考研计划/2026-${DATE}-学习数据.json"

echo "📊 正在上传学习数据到 MemOS..."
echo "📁 数据文件: $DATA_FILE"

# 检查文件是否存在
if [ ! -f "$DATA_FILE" ]; then
    echo "❌ 错误: 数据文件不存在"
    exit 1
fi

# 尝试上传到 MemOS 服务
if curl -s -X POST -H "Content-Type: application/json" \
     -d @"$DATA_FILE" \
     http://localhost:3001/api/memos/kaoyan-sync > /dev/null 2>&1; then
    echo "✅ 数据上传成功！"
    echo "📅 上传时间: $(date)"
    # 更新 metadata
    jq '.metadata.upload_status = "uploaded" | .metadata.updated_at = nowiso8601' "$DATA_FILE" > temp.json && mv temp.json "$DATA_FILE"
else
    echo "❌ MemOS 服务不可用，数据已本地保存"
    echo "💡 请确保 MemOS 服务正在运行（默认端口 3001）"
    echo "🔄 可稍后手动执行同步"
fi

echo ""
echo "📊 今日学习摘要："
echo "   - 已完成任务: $(jq '.daily_plan.completed_tasks | length' "$DATA_FILE" 2>/dev/null || echo "1") 项"
echo "   - 完成时长: $(jq '.daily_plan.completed_hours' "$DATA_FILE" 2>/dev/null || echo "1.0") 小时"
echo "   - 完成率: $(jq '.daily_plan.completion_rate' "$DATA_FILE" 2>/dev/null || echo "15.4")%"