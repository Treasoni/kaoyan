#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微分概念的几何图示
展示 Δy（真实增量）和 dy（微分）的区别
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8), dpi=150)

# 定义函数 f(x) = x^2（或其他曲线）
def f(x):
    return 0.5 * x**2

# 导数 f'(x) = x
def f_prime(x):
    return x

# 设置参数
x0 = 2  # 起始点
delta_x = 1.5  # 增量
x1 = x0 + delta_x  # 终点

# 计算关键点的 y 值
y0 = f(x0)
y1 = f(x1)
dy = f_prime(x0) * delta_x  # 微分（切线增量）

# 绘制曲线
x_curve = np.linspace(0, 5, 200)
y_curve = f(x_curve)
ax.plot(x_curve, y_curve, 'b-', linewidth=2.5, label=r'$y = f(x)$', zorder=3)

# 绘制切线
x_tangent = np.linspace(0.5, 5, 100)
y_tangent = f(x0) + f_prime(x0) * (x_tangent - x0)
ax.plot(x_tangent, y_tangent, 'g--', linewidth=1.8, label=r'切线', zorder=2)

# 绘制关键点
# P: 起点
ax.plot(x0, y0, 'ko', markersize=10, zorder=5)
ax.annotate(r'$P(x_0, f(x_0))$', xy=(x0, y0), xytext=(x0-0.8, y0-0.8),
            fontsize=12, ha='center')

# P': 曲线上的真实终点
ax.plot(x1, y1, 'bo', markersize=10, zorder=5)
ax.annotate(r"$P'$", xy=(x1, y1), xytext=(x1+0.3, y1),
            fontsize=14, ha='left', fontweight='bold')

# Q: 切线上的点
y_q = y0 + dy
ax.plot(x1, y_q, 'go', markersize=10, zorder=5)
ax.annotate(r'$Q$', xy=(x1, y_q), xytext=(x1+0.3, y_q),
            fontsize=14, ha='left', fontweight='bold')

# 绘制 Δy（真实增量）- 垂直线从 Q 到 P'
ax.annotate('', xy=(x1, y1), xytext=(x1, y_q),
            arrowprops=dict(arrowstyle='<->', color='red', lw=2.5))
ax.text(x1 + 0.15, (y1 + y_q)/2, r'$\Delta y$', fontsize=14, color='red',
        fontweight='bold', va='center')

# 绘制 dy（微分）- 垂直线从 P 到 Q
ax.annotate('', xy=(x1, y_q), xytext=(x1, y0),
            arrowprops=dict(arrowstyle='<->', color='purple', lw=2.5))
ax.text(x1 - 0.25, (y_q + y0)/2, r'$dy$', fontsize=14, color='purple',
        fontweight='bold', va='center', ha='right')

# 绘制 Δx（水平增量）
ax.annotate('', xy=(x1, y0-0.3), xytext=(x0, y0-0.3),
            arrowprops=dict(arrowstyle='<->', color='orange', lw=2))
ax.text((x0+x1)/2, y0-0.7, r'$\Delta x$', fontsize=13, color='orange',
        ha='center', fontweight='bold')

# 绘制 o(Δx) 误差标注 - 从 Q 到 P' 的一小段
# 用虚线矩形标注
ax.annotate('', xy=(x1, y1), xytext=(x1, y_q),
            arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5,
                          linestyle=':'))

# 绘制辅助虚线
ax.plot([x0, x0], [0, y0], 'k:', linewidth=1, alpha=0.5)
ax.plot([x1, x1], [0, y1], 'k:', linewidth=1, alpha=0.5)
ax.plot([0, x1], [y0, y0], 'k:', linewidth=1, alpha=0.5)

# 标注 x₀ 和 x₀+Δx
ax.text(x0, -0.4, r'$x_0$', fontsize=12, ha='center')
ax.text(x1, -0.4, r'$x_0 + \Delta x$', fontsize=12, ha='center')

# 设置坐标轴
ax.set_xlim(-0.5, 5)
ax.set_ylim(-1, 8)
ax.set_aspect('equal')

# 绘制坐标轴（穿过原点风格）
ax.axhline(y=0, color='black', linewidth=1.5)
ax.axvline(x=0, color='black', linewidth=1.5)
ax.set_xlabel(r'$x$', fontsize=14, loc='right')
ax.set_ylabel(r'$y$', fontsize=14, loc='top', rotation=0)

# 添加图例
legend = ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

# 添加公式说明框
textstr = '\n'.join([
    r'$\Delta y = f(x_0 + \Delta x) - f(x_0)$',
    r'$dy = f''(x_0) \cdot \Delta x$',
    r'$\Delta y - dy = o(\Delta x)$'
])
props = dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.9)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)

# 设置标题
ax.set_title(r'微分的几何意义：$\Delta y$ 与 $dy$', fontsize=16, fontweight='bold', pad=15)

# 移除顶部和右侧边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置网格
ax.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()

# 保存图片
output_path = '考研数学/高数-一元微分学/一元微分学的概念/4-微分的概念/assets/differential_concept.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"图片已保存至: {output_path}")

plt.close()
