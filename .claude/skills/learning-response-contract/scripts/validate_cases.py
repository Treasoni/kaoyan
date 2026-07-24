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
