# -*- coding: utf-8 -*-
"""Draw clean timing diagrams for latch vs flip-flop (digital electronics)."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

plt.rcParams["font.sans-serif"] = ["PingFang SC", "Arial Unicode MS", "Heiti SC"]
plt.rcParams["axes.unicode_minus"] = False

OUT = "/Users/zhqznc/Documents/考研复习/考研专业课/数字电子技术/5-锁存器和触发器/assets/04-触发器的电路结构"

C_CLK = "#111111"
C_D = "#1565C0"
C_Q = "#C62828"
C_WIN = "#FFB74D"
C_EDGE = "#E53935"
C_GREY = "#666666"


def wave(ax, t, v, color, lw=2.6):
    ax.step(t, v, where="post", color=color, lw=lw, solid_capstyle="round")


def clean(ax, ylabel=None, ymin=-0.35, ymax=1.35):
    ax.set_ylim(ymin, ymax)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["0", "1"], fontsize=11, color=C_GREY)
    ax.set_xticks([])
    for s in ["top", "right", "bottom"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#BBBBBB")
    ax.tick_params(axis="y", length=0)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=13, rotation=0, labelpad=22, va="center")


def draw_ff_symbol(ax, bubble=False, note=""):
    sx, sy, w, h = 0.80, 0.26, 0.105, 0.42
    ax.add_patch(Rectangle((sx, sy), w, h, transform=ax.transAxes,
                           fill=False, lw=1.8, ec="#333333", clip_on=False))
    ax.add_patch(Polygon([[sx, sy + h * 0.70], [sx + 0.030, sy + h * 0.52],
                          [sx, sy + h * 0.34]], closed=True,
                         transform=ax.transAxes, fill=False, lw=1.6,
                         ec="#333333", clip_on=False))
    if bubble:
        ax.add_patch(Circle((sx - 0.011, sy + h * 0.52), 0.011,
                            transform=ax.transAxes, fill=True, fc="white",
                            ec="#333333", lw=1.6, clip_on=False))
    ax.text(sx + w + 0.008, sy + h * 0.84, "Q", transform=ax.transAxes,
            fontsize=11, va="center", color="#333333")
    ax.text(sx - 0.016, sy + h * 0.84, "D", transform=ax.transAxes,
            fontsize=11, va="center", ha="right", color="#333333")
    ax.text(sx - (0.032 if bubble else 0.016), sy + h * 0.52, "CP",
            transform=ax.transAxes, fontsize=9, va="center", ha="right",
            color="#333333")
    ax.text(sx + w / 2, sy - 0.055, note, transform=ax.transAxes,
            fontsize=9, ha="center", va="top", color=C_GREY)


# ============================================================
# Figure A: latch vs edge-triggered FF, same clock / same D
# ============================================================
figA, axesA = plt.subplots(3, 2, figsize=(13.6, 7.6), sharex=True,
                           gridspec_kw={"hspace": 0.16, "wspace": 0.12})

t_cp = [0, 1.5, 4.5, 7.0, 9.0, 10]
v_cp = [0, 1, 0, 1, 0, 0]
t_d = [0, 2.0, 3.0, 5.5, 8.0, 10]
v_d = [0, 1, 0, 1, 0, 0]
t_ql = [0, 1.5, 2.0, 3.0, 4.5, 7.0, 8.0, 9.0, 10]
v_ql = [0, 0, 1, 0, 0, 1, 0, 0, 0]
t_qf = [0, 1.5, 7.0, 10]
v_qf = [0, 0, 1, 1]

for col in range(2):
    ax0, ax1, ax2 = axesA[0, col], axesA[1, col], axesA[2, col]
    wave(ax0, t_cp, v_cp, C_CLK)
    wave(ax1, t_d, v_d, C_D)
    clean(ax0, "E" if col == 0 else "CP")
    clean(ax1, "D")
    clean(ax2, "Q")
    ax2.set_xlim(-0.2, 10.2)

# left: latch
axesA[0, 0].axvspan(1.5, 4.5, color=C_WIN, alpha=0.22, lw=0)
axesA[0, 0].axvspan(7.0, 9.0, color=C_WIN, alpha=0.22, lw=0)
wave(axesA[2, 0], t_ql, v_ql, C_Q)
axesA[0, 0].text(3.0, 0.55, "E = 1 整段都敏感", ha="center", va="center",
                 fontsize=12, color="#E65100", fontweight="bold")
axesA[0, 0].text(3.0, 0.20, "（采样窗口很宽）", ha="center", va="center",
                 fontsize=10.5, color="#E65100")
axesA[2, 0].annotate("D 一变，Q 立刻跟着变", xy=(2.15, 1.02), xytext=(3.6, 1.24),
                     fontsize=11, color=C_Q, va="bottom",
                     arrowprops=dict(arrowstyle="->", color=C_Q, lw=1.4))
axesA[2, 0].annotate("E = 0，锁存保持", xy=(5.7, 0.02), xytext=(5.7, 0.58),
                     fontsize=11, color=C_GREY, ha="center", va="bottom",
                     arrowprops=dict(arrowstyle="->", color=C_GREY, lw=1.2))
# (second pulse speaks for itself; keep the panel uncluttered)

# right: edge-triggered
for edge in (1.5, 7.0):
    axesA[0, 1].axvspan(edge - 0.055, edge + 0.055, color=C_EDGE, alpha=0.85, lw=0)
    axesA[0, 1].plot(edge, 0.55, "o", color=C_EDGE, ms=7, zorder=6)
wave(axesA[2, 1], t_qf, v_qf, C_Q)
axesA[0, 1].annotate("↑ 只在这一瞬间采样", xy=(1.5, 1.0), xytext=(2.05, 1.24),
                     fontsize=11.5, color=C_EDGE, fontweight="bold", va="bottom",
                     arrowprops=dict(arrowstyle="->", color=C_EDGE, lw=1.5))
axesA[0, 1].annotate("↑ 采样窗口 ≈ 0", xy=(7.0, 1.0), xytext=(7.35, 1.24),
                     fontsize=11, color=C_EDGE, va="bottom",
                     arrowprops=dict(arrowstyle="->", color=C_EDGE, lw=1.5))
axesA[2, 1].annotate("D 变了，Q 不动", xy=(3.1, 0.02), xytext=(3.5, 1.24),
                     fontsize=11, color=C_GREY, ha="center", va="bottom",
                     arrowprops=dict(arrowstyle="->", color=C_GREY, lw=1.2))
axesA[2, 1].annotate("到边沿才更新", xy=(7.02, 1.0), xytext=(7.7, 1.24),
                     fontsize=11, color=C_Q, va="bottom",
                     arrowprops=dict(arrowstyle="->", color=C_Q, lw=1.3))

axesA[0, 0].set_title("锁存器：看电平", fontsize=16, fontweight="bold",
                      color="#E65100", pad=10)
axesA[0, 1].set_title("触发器：看边沿", fontsize=16, fontweight="bold",
                      color=C_EDGE, pad=10)
figA.suptitle("同一路时钟、同一个输入 D：锁存器和触发器到底差在哪",
              fontsize=18, fontweight="bold", y=0.985)
figA.text(0.5, 0.015,
          "橙色区域 = 器件“盯着”输入的时间段；红色竖线 + 圆点 = 只在一个瞬间“看一眼”",
          ha="center", fontsize=12, color=C_GREY)
figA.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.075)
figA.savefig(f"{OUT}/采样窗口-锁存器与触发器.png", dpi=220, facecolor="white")
plt.close(figA)

# ============================================================
# Figure B: rising-edge vs falling-edge
# ============================================================
figB, axesB = plt.subplots(3, 2, figsize=(13.4, 7.2), sharex=True,
                           gridspec_kw={"hspace": 0.16, "wspace": 0.12})
t_cp2 = [0, 2.0, 6.0, 10]
v_cp2 = [0, 1, 0, 0]
t_d2 = [0, 1.0, 9.0, 10]
v_d2 = [0, 1, 0, 0]

for col, (edge_t, edge_name, q_t, color, note, chip) in enumerate([
        (2.0, "上升沿", [0, 2.0, 10], "#E53935", "无小圈", "74HC74"),
        (6.0, "下降沿", [0, 6.0, 10], "#1565C0", "加小圈", "74LS112")]):
    ax0, ax1, ax2 = axesB[0, col], axesB[1, col], axesB[2, col]
    wave(ax0, t_cp2, v_cp2, C_CLK)
    wave(ax1, t_d2, v_d2, C_D)
    wave(ax2, q_t, [0, 1, 1], C_Q)
    clean(ax0, "CP")
    clean(ax1, "D")
    clean(ax2, "Q")
    ax2.set_xlim(-0.2, 10.2)

    ax0.axvspan(edge_t - 0.055, edge_t + 0.055, color=color, alpha=0.9, lw=0)
    if col == 0:
        p_start, p_end = (edge_t, 0.02), (edge_t, 1.22)
    else:
        p_start, p_end = (edge_t, 1.22), (edge_t, 0.02)
    ax0.annotate("", xy=p_end, xytext=p_start,
                 arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4,
                                 mutation_scale=20))
    ax0.plot(edge_t, 0.55, "o", color="white", mec=color, mew=2, ms=7, zorder=6)
    ax0.text(edge_t - 0.15, 1.12, f"{edge_name}触发", ha="right", va="bottom",
             fontsize=13, color=color, fontweight="bold")
    ax0.set_title(f"{edge_name}触发（{chip}）", fontsize=15, fontweight="bold",
                  color=color, pad=8)

    ax2.annotate("Q 在这一刻更新", xy=(edge_t + 0.02, 1.0),
                 xytext=(edge_t + 1.1, 1.25), fontsize=11.5, color=C_Q,
                 va="bottom",
                 arrowprops=dict(arrowstyle="->", color=C_Q, lw=1.4))

    draw_ff_symbol(ax2, bubble=(col == 1), note=note)

figB.suptitle("边沿触发的两种极性：看 Q 在哪一条竖边上改变",
              fontsize=18, fontweight="bold", y=0.985)
figB.text(0.5, 0.015,
          "同为 D=1：上升沿触发器在 ↑ 把 Q 置 1；下降沿触发器要等到 ↓ 才置 1",
          ha="center", fontsize=12, color=C_GREY)
figB.subplots_adjust(left=0.075, right=0.985, top=0.88, bottom=0.075)
figB.savefig(f"{OUT}/触发极性-上升沿与下降沿.png", dpi=220, facecolor="white")
plt.close(figB)

# ============================================================
# Figure C: three trigger modes, sampling window comparison
# ============================================================
figC, axesC = plt.subplots(3, 1, figsize=(13.2, 7.6),
                           gridspec_kw={"hspace": 0.46})
t_cp3 = [0, 2.0, 6.0, 10]
v_cp3 = [0, 1, 0, 0]

modes = [
    ("电平触发（锁存器）", "#E65100", "wide", "latch"),
    ("脉冲触发（主从结构）", "#6A1B9A", "wide", "pulse"),
    ("边沿触发（现代触发器）", "#C62828", "narrow", "edge"),
]
for ax, (title, color, win_kind, kind) in zip(axesC, modes):
    wave(ax, t_cp3, v_cp3, C_CLK)
    ax.set_xlim(-0.2, 10.2)
    clean(ax, "CP", ymin=-0.62, ymax=1.35)
    ax.set_title(title, fontsize=14.5, fontweight="bold", color=color,
                 loc="left", pad=6)

    if win_kind == "wide":
        ax.axvspan(2.0, 6.0, color=C_WIN, alpha=0.25, lw=0)
        ax.annotate("", xy=(2.0, -0.22), xytext=(6.0, -0.22),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=2.0))
        ax.text(4.0, -0.34, "采样窗口：整个高电平（很宽）", ha="center",
                va="top", fontsize=11, color=color)
    else:
        ax.axvspan(2.0 - 0.055, 2.0 + 0.055, color=color, alpha=0.9, lw=0)
        ax.annotate("", xy=(2.0, 1.18), xytext=(2.0, 0.05),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2,
                                    mutation_scale=18))
        ax.plot(2.0, 0.55, "o", color="white", mec=color, mew=2, ms=7, zorder=6)
        ax.text(2.25, -0.34, "采样窗口 ≈ 0（只有一条竖线）", fontsize=11,
                color=color, va="top")

    if kind == "latch":
        ax.text(4.0, 0.55, "Q 在窗口内随时更新", fontsize=11.5, color=color,
                ha="center", va="center", fontweight="bold")
    elif kind == "pulse":
        ax.plot([6.0, 6.0], [0.02, 1.0], ls=(0, (4, 3)), color=color, lw=1.5)
        ax.plot(6.0, 0.5, "o", color=color, ms=8, zorder=6, mec="white", mew=1.2)
        ax.text(6.48, 0.66, "Q 只在 ↓ 统一更新", fontsize=11.5, color=color,
                fontweight="bold", va="center")
    else:
        ax.plot(2.0, 0.5, "o", color=color, ms=8, zorder=6, mec="white", mew=1.2)
        ax.text(2.3, 0.66, "采样 + 更新都在这一刻", fontsize=11.5, color=color,
                fontweight="bold", va="center")

figC.suptitle("三种触发方式：只看“采样窗口”是宽还是窄",
              fontsize=18, fontweight="bold", y=0.985)
figC.text(0.5, 0.015,
          "宽窗口 = 抗干扰弱；窄窗口 = 抗干扰强。主从结构窗口仍很宽，所以它属于脉冲触发而不是边沿触发",
          ha="center", fontsize=11.5, color=C_GREY)
figC.subplots_adjust(left=0.075, right=0.985, top=0.86, bottom=0.10)
figC.savefig(f"{OUT}/三种触发方式-采样窗口对比.png", dpi=220, facecolor="white")
plt.close(figC)

print("done")
