# Codex Compatibility Layer

This project keeps Claude Code and Codex side by side.

## Design

- `CLAUDE.md` and `.claude/` remain the Claude-specific entrypoints.
- `AGENTS.md` is the Codex-facing project rule file.
- Shared reusable skills live in `.agents/skills/`.
- Codex-only MCP wiring lives in `.codex/config.toml`.

## What was added for Codex

To mirror the existing Claude workflow without changing it, Codex now has:

- `parse-words`
- `understanding`
- `sync`

These are implemented as Codex skills under `.agents/skills/` so they can coexist with Claude's command-based setup.

## Maintenance Rule

When adding new study workflow abilities in the future:

1. Keep Claude command files in `.claude/commands/` if they are Claude-specific.
2. Add a Codex skill under `.agents/skills/` when the capability should also be available in Codex.
3. Add Codex MCP dependencies only in `.codex/config.toml`.

This keeps the two agents compatible without overwriting each other's configuration.
