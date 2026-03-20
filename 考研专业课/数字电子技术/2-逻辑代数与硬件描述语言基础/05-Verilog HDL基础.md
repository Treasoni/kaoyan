---
知识点: Verilog HDL基础
模块: 数字电子技术
章节: 第二章 逻辑代数与硬件描述语言基础
考试频率: ⭐⭐
学习状态: 待学习
tags:
  - 数电
  - Verilog
  - HDL
  - 硬件描述语言
---

# Verilog HDL基础（精简版）

> [!info] 概述
> Verilog HDL是一种硬件描述语言，用于描述数字系统的结构和行为。本节只需了解基本概念，详细内容将在后续章节深入学习。

> [!tip] 822考纲要求
> - 了解HDL的基本概念（仿真、综合）
> - 了解模块的基本结构
> - 了解三种描述方式的概念
> - **不要求详细语法**

---

## 一、HDL的基本概念

### 1.1 什么是HDL

> [!def] 硬件描述语言（HDL）
> HDL（Hardware Description Language）是一种以**文本形式**描述数字系统硬件结构和功能的语言。

**两种标准HDL**：
- **Verilog HDL**（本课程采用）
- VHDL

### 1.2 HDL的两大应用

> [!important] HDL的两个核心应用

| 应用 | 说明 | 输出 |
|:----:|:----:|:----:|
| **逻辑仿真** | 用软件验证电路逻辑功能是否正确 | 波形图、文本结果 |
| **逻辑综合** | 将HDL代码转换为实际硬件电路 | 门级网表 |

```
HDL代码 ──→ 仿真器 ──→ 仿真结果（验证功能）
       │
       └──→ 综合器 ──→ 门级网表（实现电路）
```

---

## 二、Verilog的四种逻辑值

> [!def] Verilog的四种基本逻辑值

| 逻辑值 | 含义 | 说明 |
|:------:|:----:|:----:|
| **0** | 逻辑0、低电平 | 假 |
| **1** | 逻辑1、高电平 | 真 |
| **x** 或 **X** | 不定态（未知） | 仿真时出现，可能是0或1 |
| **z** 或 **Z** | 高阻态 | 开路状态 |

> [!note] 实际硬件
> 实际电路中只有0和1，x和z主要用于仿真阶段。

---

## 三、变量数据类型 ⭐

### 3.1 线网类型（wire）

> [!def] wire类型
> 表示硬件电路中的**连线**，其值由驱动它的元件决定。

```verilog
wire a, b;           // 声明两个1位线网
wire [7:0] databus;  // 声明8位线网（数据总线）
wire [31:0] data;    // 声明32位线网
```

**特点**：
- 默认值：**高阻态 z**
- 用于连续赋值（assign）
- 模块端口默认为wire类型

### 3.2 寄存器类型（reg）

> [!def] reg类型
> 表示**数据存储单元**，具有状态保持功能。

```verilog
reg clock;           // 声明1位寄存器
reg [3:0] counter;   // 声明4位寄存器
reg [7:0] mem [0:255]; // 声明256×8位存储器
```

**特点**：
- 默认值：**不定态 x**
- 只能在initial或always块中赋值
- 用于行为描述

### 3.3 wire与reg的区别 ⭐

| 特性 | wire | reg |
|:----:|:----:|:---:|
| 物理意义 | 连线 | 存储 |
| 默认值 | z | x |
| 赋值方式 | assign | always/initial |
| 综合结果 | 组合逻辑 | 组合或时序逻辑 |

---

## 四、模块的基本结构

> [!def] 模块（module）
> 模块是Verilog描述电路的基本单元，可以表示简单门电路或复杂系统。

### 4.1 模块结构

```verilog
module 模块名(端口列表);
    // 端口类型说明
    input  [位宽] 端口名;
    output [位宽] 端口名;
    inout  [位宽] 端口名;

    // 数据类型定义
    wire [位宽] 信号名;
    reg  [位宽] 信号名;

    // 逻辑功能描述
    // (三种描述方式之一或组合)

endmodule
```

### 4.2 简单示例

```verilog
module mux2to1(
    input  D0, D1, S,  // 输入端口
    output Y           // 输出端口
);
    // 功能描述
    assign Y = S ? D1 : D0;  // 三目运算符
endmodule
```

---

## 五、三种描述方式 ⭐

> [!important] Verilog的三种描述方式

### 5.1 门级描述方式（结构化描述）

直接调用Verilog内置的基本门级元件。

