# 用夹逼准则

## 定理（夹逼准则）

设 $y_n \leq x_n \leq z_n$（$n$ 充分大），若 $\lim_{n \to \infty} y_n = \lim_{n \to \infty} z_n = a$，则：

$$\lim_{n \to \infty} x_n = a$$

## 几何直观

数列 $\{x_n\}$ 被 $\{y_n\}$ 和 $\{z_n\}$ "夹"在中间，两边都趋于 $a$，中间必然也趋于 $a$。

## 使用步骤

1. **放缩**：找到不等式 $y_n \leq x_n \leq z_n$
2. **求两边极限**：计算 $\lim y_n$ 和 $\lim z_n$
3. **得出结论**：若两边极限相等，则中间极限也相等

## 常见放缩技巧

### 1. 分式型

$$\frac{n}{n+1} \leq \frac{n}{n+k} \leq \frac{n}{n} = 1$$

### 2. 和式型

对于 $x_n = \sum_{k=1}^{n} a_k$，常用：
- 最大项 × 项数 ≥ 和 ≥ 最小项 × 项数
- 积分放缩

### 3. $n$ 项和的极限

$$\sum_{k=1}^{n} f\left(\frac{k}{n}\right) \cdot \frac{1}{n} \to \int_0^1 f(x) dx$$

## 典型例题

$$\lim_{n \to \infty} \left(\frac{1}{\sqrt{n^2+1}} + \frac{1}{\sqrt{n^2+2}} + \cdots + \frac{1}{\sqrt{n^2+n}}\right)$$

## 易错点

⚠️ 放缩要适度，确保两边极限相等！

---

<!-- UPDATE: 2026-03-09 补充更多典型例题、放缩技巧详解、n项和与定积分的关系 -->
## 放缩技巧详解

### 技巧一：分母放缩

> [!tip] 原则
> - **放大分式**：减小分母 或 增大分子
> - **缩小分式**：增大分母 或 减小分子

> [!example] 示例
> 对于 $\frac{1}{\sqrt{n^2+k}}$（$k = 1, 2, \dots, n$）：
> $$\frac{1}{\sqrt{n^2+n}} \leq \frac{1}{\sqrt{n^2+k}} \leq \frac{1}{\sqrt{n^2+1}}$$

### 技巧二：和式放缩

> [!tip] 原则
> 对于 $n$ 项和 $S_n = \sum_{k=1}^{n} a_k$：
> $$n \cdot \min\{a_k\} \leq S_n \leq n \cdot \max\{a_k\}$$

> [!example] 示例
> 对于 $\sum_{k=1}^{n} \frac{1}{\sqrt{n^2+k}}$：
> $$\frac{n}{\sqrt{n^2+n}} \leq \sum_{k=1}^{n} \frac{1}{\sqrt{n^2+k}} \leq \frac{n}{\sqrt{n^2+1}}$$

### 技巧三：根式放缩

> [!tip] 常用放缩
> $$\sqrt{a+b} \leq \sqrt{a} + \sqrt{b}$$（$a, b \geq 0$）

## n项和与定积分

> [!important] 重要公式
> $$\lim_{n \to \infty} \sum_{k=1}^{n} f\left(\frac{k}{n}\right) \cdot \frac{1}{n} = \int_0^1 f(x) dx$$
>
> **本质**：将求和转化为定积分（黎曼和的极限）

> [!example] 例：用定积分求极限
> **题目**：求 $\lim_{n \to \infty} \left(\frac{1}{n+1} + \frac{1}{n+2} + \cdots + \frac{1}{n+n}\right)$
>
> **解答**：
> $$\lim_{n \to \infty} \sum_{k=1}^{n} \frac{1}{n+k} = \lim_{n \to \infty} \sum_{k=1}^{n} \frac{1}{1 + \frac{k}{n}} \cdot \frac{1}{n}$$
>
> 令 $f(x) = \frac{1}{1+x}$，则：
> $$= \int_0^1 \frac{1}{1+x} dx = \ln(1+x)\big|_0^1 = \ln 2$$

## 更多典型例题

> [!example] 例1：经典夹逼
> **题目**：求 $\lim_{n \to \infty} \left(\frac{1}{\sqrt{n^2+1}} + \frac{1}{\sqrt{n^2+2}} + \cdots + \frac{1}{\sqrt{n^2+n}}\right)$
>
> **解答**：
> 放缩：
> $$\frac{n}{\sqrt{n^2+n}} \leq S_n \leq \frac{n}{\sqrt{n^2+1}}$$
>
> 两边取极限：
> $$\lim_{n \to \infty} \frac{n}{\sqrt{n^2+n}} = \lim_{n \to \infty} \frac{1}{\sqrt{1+\frac{1}{n}}} = 1$$
> $$\lim_{n \to \infty} \frac{n}{\sqrt{n^2+1}} = \lim_{n \to \infty} \frac{1}{\sqrt{1+\frac{1}{n^2}}} = 1$$
>
> 由夹逼准则，原式 $= 1$

> [!example] 例2：利用重要结论
> **题目**：求 $\lim_{n \to \infty} \sqrt[n]{1 + 2^n + 3^n}$
>
> **解答**：
> 利用结论 $\lim_{n \to \infty} \sqrt[n]{a_1^n + a_2^n + \cdots + a_m^n} = \max\{a_1, a_2, \dots, a_m\}$
>
> 原式 $= \max\{1, 2, 3\} = 3$

## 我的理解记录 🧠

> [!personal] 初始理解
> （待填写）

## 相关知识点 📚

- [[../0-数列的概念/重要不等式]] - 放缩的基础工具
- [[../3-用四则运算规则/README|四则运算]] - 配合使用
- [[../6-用单调有界准则/README|单调有界准则]] - 另一种证明极限存在的方法

<!-- END UPDATE -->
