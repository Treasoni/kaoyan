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

在 $x$ 轴上取微小区间 $[x, x + \Delta x]$（$\Delta x > 0$），对应的小竖条绕 $y$ 轴旋转一周形成一个**圆柱壳**（Shell）：

![](assets/绕y轴旋转/file-20260411112913007.png)

将圆柱壳"展开"为一个**长方体薄片**，其三个维度为：

| 维度    | 几何含义    | 对应量           |      |     |
| ----- | ------- | ------------- | ---- | --- |
| 长     | 圆柱壳底面周长 | $2\pi x$      |      |     |
| 宽     | 圆柱壳高度   | $             | y(x) | $   |
| 高（厚度） | 圆柱壳壁厚   | $\mathrm{d}x$ |      |     |

![](assets/绕y轴旋转/file-20260411112921879.png)

因此体积微元为：

$$\mathrm{d}V_y = \underbrace{2\pi x}_{\text{周长}} \cdot \underbrace{|y(x)|}_{\text{高度}} \cdot \underbrace{\mathrm{d}x}_{\text{厚度}}$$

对 $x$ 从 $a$ 到 $b$ 积分即得总体积。

> [!tip] 记忆方法
> $$V_x = \pi \int_a^b \square^2 \, \mathrm{d}x \quad \text{（往"口"里代）}$$
> $$V_y = 2\pi \int_a^b x|\square| \, \mathrm{d}x$$

> [!tip] 关键技巧
> 学会利用反函数，将绕 $x$ 轴旋转用 $V_y$ 的体积公式表示出来（$x$、$y$ 地位交换）

## 个人笔记