```verilog
module mux2to1_gate(D0, D1, S, Y);
    input  D0, D1, S;
    output Y;
    wire   Snot, A, B;

    // 调用基本门级元件
    not  U1(Snot, S);    // 非门
    and  U2(A, D0, Snot); // 与门
    and  U3(B, D1, S);    // 与门
    or   U4(Y, A, B);     // 或门
endmodule
```

**内置门级元件**：
- `and`, `nand`, `or`, `nor`, `xor`, `xnor`（多输入门）
- `buf`, `not`（多输出门）
- `bufif1`, `bufif0`, `notif1`, `notif0`（三态门）

### 5.2 数据流描述方式

使用**连续赋值语句（assign）**描述电路功能。

```verilog
module mux2to1_dataflow(D0, D1, S, Y);
    input  D0, D1, S;
    output Y;
    wire   Y;

    // 连续赋值语句
    assign Y = (~S & D0) | (S & D1);
    // 或：assign Y = S ? D1 : D0;
endmodule
```

**特点**：
- 使用 `assign` 关键字
- 左边必须是wire类型
- 适合组合逻辑电路

### 5.3 行为描述方式

使用**过程块（always）**和高级语句描述电路行为。

```verilog
module mux2to1_behavior(D0, D1, S, Y);
    input  D0, D1, S;
    output Y;
    reg    Y;  // 注意：左边必须是reg类型

    // 过程块
    always @(D0 or D1 or S)
    begin
        if (S == 1)
            Y = D1;
        else
            Y = D0;
    end
endmodule
```

**特点**：
- 使用 `always` 关键字
- 左边必须是reg类型
- 更抽象，不涉及具体电路结构

### 5.4 三种方式对比

| 描述方式 | 关键字 | 特点 | 适用场景 |
|:--------:|:------:|:----:|:--------:|
| 门级 | and/or/not | 最接近电路 | 简单门电路 |
| 数据流 | assign | 简洁直观 | 组合逻辑 |
| 行为 | always | 抽象灵活 | 复杂逻辑、时序电路 |

---

## 六、常用运算符

### 6.1 位运算符

| 运算符 | 含义 | 示例 |
|:------:|:----:|:----:|
| `~` | 按位取反 | `~A` |
| `&` | 按位与 | `A & B` |
| `\|` | 按位或 | `A \| B` |
| `^` | 按位异或 | `A ^ B` |
| `~^` 或 `^~` | 按位同或 | `A ~^ B` |

### 6.2 逻辑运算符

| 运算符 | 含义 | 示例 |
|:------:|:----:|:----:|
| `!` | 逻辑非 | `!A` |
| `&&` | 逻辑与 | `A && B` |
| `\|\|` | 逻辑或 | `A \|\| B` |

### 6.3 缩位运算符

> [!note] 缩位运算
> 对单个操作数的所有位进行运算，结果是**1位**。

```verilog
reg [3:0] A = 4'b1010;

&A;     // 缩位与 = 1&0&1&0 = 0
|A;     // 缩位或 = 1|0|1|0 = 1
^A;     // 缩位异或 = 1^0^1^0 = 0
```

### 6.4 条件运算符

```verilog
Y = S ? D1 : D0;  // 如果S为1，Y=D1；否则Y=D0
```

---

## 七、简单综合示例

> [!example] 2选1数据选择器的完整Verilog代码

```verilog
// 方式1：数据流描述
module mux2to1(
    input  D0, D1, S,
    output Y
);
    assign Y = (S) ? D1 : D0;
endmodule

// 方式2：行为描述
module mux2to1(
    input  D0, D1, S,
    output reg Y
);
    always @(*)
        Y = S ? D1 : D0;
endmodule

// 方式3：门级描述
module mux2to1(
    input  D0, D1, S,
    output Y
);
    wire Snot, A, B;
    not  (Snot, S);
    and  (A, D0, Snot);
    and  (B, D1, S);
    or   (Y, A, B);
endmodule
```

---

## 八、小结

> [!summary] 本章要点
> 1. **HDL用途**：逻辑仿真 + 逻辑综合
> 2. **四种逻辑值**：0、1、x、z
> 3. **两种数据类型**：wire（连线）、reg（存储）
> 4. **模块结构**：module...endmodule
> 5. **三种描述方式**：门级、数据流(assign)、行为(always)

---

## 相关知识点 📚

- [[考研专业课/数字电子技术/4-组合逻辑电路/|第四章：组合逻辑电路]]（详细Verilog设计）
- [[考研专业课/数字电子技术/5-锁存器和触发器/|第五章：锁存器和触发器]]（时序电路Verilog）

---

*创建日期: 2026-03-20*
