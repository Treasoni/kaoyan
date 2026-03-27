# kaoyan-electronics-circuit 代码模块

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

---

## 概述

本文件提供 kaoyan-electronics-circuit 技能的代码实现逻辑，包括电路图识别、参数提取、分析流程选择、输出生成等核心功能。

---

## 核心依赖

```python
from typing import Dict, List, Optional, Tuple
from enum import Enum
```

---

## 主入口 API

### 1. 电路分析处理器

```python
class CircuitType(Enum):
    """电路类型枚举"""
    # 模电类型
    CE_AMPLIFIER = "共射放大"
    CC_AMPLIFIER = "共集放大"
    CB_AMPLIFIER = "共基放大"
    DIFFERENTIAL = "差分放大"
    FEEDBACK = "反馈放大"
    OPAMP = "运算电路"
    POWER_AMP = "功率放大"
    OSCILLATOR = "振荡电路"
    POWER_SUPPLY = "稳压电源"

    # 数电类型
    COMBINATIONAL = "组合逻辑"
    SEQUENTIAL = "时序逻辑"
    COUNTER = "计数器"
    SHIFT_REGISTER = "移位寄存器"


def process_circuit_analysis(
    image_source: str = None,
    text_description: str = None,
    analysis_type: str = "full"
) -> Dict:
    """
    处理电路分析请求的主入口。

    参数:
        image_source: 电路图图片路径/URL
        text_description: 文字描述
        analysis_type: 分析类型 (static/dynamic/full)

    返回:
        {
            "circuit_type": CircuitType,
            "components": Dict,
            "static_analysis": Dict,
            "dynamic_analysis": Dict,
            "output_markdown": str
        }
    """
    # 1. 识别电路
    circuit_info = identify_circuit(image_source, text_description)

    # 2. 提取元件参数
    components = extract_components(circuit_info)

    # 3. 选择分析流程
    analyzer = select_analyzer(circuit_info["type"])

    # 4. 执行分析
    result = analyzer.analyze(components, analysis_type)

    # 5. 生成输出
    return generate_output(result)
```

---

## 电路识别

### MCP 工具调用

```python
def identify_circuit(image_source: str = None, text_description: str = None) -> Dict:
    """
    使用 MCP 工具识别电路结构。

    优先级:
    1. 如果有图片，使用 understand_technical_diagram
    2. 如果只有文字，使用文字解析
    """

    if image_source:
        # 调用 MCP 工具识别电路图
        return {
            "method": "mcp_understand_technical_diagram",
            "tool": "mcp__zai-mcp-server__understand_technical_diagram",
            "params": {
                "image_source": image_source,
                "prompt": "识别这个电路图的类型、元件、连接关系",
                "diagram_type": "circuit"
            }
        }
    else:
        # 文字描述解析
        return parse_text_circuit(text_description)


def extract_components(circuit_info: Dict) -> Dict:
    """
    提取电路元件参数。

    如果有图片，使用 MCP OCR 工具提取参数。
    """

    if circuit_info.get("has_image"):
        return {
            "method": "mcp_extract_text",
            "tool": "mcp__zai-mcp-server__extract_text_from_screenshot",
            "params": {
                "image_source": circuit_info["image_source"],
                "prompt": "提取电路中的元件参数（电阻、电容、晶体管等）"
            }
        }
    else:
        return parse_component_values(circuit_info.get("text", ""))
```

---

## 分析器选择

```python
def select_analyzer(circuit_type: CircuitType):
    """根据电路类型选择分析器"""

    ANALYZERS = {
        # 模电分析器
        CircuitType.CE_AMPLIFIER: CEAmplifierAnalyzer,
        CircuitType.CC_AMPLIFIER: CCAmplifierAnalyzer,
        CircuitType.CB_AMPLIFIER: CBAmplifierAnalyzer,
        CircuitType.DIFFERENTIAL: DifferentialAnalyzer,
        CircuitType.FEEDBACK: FeedbackAnalyzer,
        CircuitType.OPAMP: OpAmpAnalyzer,

        # 数电分析器
        CircuitType.COMBINATIONAL: CombinationalAnalyzer,
        CircuitType.SEQUENTIAL: SequentialAnalyzer,
        CircuitType.COUNTER: CounterAnalyzer,
    }

    return ANALYZERS.get(circuit_type, GenericAnalyzer)()
```

---

## 模电分析器

### 共射放大电路分析器

