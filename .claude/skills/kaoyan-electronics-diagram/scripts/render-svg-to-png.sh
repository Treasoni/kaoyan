#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 4 ]; then
  echo "Usage: render-svg-to-png.sh <input.svg> <output.png> [width] [height]" >&2
  exit 2
fi

input_svg="$1"
output_png="$2"
canvas_width="${3:-1600}"
canvas_height="${4:-1120}"

if [ ! -f "$input_svg" ]; then
  echo "Input SVG not found: $input_svg" >&2
  exit 1
fi

case "$input_svg" in
  /*) absolute_svg="$input_svg" ;;
  *) absolute_svg="$(cd "$(dirname "$input_svg")" && pwd -P)/$(basename "$input_svg")" ;;
esac

output_dir="$(dirname "$output_png")"
mkdir -p "$output_dir"

chrome_bin=""
if [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  chrome_bin="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif command -v google-chrome >/dev/null 2>&1; then
  chrome_bin="$(command -v google-chrome)"
elif command -v chromium >/dev/null 2>&1; then
  chrome_bin="$(command -v chromium)"
elif command -v chromium-browser >/dev/null 2>&1; then
  chrome_bin="$(command -v chromium-browser)"
fi

if [ -z "$chrome_bin" ]; then
  echo "Chrome/Chromium is required for stable SVG rendering. Do not use qlmanage as final export; it may crop wide diagrams." >&2
  exit 1
fi

file_url="$(python3 - "$absolute_svg" <<'PY'
from pathlib import Path
import sys

print(Path(sys.argv[1]).resolve().as_uri())
PY
)"

"$chrome_bin" \
  --headless \
  --disable-gpu \
  --screenshot="$output_png" \
  --window-size="${canvas_width},${canvas_height}" \
  "$file_url" >/dev/null 2>&1

if [ ! -s "$output_png" ]; then
  echo "PNG export failed or produced an empty file: $output_png" >&2
  exit 1
fi

file "$output_png"
