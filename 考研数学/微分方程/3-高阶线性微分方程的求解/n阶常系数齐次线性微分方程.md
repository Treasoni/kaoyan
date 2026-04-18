---
tags:
  - 考研数学
  - 微分方程
  - 高阶微分方程
---

# n 阶常系数齐次线性微分方程

## 标准形式

$$
a_n y^{(n)} + a_{n-1} y^{(n-1)} + \dots + a_1 y' + a_0 y = 0
$$

其中 $a_k$ 为常数，$a_n \neq 0$。

## 解法：特征方程法

写出特征方程 $a_n r^n + a_{n-1} r^{(n-1)} + \dots + a_1 r + a_0 = 0$，对每个特征根写出对应解：

| 特征根类型 | 对应解 |
|------------|--------|
| 单实根 $r$ | $Ce^{rx}$ |
| $k$ 重实根 $r$ | $(C_1 + C_2 x + \dots + C_k x^{k-1})e^{rx}$ |
| 单复根 $\alpha \pm \beta i$ | $e^{\alpha x}(C_1 \cos\beta x + C_2 \sin\beta x)$ |
| 二重复根 $\alpha \pm \beta i$ | $e^{\alpha x}[(C_1 + C_2 x)\cos\beta x + (C_3 + C_4 x)\sin\beta x]$ |

> 通解 = 所有特征根对应解之和

## 反求方程（重点题型）

已知解的形式，反推微分方程：

- 解含 $e^{rx}$ → $r$ 至少为单实根
- 解含 $x^{k-1}e^{rx}$ → $r$ 至少为 $k$ 重实根
- 解含 $e^{\alpha x}\cos\beta x$ 或 $e^{\alpha x}\sin\beta x$ → $\alpha \pm \beta i$ 至少为单复根
- 解含 $x e^{\alpha x}\cos\beta x$ 或 $x e^{\alpha x}\sin\beta x$ → $\alpha \pm \beta i$ 至少为二重复根

> [!tip] 反求步骤
> 1. 从解的形式提取所有特征根
> 2. 写出特征方程 $(r - r_1)(r - r_2)\dots = 0$
> 3. 展开得到微分方程
