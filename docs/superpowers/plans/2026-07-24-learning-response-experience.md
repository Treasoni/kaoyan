# 学习回答体验统一改造 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让日常学习请求先选择合适的回答模式，再进入学科流程，并把手写笔记重构变成可验证的跨科能力。

**Architecture:** 新增一个仅供各科入口调用的“学习回答契约”技能，统一定义五种回答模式、选择顺序和高风险质量门槛。新增“手写笔记重构”二级技能，数学和电子技术入口根据请求路由到它；原有笔记/电路子模块继续负责各自学科约束。回归样例只校验技能契约和用例完整性，不伪造对 LLM 内容质量的自动验证。

**Tech Stack:** Markdown skills, JSON fixtures, Python 3 standard library validation, shell `cmp` parity checks.

## Global Constraints

- 不引入 ExamPass 的 HTML、批量提取或多 Agent 流水线。
- 默认先解决当前问题，只有用户要求或确有长期价值时写入笔记/进度。
- 看不清的手写文字、参数、方向或图意必须标为待确认，不能以通用知识补写。
- 图形、曲线、拓扑、信号和流程关系必须保留标准图/重绘图、关键标注和做题结论。
- 不覆盖个人笔记、随手记、学习心得、踩坑记录、待探索和 `[!personal]` 块。
- `.agents/skills` 与 `.claude/skills` 的同名技能必须等价；保留平台专属元数据，不复制平台专属文件。

---

## File Structure

| 文件 | 责任 |
| --- | --- |
| `.agents/skills/learning-response-contract/SKILL.md` | Codex 侧统一回答模式和路由顺序 |
| `.claude/skills/learning-response-contract/SKILL.md` | Claude 侧等价契约 |
| `.agents/skills/learning-response-contract/evals/response-regression-cases.json` | Codex 侧匿名回归样例 |
| `.claude/skills/learning-response-contract/evals/response-regression-cases.json` | Claude 侧等价样例 |
| `.agents/skills/learning-response-contract/scripts/validate_cases.py` | 校验样例 schema、模式覆盖和字段完整性 |
| `.claude/skills/learning-response-contract/scripts/validate_cases.py` | Claude 侧等价校验器 |
| `.agents/skills/handwritten-note-reconstruction/SKILL.md` | Codex 侧手写重构协议 |
| `.claude/skills/handwritten-note-reconstruction/SKILL.md` | Claude 侧等价协议 |
| `.{agents,claude}/skills/kaoyan-{math,electronics}/SKILL.md` | 将请求动作/回答模式置于学科子模块之前 |
| `.{agents,claude}/skills/kaoyan-{math-notes,electronics-circuit}/SKILL.md` | 接入手写重构协议与学科质量门槛 |
| `.{agents,claude}/skills/kaoyan-{english,plan}/SKILL.md` | 仅接入统一回答模式，不改变已有内部流程 |

### Task 1: 建立统一回答契约与可检查的样例集

**Files:**
- Create: `.agents/skills/learning-response-contract/SKILL.md`
- Create: `.claude/skills/learning-response-contract/SKILL.md`
- Create: `.agents/skills/learning-response-contract/evals/response-regression-cases.json`
- Create: `.claude/skills/learning-response-contract/evals/response-regression-cases.json`
- Create: `.agents/skills/learning-response-contract/scripts/validate_cases.py`
- Create: `.claude/skills/learning-response-contract/scripts/validate_cases.py`

**Interfaces:**
- Consumes: `request_action`, `subject`, `write_requested`, `risk_level` as internal routing signals.
- Produces: exactly one `response_mode` in `quick_answer`, `concept_learning`, `problem_solving`, `note_reconstruction`, `planning_review`.
- Consumed by: the four subject/planning entry skills in Tasks 2 and 3.

- [ ] **Step 1: Write the failing regression fixture and validator test case**

Create `response-regression-cases.json` with this exact first case plus the five additional cases listed below:

```json
[
  {
    "id": "math-quick-derivative",
    "request": "这一步为什么能约分？",
    "subject": "math",
    "expected_mode": "quick_answer",
    "must_include": ["结论", "关键步骤", "易错点", "自检"],
    "must_not_include": ["整章笔记", "写入文件"]
  }
]
```

Add five records with IDs `math-problem-solving`, `electronics-circuit`, `math-handwritten`, `electronics-handwritten`, and `daily-planning`. Their `expected_mode` values must cover `problem_solving`, `note_reconstruction`, and `planning_review`; no identifier may repeat.

- [ ] **Step 2: Run the validator to verify it fails before implementation**

Run: `python3 .agents/skills/learning-response-contract/scripts/validate_cases.py .agents/skills/learning-response-contract/evals/response-regression-cases.json`

