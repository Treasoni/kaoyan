#!/usr/bin/env python3
"""Extract sanitized LLM usage events from Claude Code session transcripts.

Reads ~/.claude/projects/-Users-zhqznc-Documents-----/*.jsonl and emits one
llm-usage-event per assistant message that carries a `usage` block, then
writes them to .llm/prompt-cache/events/YYYY-MM-DD.jsonl.

Privacy: only metadata is kept (timestamps, model, token counts, a command
bucket and session id). Raw user input, prompt text and model output are
NEVER written. request_type is a coarse bucket derived from the session's
first user message; the raw text is discarded.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Expected: <project>/.llm/prompt-cache/scripts/extract-usage-events.py
DEFAULT_ROOT = Path(__file__).resolve().parents[3]
TRANSCRIPT_GLOB = "~/.claude/projects/-Users-zhqznc-Documents-----/*.jsonl"
PROVIDER_NOTE = "deepseek-anthropic-compat (ANTHROPIC_BASE_URL)"

COMMAND_SLUGS = {
    "/kaoyan-plan": "kaoyan_plan",
    "/kaoyan-math": "kaoyan_math",
    "/kaoyan-english": "kaoyan_english",
    "/kaoyan-electronics": "kaoyan_electronics",
    "/kaoyan-info": "kaoyan_info",
    "/sync": "sync",
    "/understanding": "understanding",
    "/parse-words": "parse_words",
    "/digest": "digest",
    "/mistake-book": "mistake_book",
    "/mistake-extract": "mistake_extract",
    "/chapter-summary": "chapter_summary",
    "/prompt-cache-optimizer": "prompt_cache_optimizer",
    "/knowledge": "knowledge",
    "/pdf": "pdf",
    "/docx": "docx",
}
KEYWORD_FALLBACK = {
    ("安排计划", "今天怎么学", "补计划", "周复盘", "完成了什么", "计划归档", "归档计划", "月计划", "周计划"): "kaoyan_plan",
    ("章节总结", "整理章节", "汇总这一章", "章节笔记"): "chapter_summary",
    ("错题", "错题本", "记错题"): "mistake_book",
    ("背单词", "复习单词", "英语"): "kaoyan_english",
    ("极限", "高数", "数学"): "kaoyan_math",
    ("电子技术", "模电", "数电", "专业课"): "kaoyan_electronics",
}


def user_text(obj: dict) -> str:
    msg = obj.get("message")
    if not isinstance(msg, dict):
        return ""
    content = msg.get("content")
    parts: list[str] = []
    if isinstance(content, str):
        parts.append(content)
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
    return "\n".join(parts).strip()


def _extract_command_name(text: str) -> str:
    """Pull the canonical /command out of the Obsidian plugin wrapper.

    The Claudian plugin prefixes slash-command sessions with:
        <command-message>kaoyan-plan</command-message>
        <command-name>/kaoyan-plan</command-name>
        <command-args>...</command-args>
    The <command-name> value is the reliable token.
    """
    m = re.search(r"<command-name>\s*(/[^\s<]+)\s*</command-name>", text)
    return m.group(1) if m else ""


def _strip_prompt_prefix(text: str) -> str:
    """Drop the Obsidian <command-message> wrapper and shell prompt glyphs.

    Handles messages such as "❯ /kaoyan-plan 7月7" that are pasted from a
    terminal, where startswith('/') would otherwise never match.
    """
    text = re.sub(r"<command-message>\s*[^<]*?\s*</command-message>", "", text, count=1)
    text = re.sub(r"^\s*[❯$>]\s*", "", text)
    return text.strip()


def detect_request_type(first_user_text: str) -> str:
    text = first_user_text.strip()
    # 1. Explicit command name embedded by the Obsidian plugin wrapper.
    cmd = _extract_command_name(text)
    if cmd in COMMAND_SLUGS:
        return COMMAND_SLUGS[cmd]
    # 2. Message text that starts with a known command (after normalising the
    #    Obsidian wrapper / terminal prompt glyphs away).
    stripped = _strip_prompt_prefix(text)
    for prefix, slug in COMMAND_SLUGS.items():
        if stripped.startswith(prefix):
            return slug
    # 3. Keyword fallback on the original text.
    for words, slug in KEYWORD_FALLBACK.items():
        if any(w in text for w in words):
            return slug
    return "general_chat"


def iso(timestamp: str) -> str:
    if not timestamp:
        return datetime.now(timezone.utc).isoformat()
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.isoformat()
    except ValueError:
        return timestamp


def has_usable_tokens(e: dict) -> bool:
    """Return False when a provider returned an empty/all-zero usage block.

    Some gateway responses (observed as MiniMax-M3 on the DeepSeek-compat
    endpoint) carry a usage dict with no token counts. Keeping those events
    pollutes cache-rate averages and regression baselines, so drop them.
    """
    return bool(
        (e.get("input_tokens") or 0)
        or (e.get("cache_read_tokens") or 0)
        or (e.get("cache_write_tokens") or 0)
        or (e.get("output_tokens") or 0)
    )


def event_key(e: dict) -> str:
    # NOTE: timestamp is intentionally excluded. Claude Code transcripts can
    # record the same assistant turn's usage block several times within ~1s
    # (verified: 90% of duplicate (session,in,cr,out) clusters span <5s, 0 span
    # >=60s), which previously inflated event counts ~3x. Distinct turns with
    # byte-identical usage do not occur in this dataset, so dropping the
    # timestamp only collapses genuine same-turn duplicates and never merges
    # separate turns.
    m = e["metadata"]
    return "|".join(
        [
            m["session_id"],
            str(e["model"]),
            str(e["input_tokens"]),
            str(e["cache_read_tokens"]),
            str(e["cache_write_tokens"]),
            str(e["output_tokens"]),
        ]
    )


def load_existing(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if not has_usable_tokens(obj):
                continue
            out[event_key(obj)] = obj
    return out


def parse_session(path: Path, session_id: str, first_user_text: str) -> list[dict]:
    request_type = detect_request_type(first_user_text)
    events: list[dict] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            msg = obj.get("message")
            usage = msg.get("usage") if isinstance(msg, dict) else None
            if not isinstance(usage, dict) or "input_tokens" not in usage:
                continue
            model = str(msg.get("model", "unknown"))
            ev = {
                "timestamp": iso(obj.get("timestamp", "")),
                "request_type": request_type,
                "template_id": "claude_code_session",
                "template_version": "transcript-v1",
                "model": model,
                "input_tokens": int(usage.get("input_tokens", 0) or 0),
                "cache_read_tokens": int(usage.get("cache_read_input_tokens", 0) or 0),
                "cache_write_tokens": int(usage.get("cache_creation_input_tokens", 0) or 0),
                "output_tokens": int(usage.get("output_tokens", 0) or 0),
                "latency_ms": 0,
                "status": "success",
                "input_reference": session_id,
                "quality_score": None,
                "metadata": {
                    "session_id": session_id,
                    "provider_note": PROVIDER_NOTE,
                    "service_tier": str(usage.get("service_tier", "")),
                    "latency_source": "unavailable",
                },
            }
            if not has_usable_tokens(ev):
                continue
            k = event_key(ev)
            if k not in seen:
                seen.add(k)
                events.append(ev)
    return events


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", default=None, help="Only sessions modified on/after YYYY-MM-DD")
    parser.add_argument("--max-sessions", type=int, default=0, help="Cap number of session files scanned (0 = all)")
    parser.add_argument("--transcript", default=None, help="Process a single transcript file instead of globbing all")
    parser.add_argument("--out-dir", default=None, help="Overwrite output dir (default: <root>/.llm/prompt-cache/events)")
    args = parser.parse_args()

    root = Path(args.out_dir).resolve() if args.out_dir else (DEFAULT_ROOT / ".llm" / "prompt-cache" / "events")
    root.mkdir(parents=True, exist_ok=True)

    if args.transcript:
        files = [os.path.expanduser(args.transcript)]
    else:
        files = sorted(glob.glob(os.path.expanduser(TRANSCRIPT_GLOB)))
    if not files:
        print("no transcripts found", file=sys.stderr)
        return 1

    if args.since:
        since = datetime.fromisoformat(args.since).astimezone()
        files = [f for f in files if datetime.fromtimestamp(Path(f).stat().st_mtime).astimezone() >= since]
    if args.max_sessions:
        files = files[-args.max_sessions:]

    per_day: dict[str, dict[str, dict]] = {}
    total_events = 0
    for f in files:
        path = Path(f)
        session_id = path.stem
        first_user_text = ""
        # Peek first user message for command detection (discard text afterwards).
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("type") == "user" and obj.get("message"):
                    first_user_text = user_text(obj)
                    if first_user_text:
                        break
        events = parse_session(path, session_id, first_user_text)
        for ev in events:
            day = ev["timestamp"][:10]
            bucket = per_day.setdefault(day, {})
            bucket[event_key(ev)] = ev
            total_events += 1

    for day, bucket in sorted(per_day.items()):
        out_path = root / f"{day}.jsonl"
        merged = load_existing(out_path)
        merged.update(bucket)
        lines = sorted(merged.values(), key=lambda e: e["timestamp"])
        out_path.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in lines), encoding="utf-8")
        print(f"{out_path}: {len(lines)} events (day)")

    print(f"total new events emitted: {total_events}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
