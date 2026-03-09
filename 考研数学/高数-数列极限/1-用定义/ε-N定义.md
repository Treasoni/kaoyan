---
知识点: ε-N定义
模块: 高数-数列极限
考试类型: 数二
考试频率: ⭐
学习状态: 待学习
tags: [高数, 数列极限, 了解即可]
---

# ε-N 定义

> [!warning] 考试提醒
> ⚠️ **卷面上不考**：用 $\varepsilon$-$N$ 定义证明极限在考研数学中基本不考查，了解即可。

## 定义

> [!def] 数列极限的 $\varepsilon$-$N$ 定义
> 设 $\{x_n\}$ 为一数列，若存在常数 $a$，对于**任意** $\varepsilon > 0$，**总存在**正整数 $N$，使得当 $n > N$ 时，
>
> $$|x_n - a| < \varepsilon$$
>
> **恒成立**，则称：
> - $a$ 是数列 $\{x_n\}$ 的**极限**
> - 数列 $\{x_n\}$ **收敛**于 $a$
> - 记为 $\lim_{n \to \infty} x_n = a$ 或 $x_n \to a$（$n \to \infty$）

## 定义的逻辑结构

| 符号 | 含义 | 作用 |
|------|------|------|
| $\forall \varepsilon > 0$ | 任意给定的正数（无论多小） | 表示"任意接近" |
| $\exists N \in \mathbf{N}_{+}$ | 存在一个正整数 $N$ | 表示"从某项开始" |
| $n > N \Rightarrow |x_n - a| < \varepsilon$ | 当 $n$ 足够大时，$x_n$ 与 $a$ 的距离小于 $\varepsilon$ | 表示"无限接近" |

## 几何解释

> [!info] 几何意义
> 对于任意给定的 $\varepsilon > 0$，无论多么小，都能找到正整数 $N$，使得数列 $\{x_n\}$ 从第 $N+1$ 项开始，所有项都落在 $(a-\varepsilon, a+\varepsilon)$ 这个开区间内。
>
> 也就是说，在 $a$ 的任意 $\varepsilon$ 邻域外，只有**有限多项**。

## 理解要点

> [!tip] 核心理解
> 1. **$\varepsilon$ 是任意的**：表示 $x_n$ 可以任意接近 $a$
> 2. **$N$ 依赖于 $\varepsilon$**：$\varepsilon$ 越小，需要的 $N$ 通常越大
> 3. **关注的是"充分大"**：前有限项不影响极限

## 与其他表述的等价形式

以下说法等价：

1. $\lim_{n \to \infty} x_n = a$
2. $\forall \varepsilon > 0, \exists N, \text{当 } n > N \text{ 时}, |x_n - a| < \varepsilon$
3. $\forall \varepsilon > 0, \text{只有有限多个 } x_n \text{ 满足 } |x_n - a| \geq \varepsilon$

## 简单例子

> [!example] 例：用定义证明 $\lim_{n \to \infty} \frac{1}{n} = 0$
>
> **分析**：需要找到 $N$，使得当 $n > N$ 时，$|\frac{1}{n} - 0| = \frac{1}{n} < \varepsilon$。
>
> **解答**：
> 对于任意 $\varepsilon > 0$，要使 $\frac{1}{n} < \varepsilon$，只需 $n > \frac{1}{\varepsilon}$。
>
> 取 $N = \lfloor \frac{1}{\varepsilon} \rfloor$（向下取整），则当 $n > N$ 时，$|\frac{1}{n} - 0| < \varepsilon$。
>
> 因此 $\lim_{n \to \infty} \frac{1}{n} = 0$。

## 与发散的关系

> [!def] 发散的表述
> 数列 $\{x_n\}$ 发散 $\Leftrightarrow$ 对于任意实数 $a$，都存在 $\varepsilon > 0$，使得对任意 $N$，都存在 $n > N$ 满足 $|x_n - a| \geq \varepsilon$

## 学习建议

> [!tip] 了解程度
> 对于考研，只需要：
> 1. **理解定义的含义**：知道什么是极限
> 2. **能看懂简单证明**：如 $\lim_{n \to \infty} \frac{1}{n} = 0$
> 3. **不必掌握复杂证明技巧**

## 相关知识点

- [[../0-数列的概念/数列的定义]] - 数列的基本概念
- [[../2-用性质/唯一性/README|唯一性]] - 用定义证明唯一性
- [[../4-用海涅定理/海涅定理]] - 函数极限的 $\varepsilon$-$\delta$ 定义与数列极限的关系

---

*创建日期: 2026-03-09*