Expected: exit code `2` because the script does not exist.

- [ ] **Step 3: Write the minimal response contract and validator**

The contract must contain this routing table and hard rule:

```markdown
| 模式 | 触发 | 最小输出 |
| --- | --- | --- |
| `quick_answer` | 局部为什么/是什么/怎么判断 | 结论、2-4 个关键步骤、一个易错点、一个自检 |
| `concept_learning` | 讲懂/系统整理一个知识点 | 钩子、TL;DR、为什么、是什么、怎么用、微型自测 |
| `problem_solving` | 题目/错因/解法 | 题型、SOP、分步解、错因、下次触发点 |
| `note_reconstruction` | 笔记、图片、手写、板书 | 来源盘点、重构正文、图示、速查、原图溯源 |
| `planning_review` | 安排、完成、复盘 | 策略、时间块/记录、兜底、下一次汇报 |

先选回答模式，再选学科和子模块；只有写入被明确请求或确有长期价值时，才启动文件更新。
```

Implement `validate_cases.py` with the following complete behavior:

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

MODES = {"quick_answer", "concept_learning", "problem_solving", "note_reconstruction", "planning_review"}
REQUIRED_IDS = {
    "math-quick-derivative", "math-problem-solving", "electronics-circuit",
    "math-handwritten", "electronics-handwritten", "daily-planning",
}
REQUIRED_FIELDS = {"id", "request", "subject", "expected_mode", "must_include", "must_not_include"}

def main(path_text: str) -> int:
    try:
        cases = json.loads(Path(path_text).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"invalid fixture: {error}", file=sys.stderr)
        return 1
    if not isinstance(cases, list):
        print("fixture must be a JSON array", file=sys.stderr)
        return 1
    ids = []
    modes = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != REQUIRED_FIELDS:
            print(f"invalid case schema: {case}", file=sys.stderr)
            return 1
        if not all(isinstance(case[key], str) and case[key] for key in ("id", "request", "subject", "expected_mode")):
            print(f"invalid scalar fields: {case['id']}", file=sys.stderr)
            return 1
        if case["expected_mode"] not in MODES:
            print(f"unknown mode: {case['expected_mode']}", file=sys.stderr)
            return 1
        if not all(isinstance(case[key], list) and case[key] for key in ("must_include", "must_not_include")):
            print(f"invalid expectation lists: {case['id']}", file=sys.stderr)
            return 1
        ids.append(case["id"])
        modes.add(case["expected_mode"])
    if len(ids) != len(set(ids)) or set(ids) != REQUIRED_IDS:
        print("fixture IDs do not match the required six cases", file=sys.stderr)
        return 1
    if not {"quick_answer", "problem_solving", "note_reconstruction", "planning_review"}.issubset(modes):
        print("fixture does not cover the required response modes", file=sys.stderr)
        return 1
    print(f"validated {len(cases)} response regression cases")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) == 2 else ""))
```

- [ ] **Step 4: Run the validators and platform parity checks**

Run:

```bash
python3 .agents/skills/learning-response-contract/scripts/validate_cases.py .agents/skills/learning-response-contract/evals/response-regression-cases.json
python3 .claude/skills/learning-response-contract/scripts/validate_cases.py .claude/skills/learning-response-contract/evals/response-regression-cases.json
cmp .agents/skills/learning-response-contract/SKILL.md .claude/skills/learning-response-contract/SKILL.md
cmp .agents/skills/learning-response-contract/evals/response-regression-cases.json .claude/skills/learning-response-contract/evals/response-regression-cases.json
```

Expected: both validators print `validated 6 response regression cases`; both `cmp` commands exit `0`.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/learning-response-contract .claude/skills/learning-response-contract
git commit -m "feat: add learning response contract"
```

### Task 2: 将数学与电子技术入口改为“模式优先”路由

**Files:**
- Modify: `.agents/skills/kaoyan-math/SKILL.md`
- Modify: `.claude/skills/kaoyan-math/SKILL.md`
- Modify: `.agents/skills/kaoyan-electronics/SKILL.md`
- Modify: `.claude/skills/kaoyan-electronics/SKILL.md`
- Modify: `.agents/skills/kaoyan-english/SKILL.md`
- Modify: `.claude/skills/kaoyan-english/SKILL.md`
- Modify: `.agents/skills/kaoyan-plan/SKILL.md`
- Modify: `.claude/skills/kaoyan-plan/SKILL.md`

**Interfaces:**
- Consumes: `learning-response-contract` from Task 1.
- Produces: a declared answer mode before the existing subject-specific routing decision.
- Consumed by: existing `kaoyan-math-notes`, `kaoyan-electronics-circuit`, English submodules and planning features.

- [ ] **Step 1: Add a failing contract-presence check**

Run this command before modifying entry skills:

