# 用四则运算规则

## 基本规则

设 $\lim_{n \to \infty} x_n = a$，$\lim_{n \to \infty} y_n = b$，则：

### 加法

$$\lim_{n \to \infty} (x_n + y_n) = a + b$$

### 减法

$$\lim_{n \to \infty} (x_n - y_n) = a - b$$

### 乘法

$$\lim_{n \to \infty} (x_n \cdot y_n) = a \cdot b$$

### 除法

$$\lim_{n \to \infty} \frac{x_n}{y_n} = \frac{a}{b} \quad (b \neq 0)$$

## 推论

1. $\lim_{n \to \infty} c \cdot x_n = c \cdot a$（$c$ 为常数）
2. $\lim_{n \to \infty} x_n^k = a^k$（$k$ 为正整数）

## 使用条件

⚠️ **必须确保各部分极限都存在**

- 若 $\lim x_n$ 和 $\lim y_n$ 都存在，才能用四则运算
- 若有一个不存在，不能直接用

## 常见题型

1. 有理分式型：$\lim_{n \to \infty} \frac{a_0 n^p + \cdots}{b_0 n^q + \cdots}$
2. 根式有理化型
3. 分子分母同除最高次幂

---

<!-- UPDATE: 2026-03-09 补充典型例题和易错点 -->
## 典型例题

> [!example] 例1：有理分式型
> **题目**：求 $\lim_{n \to \infty} \frac{3n^2 + 2n + 1}{2n^2 - n + 3}$
>
> **分析**：分子分母同除最高次幂 $n^2$。
>
> **解答**：
> $$\lim_{n \to \infty} \frac{3n^2 + 2n + 1}{2n^2 - n + 3} = \lim_{n \to \infty} \frac{3 + \frac{2}{n} + \frac{1}{n^2}}{2 - \frac{1}{n} + \frac{3}{n^2}} = \frac{3 + 0 + 0}{2 - 0 + 0} = \frac{3}{2}$$

> [!example] 例2：根式有理化型
> **题目**：求 $\lim_{n \to \infty} (\sqrt{n+1} - \sqrt{n})$
>
> **分析**：分子有理化。
>
> **解答**：
> $$\lim_{n \to \infty} (\sqrt{n+1} - \sqrt{n}) = \lim_{n \to \infty} \frac{(\sqrt{n+1} - \sqrt{n})(\sqrt{n+1} + \sqrt{n})}{\sqrt{n+1} + \sqrt{n}}$$
> $$= \lim_{n \to \infty} \frac{1}{\sqrt{n+1} + \sqrt{n}} = 0$$

> [!example] 例3：无穷大与无穷小
> **题目**：求 $\lim_{n \to \infty} \frac{n!}{n^n}$
>
> **分析**：使用夹逼准则。
>
> **解答**：
> $$0 < \frac{n!}{n^n} = \frac{1 \cdot 2 \cdot \cdots \cdot n}{n \cdot n \cdot \cdots \cdot n} \leq \frac{1}{n}$$
>
> 由夹逼准则，$\lim_{n \to \infty} \frac{n!}{n^n} = 0$

## 易错点详解

> [!warning] 易错点1：使用条件
> 四则运算要求各部分极限**都存在**。
>
> **错误示例**：$\lim_{n \to \infty} (n - n) = \lim_{n \to \infty} n - \lim_{n \to \infty} n = \infty - \infty = ?$
>
> **正确做法**：$\lim_{n \to \infty} (n - n) = \lim_{n \to \infty} 0 = 0$

> [!warning] 易错点2：除法条件
> 除法要求分母极限**不为零**。
>
> 若 $\lim y_n = 0$，不能直接用除法，需用其他方法（如洛必达、等价无穷小）。

## 有理分式极限结论

> [!important] 重要结论
> 对于 $\lim_{n \to \infty} \frac{a_0 n^p + a_1 n^{p-1} + \cdots + a_p}{b_0 n^q + b_1 n^{q-1} + \cdots + b_q}$（$a_0, b_0 \neq 0$）：
>
> | 情况 | 结果 |
> |------|------|
> | $p < q$ | $0$ |
> | $p = q$ | $\frac{a_0}{b_0}$ |
> | $p > q$ | $\infty$（需讨论符号）|

## 相关知识点 📚

- [[../2-用性质/README|用性质]] - 极限的基本性质
- [[../4-用海涅定理/README|海涅定理]] - 转化为函数极限
- [[../5-用夹逼准则/README|夹逼准则]] - 无法用四则运算时的选择

## 我的理解记录 🧠

> [!personal] 初始理解
> （待填写）

<!-- END UPDATE -->
