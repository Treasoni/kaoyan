---
tags:
  - 考研数学
  - 一元函数积分学
  - 几何应用
  - 旋转体体积
---

# 绕y轴旋转的体积

## 公式（圆柱壳法）

曲线 $y = y(x)$ 与 $x = a$，$x = b$（$0 \leqslant a < b$）及 $x$ 轴围成的曲边梯形绕 $y$ 轴旋转一周所得旋转体的体积：

$$V_y = 2\pi \int_a^b x|y(x)| \, \mathrm{d}x$$

## 推导思路（微元法）

取 $[x, x + \Delta x]$（$\Delta x > 0$），得到一个小竖条，绕 $y$ 轴旋转一周成为一个"圆柱壳"，展开为"长方体"：

$$\mathrm{d}V_y = 2\pi x|y(x)| \, \mathrm{d}x$$

> [!tip] 记忆方法
> $$V_x = \pi \int_a^b \square^2 \, \mathrm{d}x \quad \text{（往"口"里代）}$$
> $$V_y = 2\pi \int_a^b x|\square| \, \mathrm{d}x$$

> [!tip] 关键技巧
> 学会利用反函数，将绕 $x$ 轴旋转用 $V_y$ 的体积公式表示出来（$x$、$y$ 地位交换）

## 个人笔记

