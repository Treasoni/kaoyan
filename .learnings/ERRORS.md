# Errors

Command failures and integration errors.

---

## [ERR-20260425-001] obsidian-markdown-skill

**Logged**: 2026-04-25T08:41:06+00:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Invoking the `obsidian-markdown` skill failed a permission check before the markdown note edit could start.

### Error
```
Bash command permission check failed for pattern "!` to embed its content inline:

`": This command requires approval
```

### Context
- Command/operation attempted: `Skill` invocation for `obsidian-markdown`
- Input or parameters used: no explicit args; intended to help edit an existing Obsidian markdown note
- Environment details if relevant: failure happened immediately on skill launch, before file edits
- Summary or redacted excerpt of relevant output: the skill appears to rely on a shell pattern blocked by the current permission policy

### Suggested Fix
Use direct `Read`/`Edit` operations as the fallback for simple markdown note updates when the skill launch is blocked by permissions, or request approval if the skill is required.

### Metadata
- Reproducible: unknown
- Related Files: .learnings/ERRORS.md

---
