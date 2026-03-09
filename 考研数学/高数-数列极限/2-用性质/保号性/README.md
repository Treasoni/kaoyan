# 保号性

## 定理

若 $\lim_{n \to \infty} x_n = a > 0$（或 $a < 0$），则 $\exists N$，当 $n > N$ 时，$x_n > 0$（或 $x_n < 0$）。

## 逆命题

若 $\exists N$，当 $n > N$ 时 $x_n \geq 0$，且 $\lim_{n \to \infty} x_n = a$，则 $a \geq 0$。

> [!warning] 注意不等号的变化
> 原命题：$a > 0 \Rightarrow x_n > 0$
> 逆命题：$x_n \geq 0 \Rightarrow a \geq 0$

## 与函数极限的对比

| 对比项 | 数列极限 | 函数极限 |
|--------|----------|----------|
| 保号性 | $a > 0 \Rightarrow x_n > 0$ ($n > N$) | $a > 0 \Rightarrow f(x) > 0$ ($x$ 在某去心邻域) |
| 逆命题 | $x_n \geq 0 \Rightarrow a \geq 0$ | $f(x) \geq 0 \Rightarrow a \geq 0$ |

## 应用

- 判定极限的符号
- 证明不等式

## 易错点

⚠️ 逆命题中不等号可能取等！例如 $x_n = \frac{1}{n} > 0$，但 $\lim_{n \to \infty} x_n = 0$。
