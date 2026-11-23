#!/usr/bin/env python3
"""Report sanitized usage data. Historical snapshots are not replayed regressions."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

CACHE_ROOT = Path(__file__).resolve().parents[1]
LEGACY_DEEPSEEK_MODELS = {"deepseek-v4-flash", "deepseek-v4-pro"}
TOKEN_FIELDS = ("input_tokens", "cache_read_tokens", "cache_write_tokens", "output_tokens")
GroupKey = tuple[str, str, str, str, str, str]
Groups = dict[GroupKey, list[dict]]


def token(event: dict, field: str) -> int | None:
    value = event.get(field)
    return value if type(value) is int and value >= 0 else None


def load_events(paths: list[Path], since: str | None) -> list[dict]:
    events = []
    for path in paths:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(event, dict) or not any(token(event, field) for field in TOKEN_FIELDS):
                    continue
                timestamp = event.get("timestamp")
                if since and (not isinstance(timestamp, str) or timestamp[:10] < since):
                    continue
                events.append(event)
    return events


def group_key(event: dict) -> GroupKey:
    metadata = event.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    collector = str(metadata.get("collector_version", "legacy"))
    model = str(event.get("model") or "unknown")
    template = str(event.get("template_id") or "unknown")
    version = str(event.get("template_version") or "unknown")
    declared = metadata.get("cache_semantics")
    if declared == "anthropic":
        semantics = "anthropic"
    elif (
        declared is None
        and collector == "legacy"
        and template == "claude_code_session"
        and version == "transcript-v1"
        and model in LEGACY_DEEPSEEK_MODELS
    ):
        # Two-part input is documented only for these historical transcript events.
        semantics = "deepseek-legacy"
    else:
        semantics = "unknown"
    return str(event.get("request_type") or "unknown"), template, version, model, collector, semantics


def average(events: list[dict], field: str) -> float | None:
    values = [value for event in events if (value := token(event, field)) is not None]
    return sum(values) / len(values) if values else None


def input_metrics(events: list[dict], semantics: str) -> tuple[float | None, float | None]:
    if semantics == "unknown":
        return None, None
    fields = TOKEN_FIELDS[:3] if semantics == "anthropic" else TOKEN_FIELDS[:2]
    totals = [0] * len(fields)
    for event in events:
        for index, field in enumerate(fields):
            value = token(event, field)
            if value is None:
                return None, None
            totals[index] += value
    total_input = sum(totals)
    return total_input / len(events), (100 * totals[1] / total_input if total_input else None)


def fmt(value: float | None, width: int = 10, decimals: int = 0) -> str:
    return f"{value:>{width},.{decimals}f}" if value is not None else f"{'N/A':>{width}}"


def report(groups: Groups, min_events: int) -> None:
    print(f"\n{'request_type':<22} {'template/version':<33} {'model':<22} {'collector/semantics':<22} "
          f"{'n':>6} {'input_avg':>10} {'read_avg':>10} {'total_avg':>10} {'read%':>7}")
    for key, events in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        rt, template, version, model, collector, semantics = key
        n = len(events)
        total, share = input_metrics(events, semantics)
        small = "  <-- small sample" if n < min_events else ""
        print(f"{rt:<22} {template + '/' + version:<33} {model:<22} {collector + '/' + semantics:<22} "
              f"{n:>6} {fmt(average(events, 'input_tokens'))} "
              f"{fmt(average(events, 'cache_read_tokens'))} {fmt(total)} {fmt(share, 7, 1)}{small}")
    print("\ninput_avg/read_avg: raw field means where present; total_avg/read%: known, complete input accounting only.")

    sessions = defaultdict(set)
    for key, events in groups.items():
        for event in events:
            metadata = event.get("metadata")
            session_id = metadata.get("session_id") if isinstance(metadata, dict) else None
            if isinstance(session_id, str) and session_id:
                sessions[key[0]].add(session_id)
    if sessions:
        print("\nDistinct known sessions per request_type (only events with session IDs):")
        for request_type, ids in sorted(sessions.items()):
            print(f"  {request_type:<22} {len(ids):>4}")


def compare_baselines(groups: Groups, regression_path: Path) -> None:
    if not regression_path.is_file():
        print("\n[skip] regression snapshot not found:", regression_path)
        return
    spec = json.loads(regression_path.read_text(encoding="utf-8"))
    scope = spec.get("baseline_scope", {})
    print("\n=== historical snapshot (descriptive only; not a quality or savings test) ===")
    for case in spec.get("cases", []):
        if not case.get("enabled"):
            continue
        case_id = case["id"]
        baseline = case.get("baseline") or {}
        b_in, b_read = baseline.get("input_tokens"), baseline.get("cache_read_tokens")
        if b_in is None or b_read is None:
            print(f"[no-baseline] {case_id}")
            continue
        key = (case.get("request_type"), case.get("template_id"), scope.get("template_version"),
               scope.get("model"), scope.get("collector_version"), scope.get("cache_semantics"))
        events = groups.get(key)
        if not events or key[-1] != "deepseek-legacy":
            print(f"[no-matching-data] {case_id} (requires matching historical model/template/collector)")
            continue
        cutoff = scope.get("snapshot_date")
        if cutoff:
            # The snapshot day may be partial; exclude it as well as older days.
            events = [event for event in events if str(event.get("timestamp") or "")[:10] > cutoff]
        if not events:
            print(f"[no-post-snapshot-data] {case_id}")
            continue
        total, share = input_metrics(events, key[-1])
        b_total = b_in + b_read
        if total is None or share is None or not b_total:
            print(f"[no-comparable-input] {case_id}")
            continue
        print(f"{case_id:<28} n={len(events):>5}  total avg={total:>9,.0f}  read={share:5.1f}%  "
              f"vs snapshot: {total - b_total:+,.0f} tokens, {share - 100 * b_read / b_total:+.1f} pp")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--events-dir", type=Path, help="Daily JSONL files (default: project .llm/prompt-cache/events)")
    source.add_argument("--events-file", type=Path, help="Read one JSONL file instead of the daily files; never merge sources")
    parser.add_argument("--since", help="Only events dated on or after YYYY-MM-DD, per event timestamp")
    parser.add_argument("--regression", type=Path, default=CACHE_ROOT / "regression-cases.json", help="Historical snapshot JSON")
    parser.add_argument("--model", action="append", help="Restrict to a model (repeatable); default: all models")
    parser.add_argument("--no-baseline", action="store_true", help="Skip the historical snapshot")
    parser.add_argument("--min-events", type=int, default=10, help="Warn when a group has fewer events than this")
    args = parser.parse_args()

    if args.events_file is not None:
        if not args.events_file.is_file():
            parser.error(f"event file not found: {args.events_file}")
        paths = [args.events_file]
    else:
        paths = sorted((args.events_dir or CACHE_ROOT / "events").glob("*.jsonl"))
    events = load_events(paths, args.since)
    groups = defaultdict(list)
    models = set(args.model or [])
    for event in events:
        key = group_key(event)
        if not models or key[3] in models:
            groups[key].append(event)
    selected = sum(map(len, groups.values()))
    print(f"events: {selected} of {len(events)} (models: {', '.join(sorted(models)) or 'all'})")
    report(groups, args.min_events)
    if not args.no_baseline:
        compare_baselines(groups, args.regression)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
