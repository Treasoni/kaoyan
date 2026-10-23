---
name: kaoyan-electronics-diagram
description: Use when generating, redrawing, correcting, exporting, or embedding 822 electronic diagrams, including textbook-style SVG/PNG circuit diagrams, DC/AC paths, small-signal equivalents, coupling diagrams, digital logic symbols, state diagrams, timing waveforms, and handwritten-note redraws.
---

# 822 电路图生成

## 核心原则

电路图先保证拓扑正确，再追求教材风。用于学习笔记的精确电路图不把 AI 生成图当最终依据；默认使用可编辑 SVG 作为源图，再导出 PNG 嵌入 Obsidian。

**REQUIRED SUB-SKILL:** Use `kaoyan-electronics-circuit` for circuit recognition and topology analysis.

**REQUIRED SUB-SKILL:** Use `obsidian-markdown` when writing or updating Obsidian notes.

## 使用边界

- 用户要求“画电路图、重绘电路图、教材风电路图、微变等效图、直流/交流通路图、把手写电路图整理进笔记”时使用。
- 只回答概念或题解、不生成图时，由 `kaoyan-electronics-circuit` 或 `kaoyan-electronics-sop` 处理。
- 写给笔记复习的电路图优先 SVG + PNG；需要用户继续拖拽修改时，可改用 Excalidraw。
- 位图生成工具只可做风格参考或封面插图，不可作为需要拓扑准确的最终学习图。

## 固定流程

1. **确认落点**：确定目标笔记、附件目录、章节归属。若来自手写图，先识别图片标题、关键文字和电路类型，不能按当前文件名硬归类。
2. **写网表卡**：列出输入、输出、电源、地、关键节点、器件、端口方向、待分析模式。看不清的参数标“待确认”。
3. **先做通路规则**：明确直流/交流时每个源和储能元件怎么处理。
4. **画源图**：生成 SVG；输入在左、输出在右、电源在上、地在下；黑色主线、红色直流提醒、蓝色交流提醒、灰色表示被开路隔离的外部支路。
5. **导出 PNG**：用 `scripts/render-svg-to-png.sh` 从 SVG 导出 PNG，笔记中嵌入 PNG，保留 SVG 作为可编辑源。
6. **写图注**：图下方必须写“图的作用 + 关键标注/区域 + 做题结论”。
7. **回读验收**：检查文件存在、图片链接、线是否断、节点是否悬空、文字是否被裁切。

## 网表卡模板

```text
电路类型：
目标图：原图 / 直流通路 / 交流通路 / 微变等效 / 多格对照
输入端：
输出端：
电源与地：
关键节点：
器件与参数：
直流处理：
交流处理：
待确认：
```

## 准确性检查

- BJT：NPN 集电极在上、发射极在下、箭头向外；PNP 方向反向检查。
- 电源：直流分析保留偏置源；交流分析中直流电压源置零为交流地，直流电流源置零为开路。
- 电容：直流稳态开路；中频交流只有在 `|X_C|` 远小于相关电阻时才近似短路。
- 信号源：置零的是理想源本身；实际内阻 `R_s` 不要删除。
- 受控源：直流和交流分析中都保留。
- 节点：每个元件两端都要有去向；输出负载是否与 `R_C` 并联，必须按交流节点判断。
- 图面：不要让导线穿过文字；不要用“看起来相邻”代替真实连接。

## 数字电路标准图（逻辑符号 / 状态图 / 波形图）

数电笔记里的图不是电路拓扑，不套用上面的 SVG 网表流程。统一用 matplotlib 出 PNG，公共图元在 `scripts/digital_figures.py`，调用方只给数据和布局。

### 何时使用

- **逻辑符号**：触发器 / 锁存器 / 计数器的矩形符号，含输入输出、边沿三角 `>`、控制端标注 `1S/1J/1T/C1`、异步端小圆圈。
- **状态图**：两个状态圆圈 + 自环 + 双向弧线 + 转换条件标签。
- **时序波形**：CP / 输入 / Q 的阶梯波 + 触发沿竖直虚线 + 每拍动作标注。
- 原课件只有 ASCII 图或低清 jpg 时，重画后把原图折叠到 `> [!note]- 原始课件截图（溯源）`，正文只留新图。

### 图元 API

```python
import sys
sys.path.insert(0, "<vault>/<profile>/skills/kaoyan-electronics-diagram/scripts")  # profile = .claude 或 .agents
from digital_figures import (INK, BLUE, RED, GRAY, new_figure, save,
                             waveform_rows, edge_lines, level_marks, time_axis,
                             flipflop_block, two_state)
```

