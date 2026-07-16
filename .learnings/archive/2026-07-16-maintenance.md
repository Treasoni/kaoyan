# Learnings Maintenance Archive


## 2026-07-16 maintenance：ERR-20260716-002 digest

### 原记录

## [ERR-20260716-002] digest

**Logged**: 2026-07-16T10:55:08+08:00
**Priority**: high
**Status**: pending
**Area**: ops

### Summary
digest 压缩写入 RULES.md 时再次因 Python 字符串转义生成控制字符

### Error
```text
RULES.md 中 `\begin`、`\rvert` 被普通 Python 字符串解释为控制字符：\x08、\r
```

### Context
执行 digest 阈值压缩并重写 `.learnings/RULES.md` 时，最初使用普通三引号字符串保存包含 LaTeX 命令的规则文本，导致 `\begin` 和 `\rvert` 被转义污染。随后立即改用 raw string 写回 RULES.md，并扫描 `.learnings/RULES.md`、`.learnings/LEARNINGS.md`、`.learnings/ERRORS.md`、归档文件，确认控制字符为 0。

---

### 修复路径

- 修改 `.agents/skills/digest/SKILL.md` 与 `.claude/skills/digest/SKILL.md`。
- 新增 `Step 4.1: 写入安全与控制字符验证`，要求 `.learnings/` 写入使用 raw string / 安全写入方式，并在写后扫描控制字符、回读关键段落。
- 同步验证 `digest` 在 Codex 与 Claude Code 两侧一致。

### 验证方式

```bash
python3 .agents/skills/maintain-learnings/scripts/sync_platform_skills.py --root . --skill digest
python3 -c 'from pathlib import Path; p=Path(".agents/skills/digest/SKILL.md"); t=p.read_text(encoding="utf-8"); assert t.startswith("---\n") and "\n---" in t[4:]; assert "name:" in t and "description:" in t'
python3 -c 'from pathlib import Path; p=Path(".claude/skills/digest/SKILL.md"); t=p.read_text(encoding="utf-8"); assert t.startswith("---\n") and "\n---" in t[4:]; assert "name:" in t and "description:" in t'
```

### 处理结果

已归档；后续若 `.learnings/` 再出现控制字符污染，应视为 `digest` 写入安全机制失效并重新维护。

---
