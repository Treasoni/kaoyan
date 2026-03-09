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