```python
class CEAmplifierAnalyzer:
    """共射放大电路分析器"""

    def analyze(self, components: Dict, analysis_type: str = "full") -> Dict:
        result = {}

        if analysis_type in ["static", "full"]:
            result["static"] = self.static_analysis(components)

        if analysis_type in ["dynamic", "full"]:
            result["dynamic"] = self.dynamic_analysis(components)

        return result

    def static_analysis(self, c: Dict) -> Dict:
        """
        静态分析 - 计算静态工作点Q

        使用康华光符号体系
        """
        Vcc = c.get("Vcc", 12)
        Rb = c.get("Rb", 200e3)
        Rc = c.get("Rc", 3e3)
        beta = c.get("beta", 50)
        Ubeq = 0.7  # 硅管

        # 基极静态电流
        I_bq = (Vcc - Ubeq) / Rb

        # 集电极静态电流
        I_cq = beta * I_bq

        # 集射极静态电压
        U_ceq = Vcc - I_cq * Rc

        return {
            "I_BQ": I_bq,
            "I_CQ": I_cq,
            "U_CEQ": U_ceq,
            "check_amplification": U_ceq > 0.3  # 检查放大区
        }

    def dynamic_analysis(self, c: Dict) -> Dict:
        """
        动态分析 - 计算增益、输入/输出电阻
        """
        beta = c.get("beta", 50)
        I_eq = c.get("I_CQ", 2e-3)  # 近似 I_EQ ≈ I_CQ
        Rc = c.get("Rc", 3e3)
        Rl = c.get("Rl", 3e3)
        Rb = c.get("Rb", 200e3)
        r_bb = 200  # 基区体电阻

        # BJT 输入电阻
        r_be = r_bb + (1 + beta) * 26e-3 / I_eq

        # 等效负载电阻
        R_l_prime = (Rc * Rl) / (Rc + Rl)

        # 电压增益
        A_u = -beta * R_l_prime / r_be

        # 输入电阻
        R_i = (Rb * r_be) / (Rb + r_be)

        # 输出电阻
        R_o = Rc

        return {
            "r_be": r_be,
            "R_L_prime": R_l_prime,
            "A_u": A_u,
            "R_i": R_i,
            "R_o": R_o
        }
```

---

## 数电分析器

### 时序逻辑分析器

```python
class SequentialAnalyzer:
    """时序逻辑电路分析器"""

    def analyze(self, components: Dict, analysis_type: str = "full") -> Dict:
        return {
            "drive_equations": self.get_drive_equations(components),
            "state_equations": self.get_state_equations(components),
            "output_equations": self.get_output_equations(components),
            "state_table": self.generate_state_table(components),
            "state_diagram": self.generate_state_diagram(components),
            "self_start_check": self.check_self_starting(components)
        }

    def get_drive_equations(self, c: Dict) -> List[str]:
        """获取驱动方程"""
        # J-K 触发器示例
        return [
            "J_1 = X · Q_0^n",
            "K_1 = X + Q_0^n",
            "J_0 = \\overline{Q_1^n}",
            "K_0 = Q_1^n"
        ]

    def get_state_equations(self, c: Dict) -> List[str]:
        """获取状态方程"""
        return [
            "Q_1^{n+1} = J_1 \\overline{Q_1^n} + \\overline{K_1} Q_1^n",
            "Q_0^{n+1} = J_0 \\overline{Q_0^n} + \\overline{K_0} Q_0^n"
        ]

    def generate_state_table(self, c: Dict) -> str:
        """生成状态转换表（Markdown格式）"""
        return """
| $X$ | $Q_1^n Q_0^n$ | $Q_1^{n+1} Q_0^{n+1}$ | $Y$ |
|-----|--------------|---------------------|-----|
| 0 | 00 | 01 | 0 |
| 0 | 01 | 00 | 0 |
| 0 | 10 | 00 | 1 |
| 0 | 11 | 00 | 1 |
| 1 | 00 | 11 | 0 |
| 1 | 01 | 10 | 0 |
| 1 | 10 | 01 | 1 |
| 1 | 11 | 10 | 1 |
"""

    def generate_state_diagram(self, c: Dict) -> str:
        """生成状态转换图（Mermaid格式）"""
        return """```mermaid
stateDiagram-v2
    direction LR
    S0 --> S1: X=0
    S1 --> S0: X=0
    S0 --> S3: X=1
    S3 --> S2: X=1
    S2 --> S1: X=1
    S1 --> S2: X=1
```"""

    def check_self_starting(self, c: Dict) -> Dict:
        """检查自启动能力"""
        return {
            "all_states_reachable": True,
            "invalid_states": [],
            "can_enter_valid_cycle": True
        }
```

---

## 输出生成器

### 模电输出格式