| 图元 | 用途 | 关键参数 |
| --- | --- | --- |
| `new_figure(figsize, xlim, ylim)` | 空白画布：无坐标轴、等比例 | 数据坐标自己定，`xlim/ylim` 要留出标注空间 |
| `save(fig, path)` | 导出 PNG | 固定 220 dpi、白底、`bbox_inches="tight"` |
| `flipflop_block(ax, x0, y0, w, h, inputs, outputs, top, bottom, title)` | 触发器矩形符号 | `inputs=[(标签, y, 框内标注, 是否三角[, 是否取反])]`；`top/bottom=(标签, x)` 自动加小圆圈 |
| `two_state(ax, self0, self1, fwd, back, note)` | 两状态状态图 | 四项均为 `(文字, 颜色)`；`note` 写无关项或禁止状态说明 |
| `waveform_rows(ax, rows, h=0.62)` | 多条阶梯波 | `rows=[(名称, 基线 y, [(t0, t1, 电平)], 颜色, 线宽)]` |
| `edge_lines(ax, times, y_bottom, y_top)` | 触发沿竖直虚线 | 上下端要避开文字行 |
| `level_marks(ax, base)` | 行首 1/0 标记 | 多行同时标会读成竖列，通常只标第一行 |
| `time_axis(ax, x_start, x_end, y)` | 底部时间轴 | 每图只画一条 |

### 版式约定

- 白底、无网格、`axis off`、等比例；不写标题，标题信息放进图注或图内一处文字。
- 配色固定：CP 蓝 `#1f5fa8`、输入红 `#c0392b`、Q 黑 `#1a1a1a`、参考虚线灰 `#8a8a8a`；辅助信息可用紫 `#7d3c98`、绿 `#1e8449`。
- 波形高度统一 `H = 0.62`；低电平为基线、高电平 = 基线 + `H`，所有跳变画竖直边（`step_trace` 已保证）。
- 行间距 ≥ 1.30；顺序自上而下为 CP → 输入 → Q，或按信号层级排列。
- 跨行标注文字必须加白底 `bbox=dict(facecolor="white", edgecolor="none", pad=1.5)`，否则虚线会穿字。
- 附件命名：`逻辑符号.png`、`状态图.png`、`波形图.png`、`波形图-<场景>.png`（如 `波形图-二分频.png`）、`转换接线图.png`。

### 出图后四项核对（必做）

1. **沿与值**：逐个触发沿回算"沿前瞬间"的输入 → 次态，与画的阶梯波逐段对齐。
2. **标注同拍**：动作文字（置1 / 置0 / 保持 / 翻转）挂在对应触发沿上；标注序列要与 J/K 电平**逐拍一致**。
3. **电平标记**：只在一行标注 1/0，多行齐标会形成干扰竖列。
4. **遮挡与留白**：虚线不穿字、标题不压电平标记、被替换的 ASCII 图不留孤立空行。

### 配套笔记文字

图后按固定顺序写：

1. `> [!info] 读图要点` —— 这张图怎么看（沿在哪、谁决定状态）。
2. `### 画输出波形的三步法` —— 标沿 → 采样 → 保持；锁存器版本换成 判有效电平 → 看跳变 → 保持。
3. `> [!warning] 常见扣分点` —— 3~4 条高频错误，与图上的坑一一对应。

## Obsidian 写入规范

- 附件命名：`图-<知识点>-<用途>.svg` 与同名 `.png`。
- SVG 存在附件目录作为源图；Markdown 正文嵌入 PNG：`![[.../图名.png]]`。
- 图注使用普通 callout：

```markdown
> [!note] 图的作用
> 说明这张图解决什么、看哪些标注、考试时得出什么结论。
```

- 原手写图只作折叠溯源，不能替代正文清晰图。
- 如果本次修改的 Markdown 含表格，完成后使用 `fix-table-pipe` 做表格检查。

## 导出脚本

用法：

```bash
scripts/render-svg-to-png.sh <input.svg> <output.png> [width] [height]
```

默认宽高为 `1600 1120`。不要依赖 `qlmanage` 作为最终导出方式；它可能把宽图裁成方图预览。

## 最终验收

运行并确认：

```bash
xmllint --noout <input.svg>
scripts/render-svg-to-png.sh <input.svg> <output.png> 1600 1120
file <output.png>
```

然后肉眼检查 PNG：四角不裁切、标题完整、导线不断、节点不悬空、颜色提示不误导。

## 可继续补充

- 给常见题型增加 SVG 模板：固定偏置共射、分压偏置共射、共集、共基、差分、运放反馈、数电门电路、触发器。
- 为微变等效图增加专门模板：`r_be`、受控源、`R_i`、`R_o` 观察端。
- 为多格对照图固定版式：原图/直流/交流/微变，或直接耦合/阻容耦合 × 直流/交流。