```bash
rg -q '先选回答模式，再选学科' .agents/skills/kaoyan-math/SKILL.md
```

Expected: exit code `1` because no entry skill yet references the contract.

- [ ] **Step 2: Add the minimal routing block to the four entry skills on both platforms**

Add this section after each entry skill’s role definition, adapting the final subject-specific line only:

```markdown
## 回答模式优先

先读取 `learning-response-contract` 并确定本次 `response_mode`，再进入本技能的既有路由。

- `quick_answer`：只解决当前疑问，不自动展开成整章笔记或写入文件。
- `concept_learning`：按“钩子 → TL;DR → 为什么 → 是什么 → 怎么用 → 自检”组织。
- `problem_solving`：进入本学科已有 SOP/分步讲解。
- `note_reconstruction`：数学转入 `kaoyan-math-notes`；电子技术转入 `kaoyan-electronics-circuit`；英语仅在用户明确提供手写词汇/阅读标注时做保守转写。
- `planning_review`：仅 `/kaoyan-plan` 处理；其他科目把计划/完成汇报转交它。

只有用户明确要求或长期复习价值明确时才写入文件；若目标路径不明，不创建文件。
```

For `kaoyan-plan`, retain its existing schedule template and replace the `problem_solving` line with “不处理题目讲解，转交对应学科入口”。

- [ ] **Step 3: Synchronize the existing math-notes divergence before adding new behavior**

Use `.agents/skills/kaoyan-math-notes/SKILL.md` as the functional baseline because it contains the complete source-note, LaTeX, protection, and template rules. Merge any Claude-only version metadata into the common file, set both frontmatter versions to `1.2.0`, then make the resulting two `SKILL.md` files byte-identical. Do not copy `agents/openai.yaml` or any platform-only files.

- [ ] **Step 4: Verify routing and parity**

Run:

```bash
for skill in kaoyan-math kaoyan-electronics kaoyan-english kaoyan-plan; do
  rg -q '学习回答契约\|learning-response-contract' ".agents/skills/$skill/SKILL.md"
  cmp ".agents/skills/$skill/SKILL.md" ".claude/skills/$skill/SKILL.md"
done
```

Expected: all commands exit `0`.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/kaoyan-math .claude/skills/kaoyan-math \
  .agents/skills/kaoyan-electronics .claude/skills/kaoyan-electronics \
  .agents/skills/kaoyan-english .claude/skills/kaoyan-english \
  .agents/skills/kaoyan-plan .claude/skills/kaoyan-plan \
  .agents/skills/kaoyan-math-notes .claude/skills/kaoyan-math-notes
git commit -m "feat: route learning requests by response mode"
```

### Task 3: 实现手写笔记重构协议并接入学科质量门槛

**Files:**
- Create: `.agents/skills/handwritten-note-reconstruction/SKILL.md`
- Create: `.claude/skills/handwritten-note-reconstruction/SKILL.md`
- Modify: `.agents/skills/kaoyan-math-notes/SKILL.md`
- Modify: `.claude/skills/kaoyan-math-notes/SKILL.md`
- Modify: `.agents/skills/kaoyan-electronics-circuit/SKILL.md`
- Modify: `.claude/skills/kaoyan-electronics-circuit/SKILL.md`

**Interfaces:**
- Consumes: `note_reconstruction` mode from Task 1, plus source images, screenshots or handwritten notes.
- Produces: visual inventory, reconstructed logic, optional redraw requirements, uncertainty list, source-to-body mapping and a reviewable output shape.
- Consumed by: math notes and electronics circuit modules.

- [ ] **Step 1: Add a failing static check**

Run:

```bash
test -f .agents/skills/handwritten-note-reconstruction/SKILL.md
```

Expected: exit code `1` because the shared protocol does not yet exist.

- [ ] **Step 2: Create the shared protocol on both platforms**

The shared `SKILL.md` must include this fixed sequence and output shape:

```markdown
## 固定处理顺序

1. 视觉盘点：文字、公式、箭头、框选、颜色、编号、图、曲线、表格、拓扑与留白。
2. 不确定项：看不清的内容列为“待确认”，不得猜测。
3. 思路重建：问题 → 核心结论 → 条件/符号 → 推导或判断链 → 做题启动条件。
4. 图文双轨：图形知识重绘标准图，并写图的作用、关键标注、做题结论。
5. 原图溯源：原图折叠保存，正文每个关键段可回指对应区域。

## 默认交付

1. 一句话结论；2. 符号/标注速查；3. 重构逻辑链；4. 图示说明；5. 最小 SOP；6. 易错点与待确认项；7. 手写来源。
```

Include the safety constraints from the global constraints verbatim and state that “仅转写” may omit extended explanation but may not omit uncertainty marking or source traceability.

- [ ] **Step 3: Integrate the protocol into the two specialized modules**

Append this exact routing requirement to `kaoyan-math-notes` after source-note rules:

```markdown
### 手写笔记重构