```python
def generate_modian_output(result: Dict) -> str:
    """生成模电分析 Markdown 输出"""

    circuit_type = result.get("circuit_type", "电路")
    static = result.get("static", {})
    dynamic = result.get("dynamic", {})

    output = f"""# {circuit_type}分析

## 电路识别
- 类型：{circuit_type}
- 元��：{format_components(result.get('components', {}))}

## 静态分析
$$
I_{{BQ}} = \\frac{{V_{{CC}} - U_{{BEQ}}}}{{R_b}} = {static.get('I_BQ', 0)*1e6:.2f}\\mu A
$$
$$
I_{{CQ}} = \\beta I_{{BQ}} = {static.get('I_CQ', 0)*1e3:.2f}mA
$$
$$
U_{{CEQ}} = V_{{CC}} - I_{{CQ}} R_c = {static.get('U_CEQ', 0):.2f}V
$$

## 动态分析
$$
r_{{be}} = r_{{bb'}} + (1+\\beta)\\frac{{26}}{{I_{{EQ}}}} = {dynamic.get('r_be', 0)/1e3:.2f}k\\Omega
$$
$$
A_u = -\\frac{{\\beta R'_L}}{{r_{{be}}}} = {dynamic.get('A_u', 0):.1f}
$$
$$
R_i = R_b // r_{{be}} = {dynamic.get('R_i', 0)/1e3:.2f}k\\Omega
$$
$$
R_o = R_c = {dynamic.get('R_o', 0)/1e3:.2f}k\\Omega
$$

## 结论
{generate_conclusion(result)}
"""
    return output
```

### 数电输出格式

```python
def generate_shudian_output(result: Dict) -> str:
    """生成数电分析 Markdown 输出"""

    output = f"""# {result.get('circuit_type', '时序逻辑电路')}分析

## 电路识别
- 类型：{result.get('circuit_type', '时序逻辑电路')}
- 触发器类型/数量：{result.get('flipflops', 'N/A')}
- 输入输出：{result.get('io', 'N/A')}

## 驱动方程
$$
{result.get('drive_equations', ['N/A'])[0]}
$$

## 状态方程
$$
{result.get('state_equations', ['N/A'])[0]}
$$

## 状态转换表
{result.get('state_table', 'N/A')}

## 状态转换图
{result.get('state_diagram', 'N/A')}

## 自启动检查
- 无效状态：{result.get('self_start_check', {}).get('invalid_states', '无')}
- 能否进入有效循环：{'是' if result.get('self_start_check', {}).get('can_enter_valid_cycle', False) else '否'}

## 结论
{result.get('conclusion', '功能描述')}
"""
    return output
```

---

## 康华光符号强制

```python
# 康华光符号体系（circuit 模块）
KANG_SYMBOLS_CIRCUIT = {
    # 静态工作点
    "I_BQ": "I_{BQ}",
    "I_CQ": "I_{CQ}",
    "U_CEQ": "U_{CEQ}",
    "U_BEQ": "U_{BEQ}",

    # 动态参数
    "r_be": "r_{be}",
    "r_ce": "r_{ce}",
    "A_u": "A_u",
    "R_i": "R_i",
    "R_o": "R_o",

    # FET参数
    "U_GS_off": "U_{GS(off)}",
    "U_GS_th": "U_{GS(th)}",
    "I_DSS": "I_{DSS}",
    "g_m": "g_m",
}


def validate_kang_symbol(symbol: str) -> str:
    """验证并返回康华光符号"""
    return KANG_SYMBOLS_CIRCUIT.get(symbol, symbol)


def format_equation_kang(equation: str) -> str:
    """将公式中的符号转换为康华光符号"""
    for old, new in KANG_SYMBOLS_CIRCUIT.items():
        equation = equation.replace(old, new)
    return equation
```

---

## MCP 工具集成

```python
# MCP 工具调用配置
MCP_TOOLS = {
    "understand_diagram": {
        "tool": "mcp__zai-mcp-server__understand_technical_diagram",
        "usage": "识别电路图结构"
    },
    "extract_text": {
        "tool": "mcp__zai-mcp-server__extract_text_from_screenshot",
        "usage": "提取元件参数"
    }
}


def call_mcp_tool(tool_name: str, params: Dict) -> Dict:
    """
    调用 MCP 工具的统一接口。

    实际调用时会转换为对应的 Claude Tool 调用。
    """
    tool_config = MCP_TOOLS.get(tool_name)
    if not tool_config:
        raise ValueError(f"Unknown MCP tool: {tool_name}")

    return {
        "tool": tool_config["tool"],
        "params": params
    }
```

---

## 版本信息

- **创建日期**: 2026-03-27
- **版本**: 1.1.0 (模块化重构)

> 📋 **返回主文档**: [SKILL.md](SKILL.md)
