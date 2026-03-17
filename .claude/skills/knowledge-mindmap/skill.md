---
name: knowledge-mindmap
description: 自动分析知识点目录结构，生成 Excalidraw 格式的详细思维导图。适用于考研数学、专业课等知识体系的可视化整理。触发词包括"知识点思维导图"、"生成思维导图"、"知识结构图"、"目录结构图"。
metadata:
  version: 1.0.0
---

# Knowledge Mindmap Generator

自动分析知识点目录结构，生成 Excalidraw 格式的详细思维导图。

## 功能说明

这个 skill 专门用于：
- 分析知识点目录的层级结构
- 提取各模块的核心内容
- 生成可视化思维导图
- 保存为 Obsidian Excalidraw 格式

## 使用场景

| 场景 | 示例 |
|------|------|
| 数学知识体系 | `/knowledge-mindmap 考研数学/高数-极限` |
| 专业课结构 | `/knowledge-mindmap 考研专业课/模电` |
| 章节总结 | `/knowledge-mindmap 当前章节` |

## 工作流程

### 1. 目录探索阶段

```
用户指定目录
    ↓
探索目录结构
    ↓
识别知识点模块
    ↓
提取核心内容
```

**自动识别的关键文件：**
- `📑 索引.md` - 模块总索引
- `📊 学习进度.md` - 学习进度追踪
- `📝 章节总结.md` - 全章总结
- `README.md` - 模块说明
- 各知识点笔记文件

### 2. 内容分析阶段

从笔记中提取：
- 模块标题和星级（⭐⭐⭐⭐⭐）
- 核心概念和定义
- 重要定理和公式
- 解题方法和技巧
- 易错点和注意事项

### 3. 思维导图生成阶段

生成 Excalidraw JSON 格式的思维导图。

## 输出格式

### Obsidian Excalidraw 格式（默认）

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
\`\`\`json
{JSON 完整数据}
\`\`\`
%%
```

**关键要点：**
- Frontmatter 必须包含 `tags: [excalidraw]`
- JSON 必须被 `%%` 标记包围
- 文件扩展名：`.md`

## 设计规范

### 布局策略

采用**中心发散布局**：

```
                    [模块1]
                        ↑
[模块2] ←← [模块3] ←← [中心主题] →→ [模块4] →→ [模块5]
                        ↓
                    [模块6]
                        ↓
                   [辅助系统]
```

### 颜色编码

| 元素类型 | 边框颜色 | 背景颜色 | 用途 |
|---------|---------|---------|------|
| **中心节点** | `#1e40af` | `#dbeafe` | 椭圆形，主题核心 |
| **五星模块** | `#f59e0b` | `#fef3c7` | 核心考点，粗边框 |
| **普通模块** | `#3b82f6` | `#eff6ff` | 基础知识点 |
| **辅助系统** | `#9ca3af` | `#f3f4f6` | 虚线边框 |
| **连接线** | 根据目标类型 | - | 实线或虚线 |

### 模块尺寸

| 模块类型 | 宽度 | 高度 | 字体大小 |
|---------|------|------|---------|
| 中心节点 | 300-400px | 120-140px | 28-32px |
| 五星模块 | 200-240px | 200-280px | 15px |
| 普通模块 | 200-260px | 150-200px | 15px |
| 辅助系统 | 500-620px | 180-200px | 14px |

## JSON 结构规范

### 完整结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [
    /* 所有元素 */
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

### 元素模板

#### 中心节点（椭圆）

```json
{
  "id": "center",
  "type": "ellipse",
  "x": 400,
  "y": 250,
  "width": 400,
  "height": 140,
  "angle": 0,
  "strokeColor": "#1e40af",
  "backgroundColor": "#dbeafe",
  "fillStyle": "solid",
  "strokeWidth": 3,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a0",
  "roundness": {"type": 2},
  "seed": 100,
  "version": 1,
  "versionNonce": 101,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false
}
```

#### 五星模块（矩形）

```json
{
  "id": "box-star-1",
  "type": "rectangle",
  "x": 300,
  "y": 20,
  "width": 240,
  "height": 280,
  "angle": 0,
  "strokeColor": "#f59e0b",
  "backgroundColor": "#fef3c7",
  "fillStyle": "solid",
  "strokeWidth": 3,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a1",
  "roundness": {"type": 3},
  "seed": 112,
  "version": 1,
  "versionNonce": 113,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false
}
```

#### 普通模块（矩形）

