#!/usr/bin/env python3
"""SessionEnd hook: auto-extract LLM usage events for the finished session.

Reads the Claude Code hook input JSON from stdin, resolves the session
transcript path, and runs `.llm/prompt-cache/scripts/extract-usage-events.py`
on just that transcript (single-file mode). Writes sanitized events under
`.llm/prompt-cache/events/`.

Deliberately prints nothing and discards the extractor's stdout/stderr so the
hook does not inject output into the next session.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent          # <root>/.claude/hooks
PROJECT_ROOT = HOOK_DIR.parents[1]                   # <root>
EXTRACTOR = PROJECT_ROOT / ".llm" / "prompt-cache" / "scripts" / "extract-usage-events.py"


def main() -> int:
    transcript_path = None
    try:
        data = json.load(sys.stdin)
        transcript_path = data.get("transcript_path")
    except Exception:
        transcript_path = None

    if not EXTRACTOR.exists():
        return 0

    cmd = [sys.executable, str(EXTRACTOR)]
    if transcript_path and os.path.isfile(transcript_path):
        cmd += ["--transcript", transcript_path]
    else:
        # Fallback: catch up on today's transcripts.
        cmd += ["--since", date.today().isoformat()]

    subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        timeout=60,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