用户提供手写笔记、板书截图或照片时，先调用 `handwritten-note-reconstruction`，不得直接按普通文本模板改写。数学公式、定义、定理和推导须在重构前自行核验；有曲线、几何关系、边界或变量方向时，正文必须包含标准图或重绘图及其做题结论。
```

Append this exact requirement to `kaoyan-electronics-circuit` after its image-handling rules:

```markdown
### 手写电路笔记重构

用户提供手写电路/波形/特性曲线时，先调用 `handwritten-note-reconstruction`。重绘前逐项核对器件、端口、接地、电源、输入输出、方向、反馈路径和悬空节点；无法辨认的参数或极性只能标“待确认”。原图只能作为折叠溯源，不能代替正文的清晰电路图或波形图。
```

- [ ] **Step 4: Verify shared protocol, integrations and parity**

Run:

```bash
for root in .agents .claude; do
  rg -q '视觉盘点' "$root/skills/handwritten-note-reconstruction/SKILL.md"
  rg -q '不得猜测' "$root/skills/handwritten-note-reconstruction/SKILL.md"
  rg -q 'handwritten-note-reconstruction' "$root/skills/kaoyan-math-notes/SKILL.md"
  rg -q 'handwritten-note-reconstruction' "$root/skills/kaoyan-electronics-circuit/SKILL.md"
done
cmp .agents/skills/handwritten-note-reconstruction/SKILL.md .claude/skills/handwritten-note-reconstruction/SKILL.md
cmp .agents/skills/kaoyan-electronics-circuit/SKILL.md .claude/skills/kaoyan-electronics-circuit/SKILL.md
```

Expected: every command exits `0`.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/handwritten-note-reconstruction .claude/skills/handwritten-note-reconstruction \
  .agents/skills/kaoyan-math-notes .claude/skills/kaoyan-math-notes \
  .agents/skills/kaoyan-electronics-circuit .claude/skills/kaoyan-electronics-circuit
git commit -m "feat: add handwritten note reconstruction workflow"
```

### Task 4: 完成端到端检查和项目说明同步

**Files:**
- Modify: `docs/superpowers/specs/2026-07-24-learning-response-experience-design.md`
- Modify: `docs/superpowers/specs/2026-07-24-handwritten-note-reconstruction-design.md`

**Interfaces:**
- Consumes: completed Tasks 1-3.
- Produces: implementation status recorded in the design documents and repeatable validation commands.

- [ ] **Step 1: Run all contract checks**

Run:

```bash
python3 .agents/skills/learning-response-contract/scripts/validate_cases.py .agents/skills/learning-response-contract/evals/response-regression-cases.json
python3 .claude/skills/learning-response-contract/scripts/validate_cases.py .claude/skills/learning-response-contract/evals/response-regression-cases.json
for skill in learning-response-contract handwritten-note-reconstruction kaoyan-math kaoyan-electronics kaoyan-english kaoyan-plan kaoyan-math-notes kaoyan-electronics-circuit; do
  diff -q ".agents/skills/$skill/SKILL.md" ".claude/skills/$skill/SKILL.md"
done
git diff --check
```

Expected: both validators report six cases, all `diff -q` calls return `0`, and `git diff --check` has no output.

- [ ] **Step 2: Record implemented behavior without changing the approved scope**

Append this exact status block to both design documents:

```markdown
## 实施状态

- 已实现：统一回答模式、入口路由、手写笔记重构协议、匿名回归样例和双平台一致性检查。
- 未自动化：对真实 LLM 回复的语义评分；该部分由回归样例的人工验收承担，后续用真实不满意回复持续扩充。
```

- [ ] **Step 3: Re-run checks and commit**

Run the command from Step 1 again, then:

```bash
git add docs/superpowers/specs/2026-07-24-learning-response-experience-design.md \
  docs/superpowers/specs/2026-07-24-handwritten-note-reconstruction-design.md
git commit -m "docs: record learning response rollout"
```

## Plan Self-Review

- **Spec coverage:** Task 1 implements response modes and sample-based regression; Task 2 implements mode-first routing and existing math skill parity; Task 3 implements handwritten reconstruction and specialized quality gates; Task 4 verifies platform equivalence and records limitations.
- **No-placeholder check:** all created and changed paths, commands, required strings, JSON schema and validator source are specified.
- **Interface consistency:** every entry skill consumes `learning-response-contract`; `note_reconstruction` routes to `handwritten-note-reconstruction`; specialized modules consume that exact identifier; the validator’s fixture schema uses the same five response mode values.
