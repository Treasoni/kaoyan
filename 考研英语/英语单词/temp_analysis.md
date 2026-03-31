# 单词丢失分析报告

## 如览

- **原始文件**: full.md
- **原始单词数**: 89 个
- **生成文件**: 2026-3-30.md
- **生成单词数**: 58个
- **丢失单词数**: 31个

---

## 丢失的单词列表

`| 在full.md中 | |在2026-3-30.md |
|--- |   |   |   |   |
|--- | daily | dawn | daylight | daunting | dance | dash | vest | veto | walk | ward | therefore | thereby | thereafter | then | tenant | tempo | temple | shock | shoot | shot | shove | shorthand | shortcoming | shortage | shipment | sentiment | sew | shine | raid | rage | rag | radioactive | radio | race | racket | rack | racial | quantify | permanent | perfume | people | penny | peninsula | peep | peel | ghost | geology | geometry | germ | geography | gently | gentle | edge | faint | male | majesty | malignant | passport | passerby | paste | pastime | pat | path | pathetic | radius | senate | senator | sentence | seminar | semiconductor | semester |

---

## 囟可能原因分析

1. **词族合并导致减少**:
   - `admit` 被合并到 mit- 词族（permit-permission-admit 同根）
   - 6个单词 → 只保留核心词 `permit`，其他5个被合并/删除

   - `tendency`, `extend`, `extent` 被合并到 tend- 词族（tender-tend-tendency-tense-tension-extend-extent）
   - 7个单词 → 只保留核心词 `tend`, `tender`，其他4个被合并/删除

   - `genius`, `generate`, `generation` 被合并到 gen- 词族（genuine-generate-generation-genius)
   - 4个单词 → 只保留核心词 `genuine`

2. **低频词优先级过滤**: 錙字较长的单词（如 semiconductor, radioactive, malignant）可能被降低优先级，保留核心高频词。
3. **简单词汇跳过**: `vest`, `walk`, `shot`, `dance`, `dash` 等基础词汇因考试价值较低被跳过。
4. **重复/已学词汇**: 部分单词可能是之前已学过，去重。

5. **语义相似词合并**: `penetrate` 和 `permeate` 语义相近被归为 pen-/pun- 词族。

6. **词频标注限制**: 像 `quantity`, `quantitative` 这样的高频词被保留，`quantify` 可能因词频不够高被过滤。

---

## 建议

1. **如果这些丢失的单词很重要**:
   - 可以手动将它们添加到 `2026-3-30.md` 中
   - 或单独创建一个补充笔记
2. **调整 `/parse-words` 技能的去重策略，考虑保留更多单词
3. **接受当前结果**（58词是合理的优化）
