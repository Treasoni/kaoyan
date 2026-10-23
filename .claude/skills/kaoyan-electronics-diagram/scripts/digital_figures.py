# -*- coding: utf-8 -*-
"""数字电路图元：逻辑符号块、状态图、时序波形。

用于 822 数字电子技术笔记中的标准图（触发器逻辑符号、状态图、工作波形）。
只提供绘图图元，不绑定具体知识点；调用方负责数据与布局。

约定：
- 教材风、白底、黑主线；CP 用蓝色、输入用红色、Q 用黑色。
- 波形：低电平为基线，高电平 = 基线上移 H，所有跳变画成竖直边。
- 状态图：两状态 + 自环 + 双向弧线，标签写在弧线外侧。
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.path import Path

INK = "#1a1a1a"
BLUE = "#1f5fa8"
RED = "#c0392b"
GRAY = "#8a8a8a"

_CJK_FONTS = ["STHeiti", "Heiti SC", "PingFang SC", "Songti SC", "Arial Unicode MS"]

plt.rcParams["font.sans-serif"] = _CJK_FONTS
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "dejavusans"


def new_figure(figsize, xlim, ylim):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def save(fig, path, dpi=220):
    fig.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white", pad_inches=0.12)
    plt.close(fig)


# ------------------------------------------------------------------ 波形
def step_trace(ax, base, segments, h, color=INK, lw=2.0):
    """segments: [(t_start, t_end, level)]，level 取 0/1。"""
    xs, ys = [], []
    for i, (a, b, v) in enumerate(segments):
        y = base + v * h
        if i > 0:
            xs.append(a)
            ys.append(ys[-1])
        xs.extend([a, b])
        ys.extend([y, y])
    ax.plot(xs, ys, color=color, lw=lw,
            solid_joinstyle="miter", solid_capstyle="butt")


def waveform_rows(ax, rows, h=0.62, x_left=-0.22, name_size=16):
    """rows: [(name, base_y, segments, color, lw)]"""
    for name, base, segs, color, lw in rows:
        step_trace(ax, base, segs, h, color=color, lw=lw)
        ax.text(x_left, base + h * 0.5, name, ha="right", va="center",
                fontsize=name_size, style="italic")


def edge_lines(ax, times, y_bottom, y_top, color=GRAY):
    for t in times:
        ax.plot([t, t], [y_bottom, y_top], ls=(0, (4, 3)), color=color, lw=1.0, zorder=0)


def level_marks(ax, base, h, color=GRAY, x=0.36):
    ax.text(x, base + h + 0.02, "1", ha="center", va="bottom", fontsize=8, color=color)
    ax.text(x, base - 0.02, "0", ha="center", va="top", fontsize=8, color=color)


def time_axis(ax, x_start, x_end, y, color=GRAY):
    ax.annotate("", xy=(x_end, y), xytext=(x_start, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2))
    ax.text(x_end + 0.07, y, "t", fontsize=12, color=color, va="center", style="italic")


# ------------------------------------------------------------------ 逻辑符号
def flipflop_block(ax, x0=0.0, y0=0.0, w=2.6, h=3.6,
                   inputs=(), outputs=(), top=None, bottom=None,
                   title=None, title_color=BLUE, title_size=12):
    """教材风触发器符号。

    inputs:  [(标签, y, 框内标注, 是否边沿三角[, 是否输入取反小圆圈])]
    outputs: [(标签, y, 是否取反小圆圈)]
    top/bottom: (标签, x) —— 异步端，自动加小圆圈（低电平有效）
    """
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, lw=2.0, ec=INK))

    for item in inputs:
        label, y, inner, edge = item[:4]
        bubble_in = item[4] if len(item) > 4 else False
        ax.plot([x0 - 1.0, x0], [y, y], color=INK, lw=1.8)
        if bubble_in:
            ax.add_patch(Circle((x0 - 0.09, y), 0.09, facecolor="white",
                                ec=INK, lw=1.4, zorder=3))
            ax.plot([x0 - 1.0, x0 - 0.18], [y, y], color=INK, lw=1.8)
        ax.text(x0 - 1.08, y, label, ha="right", va="center", fontsize=14)
        if inner:
            ax.text(x0 + 0.14, y, inner, ha="left", va="center", fontsize=11.5)
        if edge:
            ax.plot([x0, x0 + 0.46, x0], [y - 0.26, y, y + 0.26],
                    color=INK, lw=1.6, solid_joinstyle="miter", solid_capstyle="butt")

    for label, y, bubble in outputs:
        ax.plot([x0 + w, x0 + w + 1.0], [y, y], color=INK, lw=1.8)
        if bubble:
            ax.add_patch(Circle((x0 + w + 0.09, y), 0.09, facecolor="white",
                                ec=INK, lw=1.4, zorder=3))
            ax.plot([x0 + w + 0.18, x0 + w + 1.0], [y, y], color=INK, lw=1.8)
        ax.text(x0 + w + 1.10, y, label, ha="left", va="center", fontsize=14)

    def _async(label, x, y_edge, direction):
        sign = 1 if direction == "top" else -1
        ax.plot([x, x], [y_edge, y_edge + sign * 0.10], color=INK, lw=1.8)
        ax.add_patch(Circle((x, y_edge + sign * 0.19), 0.09, facecolor="white",
                            ec=INK, lw=1.4, zorder=3))
        ax.plot([x, x], [y_edge + sign * 0.28, y_edge + sign * 0.80], color=INK, lw=1.8)
        ax.text(x, y_edge + sign * 0.86, label, ha="center",
                va="bottom" if direction == "top" else "top", fontsize=13)

    if top:
        _async(top[0], top[1], y0 + h, "top")
    if bottom:
        _async(bottom[0], bottom[1], y0, "bottom")

    if title:
        ax.text(x0 + w / 2, y0 + h + (0.45 if not top else 1.15), title,
                ha="center", va="center", fontsize=title_size, color=title_color)


# ------------------------------------------------------------------ 状态图
def _self_loop(ax, cx, cy, r, color, dy_label):
    ang_a, ang_b = 132, 48
    p1 = (cx + r * np.cos(np.radians(ang_a)), cy + r * np.sin(np.radians(ang_a)))
    p2 = (cx + r * np.cos(np.radians(ang_b)), cy + r * np.sin(np.radians(ang_b)))
    c1 = (cx - 0.62, cy + r + 1.00)
    c2 = (cx + 0.62, cy + r + 1.00)
    path = Path([p1, c1, c2, p2],
                [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=16,
                                 lw=1.6, color=INK, shrinkA=0, shrinkB=0,
                                 joinstyle="miter", capstyle="butt"))
    ax.text(cx, cy + r + dy_label, "", ha="center")  # 占位，标签由调用方给出
    return (cx, cy + r + dy_label)


def two_state(ax, c0=(-1.35, 0.0), c1=(1.35, 0.0), r=0.55,
              state_labels=("0", "1"),
              self0=None, self1=None, fwd=None, back=None,
              fwd_color=BLUE, back_color=RED, note=None, note_y=-1.62):
    """两状态状态图。

    self0/self1/fwd/back: (文字, 颜色) 或 None
    """
    for c, lab in ((c0, state_labels[0]), (c1, state_labels[1])):
        ax.add_patch(Circle(c, r, facecolor="white", ec=INK, lw=2.0, zorder=2))
        ax.text(c[0], c[1], lab, ha="center", va="center", fontsize=19, zorder=3)

    if self0:
        p = _self_loop(ax, c0[0], c0[1], r, self0[1], 0.98)
        ax.text(p[0], p[1], self0[0], ha="center", va="center",
                fontsize=12, color=self0[1])
    if self1:
        p = _self_loop(ax, c1[0], c1[1], r, self1[1], 0.98)
        ax.text(p[0], p[1], self1[0], ha="center", va="center",
                fontsize=12, color=self1[1])

    if fwd:
        ax.add_patch(FancyArrowPatch((c0[0] + r - 0.02, 0.12), (c1[0] - r + 0.02, 0.12),
                                     connectionstyle="arc3,rad=-0.18", arrowstyle="-|>",
                                     mutation_scale=17, lw=1.8, color=INK,
                                     shrinkA=2, shrinkB=2))
        ax.text(0.0, 0.40, fwd[0], ha="center", va="bottom",
                fontsize=12.5, color=fwd[1])
    if back:
        ax.add_patch(FancyArrowPatch((c1[0] - r + 0.02, -0.12), (c0[0] + r - 0.02, -0.12),
                                     connectionstyle="arc3,rad=-0.18", arrowstyle="-|>",
                                     mutation_scale=17, lw=1.8, color=INK,
                                     shrinkA=2, shrinkB=2))
        ax.text(0.0, -0.42, back[0], ha="center", va="top",
                fontsize=12.5, color=back[1])

    if note:
        ax.text(0, note_y, note, ha="center", va="center", fontsize=10.5, color=GRAY)
