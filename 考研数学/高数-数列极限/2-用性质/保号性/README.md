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

---

<!-- UPDATE: 2026-03-09 补充典型例题和与函数极限对比的详细说明 -->
## 典型例题

> [!example] 例1：利用保号性判定符号
> **题目**：设 $\lim_{n \to \infty} x_n = 2$，证明：存在 $N$，当 $n > N$ 时 $x_n > 1$。
>
> **证明**：
> 由保号性，若 $\lim_{n \to \infty} x_n = 2 > 1$，则存在 $N$，当 $n > N$ 时，$x_n > 1$。

> [!example] 例2：利用逆命题
> **题目**：设 $x_n > 0$ 且 $\lim_{n \to \infty} x_n = a$，判断 $a$ 的范围。
>
> **解答**：
> 由保号性的逆命题：若 $x_n > 0$，则 $a \geq 0$。
>
> 注意：$a$ 可以等于 $0$！例如 $x_n = \frac{1}{n} > 0$，但 $\lim_{n \to \infty} x_n = 0$。

> [!example] 例3：保号性的综合应用
> **题目**：设 $\lim_{n \to \infty} x_n = a > 0$，$\lim_{n \to \infty} y_n = b$，证明 $\lim_{n \to \infty} x_n y_n = ab > 0$。
>
> **证明**：
> 由保号性，存在 $N_1$，当 $n > N_1$ 时 $x_n > 0$。
>
> 由极限运算法则，$\lim_{n \to \infty} x_n y_n = ab$。
>
> 由保号性，$ab > 0$（因为 $a > 0$ 且 $b$ 为实数，需讨论 $b$ 的符号）。

## 与函数极限的详细对比

> [!warning] 重要区别
> | 对比项 | 数列极限 | 函数极限 |
> |--------|----------|----------|
> | 保号性表述 | 若 $\lim x_n = a > b$，则某项后 $x_n > b$ | 若 $\lim f(x) = a > b$，则某去心邻域内 $f(x) > b$ |
> | 有效范围 | 从某项起（离散点） | 某去心邻域（连续区间） |
> | 逆命题 | $x_n \geq b \Rightarrow a \geq b$ | $f(x) \geq b \Rightarrow a \geq b$ |
>
> **本质区别**：数列是离散的，函数是连续的。

## 相关知识点 📚

- [[../唯一性/README|唯一性]] - 收敛数列的另一性质
- [[../有界性/README|有界性]] - 收敛数列的第三性质
- [[../../5-用夹逼准则/README|夹逼准则]] - 保号性在不等式中的应用

## 我的理解记录 🧠

> [!personal] 初始理解
> （待填写）

<!-- END UPDATE -->
