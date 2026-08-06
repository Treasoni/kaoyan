# LLM 用量测量系统（.llm/prompt-cache/）

> 为考研复习项目建立 LLM 调用可观测性，量化「提示缓存优化」的真实效果（输入 token / 缓存读取 token / 输出 / 质量），不靠猜测。
> 规则入口见 `CLAUDE.md` / `AGENTS.md` 的 Prompt Cache 区块与 `.claude/rules/common/prompt-cache.md`。

---

## 这是什么

本项目同时跑 Claude Code 与 Codex/Codebuddy 多 agent。本目录管 **Claude Code 一侧的调用计量**：

- **数据来源**：Claude Code 会话转储 `~/.claude/projects/-Users-zhqznc-Documents-----/*.jsonl` 中 assistant 消息的 `usage` 字段。
- **脱敏**：只保留时间戳、模型、token 数、粗粒度请求类型、会话 ID；**绝不保存**原始用户输入、提示词、模型输出、密钥。
- **已校验**：提取出的 `events/*.jsonl` 中 0 条原始内容泄漏。

## 目录结构

| 路径 | 说明 |
|---|---|
| `llm-usage-event.schema.json` | 每行事件的字段合同（由 bootstrap 安装） |
| `regression-cases.json` | 6 个高频请求回归样本 + 质量判定 + 基线 |
| `scripts/extract-usage-events.py` | 提取器（手动运行或 hook 触发） |
| `scripts/analyze-usage-events.py` | 分析器：汇总命中率 + 回归基线对比 |
| `events/YYYY-MM-DD.jsonl` | 按日聚合的脱敏事件（**已 gitignore**，仅本地） |
| `scripts/` 与上方 schema/regression 可提交；`events/` 不提交 | — |

## 数据流

```
Claude Code 会话
  → ~/.claude/projects/-Users-zhqznc-Documents-----/*.jsonl（自动写入）
  → SessionEnd hook：.claude/hooks/run-prompt-cache-extract.py（每次会话结束触发）
  → scripts/extract-usage-events.py --transcript <path>
  → events/YYYY-MM-DD.jsonl（合并去重）
```

## 怎么用

**1. 自动**：`.claude/settings.json` 已注册 `SessionEnd` hook，每次会话结束自动提取，无需操作。`settings.json` 是本地 gitignored 配置。

**2. 手动补齐**（SessionEnd 没触发时）：

```bash
python3 .llm/prompt-cache/scripts/extract-usage-events.py --since 2026-08-02
```

常用参数：`--transcript <文件>`（只处理单个会话）、`--since YYYY-MM-DD`、`--max-sessions N`。

**3. 回归对比**：改动任何提示词/模板/模型/hook 后，运行分析器重测，和基线对比：

```bash
python3 .llm/prompt-cache/scripts/analyze-usage-events.py
# 常用：--since YYYY-MM-DD（只看近期）、--model deepseek-v4-flash（限定模型）、--no-baseline
```

**只有质量检查通过 + 输入/缓存 token 变少，才算有效优化。**（2026-08-03 起基线由 `regression-cases.json` 提供，提取器已过滤 token 全 0 的空 usage 事件。）

## 基线怎么读（重要：DeepSeek 语义）

- 当前 `ANTHROPIC_BASE_URL` 指向 DeepSeek Anthropic 兼容端点，实际模型为 `deepseek-v4-flash` / `deepseek-v4-pro`。
- 事件中 `cache_read_tokens` 常**远大于** `input_tokens`：该端点语义下 `input_tokens` ≈ 未命中部分、`cache_read_tokens` ≈ 命中部分，**两者相加才是完整输入**。缓存命中占比 ≈ `cache_read / (input + cache_read)`。
- `output_tokens` 在转储中多为 0（请求起始记录），**不可作为输出量依据**。
- 分组比较必须同 `model + request_type`，不能跨提供方/模型混比。

## 已测量基线（2026-08-03 刷新，deepseek-v4-flash）

窗口：2026-06-18 起；已剔除 token 全 0 事件；分类已修复（Obsidian `<command-name>` 包装、`❯` 终端前缀、`/kaoyan-info`）。n 为事件数（会话数见回归样本注释）。

| request_type | 事件数 | avg 输入 | avg 缓存读 | 命中率 |
|---|---|---|---|---|
| kaoyan_plan | 1,712 | 5,594 | 84,845 | 93.8% |
| mistake_book | 1,633 | 3,468 | 81,100 | 95.9% |
| kaoyan_math | 300 | 7,824 | 63,052 | 89.0% |
| kaoyan_info | 48 | 2,065 | 41,227 | 95.2% |
| prompt_cache_optimizer（非回归样本） | 376 | 3,355 | 115,975 | 97.2% |
| general_chat（兜底桶，非回归样本） | 294 | 5,200 | 74,204 | 93.5% |
| kaoyan_electronics | 8 | 7,482 | 22,560 | 75.1%（小样本） |
| kaoyan_english / understanding | 0 | — | —（v4 的 kaoyan_english 基线为误分类的 /kaoyan-plan 完成报告，已纠正，待真实会话补齐） |

## 隐私与安全

- 提取器只写元数据；schema 明确禁止记录原始提示词、输出、密钥。
- `events/` 已加入 `.gitignore`。
- hook 脚本无 stdout 输出，不污染会话上下文。

## 维护

- **分类逻辑**：`request_type` 由会话首条用户消息关键词粗分（`scripts/extract-usage-events.py` 的 `COMMAND_SLUGS` / `KEYWORD_FALLBACK`）。不准就扩表，别改事件格式。
- **空 usage 过滤**：提取器与分析器都会丢弃 token 全 0 的事件（某些网关返回空 usage 块），防止污染均值与命中率。
- **新增高频请求类型**：① 在 `regression-cases.json` 加 case；② 在提取器的 `COMMAND_SLUGS` 加映射；③ 分析器默认按 `request_type` 分组，无需改。
- **其他 agent**：Codex（`~/.codex/logs_2.sqlite`、`sessions/`）、Codebuddy 日志格式不同，需要时另写适配器，本目录只覆盖 Claude Code。

## 测量限制

- **request_type 为会话级粗分**：由会话首条用户消息关键词决定（`extract-usage-events.py` 的 `COMMAND_SLUGS` / `KEYWORD_FALLBACK`），一次会话内切换科目（如数学会话里顺带背单词）会一直归入首条类型。分组对比时注意混合科目会话的归属。
- **kaoyan_english / understanding 为数据缺口**：两个 L1 入口技能当前 0 事件，回归基线显示 `[no-data]`，待真实会话补齐后才能评估缓存行为。
- **模型过滤口径**：分析器默认只分析 DeepSeek 两个模型（`DEFAULT_MODELS`），早期 MiniMax-M3 / mimo-v2.5 历史事件被过滤且不参与分组；表头计数已与分组口径一致（`+N events of other models excluded`）。
