#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""星形线（astroid）示意图：左=本体+尖点，右=切线族包络。"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def get_chinese_font():
    cands = ['Heiti TC', 'Songti SC', 'Hiragino Sans GB', 'PingFang HK',
             'STHeiti', 'Kaiti SC', 'Arial Unicode MS', 'Microsoft YaHei', 'SimHei']
    avail = [f.name for f in fm.fontManager.ttflist]
    for f in cands:
        if f in avail:
            return f
    return None


# 先应用 seaborn 主题（它会重置字体），之后再覆盖中文字体
try:
    import seaborn as sns
    sns.set_style('whitegrid')
    sns.set_context('notebook', font_scale=1.15)
except ImportError:
    plt.style.use('seaborn-v0_8-whitegrid')

font = get_chinese_font()
print('chinese font:', font)
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ([font] if font else []) + [
    'DejaVu Sans', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['mathtext.fontset'] = 'cm'

BLUE = '#2E86AB'
RED = '#E94F37'
ORANGE = '#F39C12'
GRAY = '#9AA0A6'


def setup_axes(ax, lim):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#333333')
    ax.spines['bottom'].set_color('#333333')
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect('equal')
    ax.set_xlabel('x', loc='right', fontsize=13)
    ax.set_ylabel('y', loc='top', fontsize=13, rotation=0)


a = 1.0
t = np.linspace(0, 2 * np.pi, 3000)
x = a * np.cos(t) ** 3
y = a * np.sin(t) ** 3
th = np.linspace(0, 2 * np.pi, 600)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 6.0))
plt.subplots_adjust(wspace=0.22)

# ---- 左图：星形线本体 ----
setup_axes(ax1, 1.38)
ax1.plot(a * np.cos(th), a * np.sin(th), '--', color=GRAY, lw=1.1,
         alpha=0.75, label='外接圆 $x^2+y^2=a^2$')
ax1.plot(0.5 * a * np.cos(th), 0.5 * a * np.sin(th), ':', color=ORANGE,
         lw=1.5, alpha=0.95, label='内切圆 $x^2+y^2=(a/2)^2$')
ax1.plot(x, y, color=BLUE, lw=3.2, label='星形线', zorder=5)

for cx, cy in [(a, 0), (0, a), (-a, 0), (0, -a)]:
    ax1.plot(cx, cy, 'o', color=RED, ms=9, zorder=6)

ax1.annotate('尖点 $(a,0)$', xy=(a, 0), xytext=(0.55, 0.52), fontsize=11,
             color=RED, arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))
ax1.annotate('尖点 $(0,a)$', xy=(0, a), xytext=(-1.15, 1.12), fontsize=11,
             color=RED, arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))
ax1.plot([0, a], [0, 0], color='#555555', lw=1.4, zorder=4)
ax1.text(0.47, 0.045, '$a$', fontsize=13, color='#333333', ha='center')
ax1.set_title(r'星形线：$x^{2/3}+y^{2/3}=a^{2/3}$', fontsize=14, pad=12)
ax1.legend(loc='lower left', fontsize=9.5, framealpha=0.92)

# ---- 右图：切线族包络 ----
setup_axes(ax2, 1.38)
for k in np.arange(0, 2 * np.pi, np.pi / 18):
    if abs(np.cos(k)) < 1e-6 or abs(np.sin(k)) < 1e-6:
        continue
    x0, y0 = a * np.cos(k), a * np.sin(k)
    ax2.plot([x0, 0], [0, y0], '-', color=GRAY, lw=1.0, alpha=0.5, zorder=2)

ax2.plot(x, y, color=BLUE, lw=3.2, label='星形线 = 切线族的包络', zorder=5)

k0 = np.pi / 5
x0, y0 = a * np.cos(k0), a * np.sin(k0)
ax2.plot([x0, 0], [0, y0], color=RED, lw=2.4, zorder=6,
         label='切线段长度恒为 $a$')
ax2.plot([x0, 0], [0, y0], 'o', color=RED, ms=6, zorder=7)
ax2.annotate('$(a\\cos t,\\,0)$', xy=(x0, 0), xytext=(x0 + 0.10, 0.10),
             fontsize=10.5, color=RED)
ax2.annotate('$(0,\\,a\\sin t)$', xy=(0, y0), xytext=(0.10, y0 + 0.10),
             fontsize=10.5, color=RED)
ax2.set_title('为什么是“星形”：切线被两坐标轴截出的长度恒为 $a$',
              fontsize=13, pad=12)
ax2.legend(loc='lower left', fontsize=9.5, framealpha=0.92)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'astroid-20261011.png')
fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print('saved:', out)
