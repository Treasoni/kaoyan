#!/usr/bin/env python3
"""Summarize sanitized LLM usage events and compare them to regression baselines.

Reads .llm/prompt-cache/events/*.jsonl, groups events by request_type + model,
and reports cache-read ratios under the DeepSeek-compat endpoint semantics
(input_tokens ~= uncached portion, cache_read_tokens ~= cached portion;
hit rate = cache_read / (input + cache_read)).

Also loads regression-cases.json and prints a before/after delta for each
enabled case whose request_type has real events.

Privacy: reads metadata only. It never prints raw prompts or model output.
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[3]   # <project>/
DEFAULT_EVENTS_DIR = DEFAULT_ROOT / ".llm" / "prompt-cache" / "events"
DEFAULT_REGRESSION = DEFAULT_ROOT / ".llm" / "prompt-cache" / "regression-cases.json"
DEFAULT_MODELS = {"deepseek-v4-flash", "deepseek-v4-pro"}


def load_events(events_dir: Path, since: str | None) -> list[dict]:
    out: list[dict] = []
    for f in sorted(glob.glob(str(events_dir / "*.jsonl"))):
        if since and Path(f).stem < since:
            continue
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if not (
                (obj.get("input_tokens") or 0)
                or (obj.get("cache_read_tokens") or 0)
                or (obj.get("cache_write_tokens") or 0)
                or (obj.get("output_tokens") or 0)
            ):
                continue
            out.append(obj)
    return out


def hit_rate(rs: list[dict]) -> float:
    tin = sum(r.get("input_tokens", 0) or 0 for r in rs)
    tcr = sum(r.get("cache_read_tokens", 0) or 0 for r in rs)
    return tcr / (tin + tcr) if (tin + tcr) else 0.0


def report(events: list[dict], model_filter: set[str], min_events: int) -> None:
    # Zero-token residue check (should normally be empty after F1 fix).
    zero = sum(
        1
        for r in events
        if not (
            (r.get("input_tokens") or 0)
            or (r.get("cache_read_tokens") or 0)
            or (r.get("cache_write_tokens") or 0)
            or (r.get("output_tokens") or 0)
        )
    )
    if zero:
        print(f"[warn] {zero} all-zero-token events present (run extract-usage-events.py to purge)")

    groups: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for r in events:
        if model_filter and r.get("model") not in model_filter:
            continue
        groups[(r.get("request_type", "?"), r.get("model", "?"))].append(r)

    kept = sum(len(rs) for rs in groups.values())
    dropped = len(events) - kept
    label = f"events: {kept} total (models: {', '.join(sorted(model_filter)) or 'all'})"
    if dropped:
        label += f" (+{dropped} events of other models excluded)"
    print(label)
    print(f"\n{'request_type':<22} {'model':<16} {'n':>6} {'in_avg':>9} {'cr_avg':>10} {'hit%':>7}")
    print("-" * 74)
    for (rt, model), rs in sorted(
        groups.items(), key=lambda kv: -sum(x.get("input_tokens", 0) or 0 for x in kv[1])
    ):
        n = len(rs)
        in_avg = sum(r.get("input_tokens", 0) or 0 for r in rs) / n
        cr_avg = sum(r.get("cache_read_tokens", 0) or 0 for r in rs) / n
        hit = hit_rate(rs) * 100
        flag = "  <-- small sample" if n < min_events else ""
        print(f"{rt:<22} {model:<16} {n:>6} {in_avg:>9,.0f} {cr_avg:>10,.0f} {hit:>6.1f}%{flag}")

    # Sessions per type (avoid the "n=events called sessions" confusion).
    sess = collections.defaultdict(set)
    for r in events:
        if model_filter and r.get("model") not in model_filter:
            continue
        sess[r.get("request_type", "?")].add(r.get("input_reference"))
    print("\nsessions per request_type:")
    for rt, s in sorted(sess.items()):
        print(f"  {rt:<22} {len(s):>4}")


def compare_baselines(events: list[dict], regression_path: Path, model_filter: set[str]) -> None:
    if not regression_path.exists():
        print("\n[skip] regression-cases.json not found:", regression_path)
        return
    spec = json.loads(regression_path.read_text(encoding="utf-8"))
    print("\n=== regression baseline delta ===")
    any_delta = False
    for case in spec.get("cases", []):
        rt = case.get("request_type")
        if not case.get("enabled"):
            continue
        rs = [r for r in events if r.get("request_type") == rt and (not model_filter or r.get("model") in model_filter)]
        if not rs:
            print(f"[no-data] {case.get('id'):<28} request_type={rt:<22} baseline present: {bool(case.get('baseline', {}).get('input_tokens') is not None)}")
            continue
        any_delta = True
        n = len(rs)
        in_avg = sum(r.get("input_tokens", 0) or 0 for r in rs) / n
        cr_avg = sum(r.get("cache_read_tokens", 0) or 0 for r in rs) / n
        hit = hit_rate(rs) * 100
        base = case.get("baseline", {}) or {}
        b_in = base.get("input_tokens")
        b_cr = base.get("cache_read_tokens")
        print(f"{case.get('id'):<28} n={n:>5}  in={in_avg:>8,.0f}  cr={cr_avg:>10,.0f}  hit={hit:>5.1f}%")
        if b_in is not None and b_cr is not None:
            b_hit = b_cr / (b_in + b_cr) * 100 if (b_in + b_cr) else 0
            print(f"{'':<28}    baseline       in={b_in:>8,.0f}  cr={b_cr:>10,.0f}  hit={b_hit:>5.1f}%")
            print(f"{'':<28}    delta          in={(in_avg-b_in):>+8,.0f}  cr={(cr_avg-b_cr):>+10,.0f}  hit={(hit-b_hit):>+5.1f}pp")
    if not any_delta:
        print("(no baseline comparison available for enabled cases)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events-dir", default=None, help="Events dir (default: <project>/.llm/prompt-cache/events)")
    parser.add_argument("--since", default=None, help="Only days >= YYYY-MM-DD")
    parser.add_argument("--regression", default=None, help="Path to regression-cases.json")
    parser.add_argument("--model", action="append", help="Restrict to a model (repeatable). Default: deepseek-v4-flash + deepseek-v4-pro")
    parser.add_argument("--no-baseline", action="store_true", help="Skip regression baseline comparison")
    parser.add_argument("--min-events", type=int, default=10, help="Warn when a group has fewer events than this")
    args = parser.parse_args()

    events_dir = Path(args.events_dir).resolve() if args.events_dir else DEFAULT_EVENTS_DIR
    regression = Path(args.regression).resolve() if args.regression else DEFAULT_REGRESSION
    model_filter = set(args.model) if args.model else DEFAULT_MODELS

    events = load_events(events_dir, args.since)
    report(events, model_filter, args.min_events)
    if not args.no_baseline:
        compare_baselines(events, regression, model_filter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