```json
{
  "id": "box-normal-1",
  "type": "rectangle",
  "x": 30,
  "y": 50,
  "width": 260,
  "height": 180,
  "angle": 0,
  "strokeColor": "#3b82f6",
  "backgroundColor": "#eff6ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a2",
  "roundness": {"type": 3},
  "seed": 104,
  "version": 1,
  "versionNonce": 105,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false
}
```

#### 文本元素

```json
{
  "id": "text-1",
  "type": "text",
  "x": 50,
  "y": 60,
  "width": 220,
  "height": 160,
  "angle": 0,
  "strokeColor": "#374151",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a3",
  "roundness": {"type": 3},
  "seed": 106,
  "version": 1,
  "versionNonce": 107,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false,
  "text": "模块标题\n⭐⭐⭐⭐⭐\n\n• 要点1\n• 要点2\n• 要点3",
  "rawText": "模块标题\n⭐⭐⭐⭐⭐\n\n• 要点1\n• 要点2\n• 要点3",
  "fontSize": 15,
  "fontFamily": 5,
  "textAlign": "left",
  "verticalAlign": "top",
  "containerId": null,
  "originalText": "模块标题\n⭐⭐⭐⭐⭐\n\n• 要点1\n• 要点2\n• 要点3",
  "autoResize": true,
  "lineHeight": 1.25
}
```

#### 连接箭头

```json
{
  "id": "arrow-1",
  "type": "arrow",
  "x": 400,
  "y": 250,
  "width": 120,
  "height": 140,
  "angle": 0,
  "strokeColor": "#3b82f6",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a20",
  "roundness": {"type": 2},
  "seed": 140,
  "version": 1,
  "versionNonce": 141,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false,
  "points": [[0, 0], [-100, -100], [-120, -140]],
  "lastCommittedPoint": [0, 0],
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

## 文本处理规则

### 字符替换

| 原字符 | 替换为 | 说明 |
|-------|-------|------|
| `"` | `『』` | 双引号 |
| `()` | `「」` | 圆括号 |

### 文本格式

```
模块标题
⭐⭐⭐⭐⭐ (如有)

• 要点1
  - 子要点
• 要点2
• 要点3
```

### 字体规范

- **字体家族**：`fontFamily: 5`（Excalifont）
- **行高**：`lineHeight: 1.25`
- **对齐方式**：`textAlign: "left"`, `verticalAlign: "top"`

## 自动保存流程

### 1. 生成文件名

格式：`{主题名称}.思维导图.md`

示例：
- `数列极限.思维导图.md`
- `函数极限与连续.思维导图.md`

### 2. 保存位置

保存到用户指定的目录，或当前工作目录。

### 3. 用户反馈

生成完成后报告：
- 文件保存位置
- 如何在 Obsidian 中查看
- 思维导图结构概览

## 常见问题排查

### JSON 语法错误

**问题**：思维导图无法显示，提示解析错误。

**检查项**：
1. 确保所有字符串值正确引用
2. 检查是否有未闭合的括号
3. 确保数值类型没有多余引号（如 `"x": 730"` 应为 `"x": 730`）
4. 检查 `points` 数组格式是否正确

### 布局问题

**问题**：元素重叠或位置不当。

**解决方案**：
- 调整各模块的 x, y 坐标
- 确保模块间有足够间距
- 检查画布范围（建议 0-1200 x 0-800）

## 示例输出

```
思维导图已生成！

保存位置：[[考研数学/高数-数列极限/数列极限.思维导图.md]]

使用方法：
1. 在 Obsidian 中打开此文件
2. 按 Ctrl+E（Mac: Cmd+E）切换到阅读模式
3. 或点击右上角 ··· → Switch to EXCALIDRAW VIEW

结构概览：
- 中心主题：数列极限
- 核心模块（⭐⭐⭐⭐⭐）：用性质、海涅定理、夹逼准则、单调有界
- 基础模块：数列概念、定义、四则运算、收敛速度
- 辅助系统：索引、进度、总结、错题本
```

## 注意事项

1. **JSON 语法严格**：确保 JSON 格式完全正确，任何语法错误都会导致解析失败
2. **坐标系统**：左上角为原点 (0,0)，x 向右增大，y 向下增大
3. **元素 ID 唯一**：每个元素必须有唯一的 `id`
4. **文本长度**：避免单个文本元素过长，适当分行
5. **星级标注**：保留原有的星级标注（⭐），便于识别重点
