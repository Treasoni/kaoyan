# -*- coding: utf-8 -*-
import re

VAULT = "/Users/zhqznc/Documents/考研复习"
path = VAULT + "/线性代数/每日一背.md"
entry_path = VAULT + "/workspace/_tmp_entry.md"

with open(path, encoding="utf-8") as f:
    text = f.read()
with open(entry_path, encoding="utf-8") as f:
    entry = f.read().rstrip("\n")

lines = text.split("\n")

# frontmatter boundaries
assert lines[0].strip() == "---"
fm_end = None
for i in range(1, len(lines)):
    if lines[i].strip() == "---":
        fm_end = i
        break
assert fm_end is not None
body_start = fm_end + 1

# locate index table region
idx_start = None
for i in range(body_start, len(lines)):
    if lines[i].strip() == "## 📋 条目索引":
        idx_start = i
        break
assert idx_start is not None, "index heading not found"
idx_end = None
for j in range(idx_start + 1, len(lines)):
    if lines[j].strip() == "---":
        idx_end = j
        break
assert idx_end is not None, "index end not found"

# 1) renumber index rows (first cell) within region only
row_re = re.compile(r"^\| (\d+) \|(.*)$")
for i in range(idx_start, idx_end):
    m = row_re.match(lines[i])
    if m:
        n = int(m.group(1))
        if n >= 3:
            lines[i] = "| %d |%s" % (n + 1, m.group(2))

# 2) renumber titles + cross-refs in body (skip frontmatter)
title_re = re.compile(r"^### (\d+)\. ")
ref_re = re.compile(r"第 (\d+) 条")

def ref_repl(mm):
    n = int(mm.group(1))
    # all entry cross-refs are >=6; "第 3 条" (三点检查法) and any 1/2 must stay
    if n >= 4:
        return "第 %d 条" % (n + 1)
    return mm.group(0)

for i in range(body_start, len(lines)):
    ln = lines[i]
    m = title_re.match(ln)
    if m:
        n = int(m.group(1))
        if n >= 3:
            ln = "### %d. " % (n + 1) + ln[len(m.group(0)):]
    ln = ref_re.sub(ref_repl, ln)
    lines[i] = ln

# 3) insert index row for new entry #3 after row "| 2 |"
insert_row = ("| 3 | 严格三角矩阵与幂零矩阵：$\\lambda E+N$ 拆分法与幂零求逆 ★★★ "
              "| 第二章 §7 常见的特殊矩阵 | — |")
done_row = False
for i in range(idx_start, idx_end):
    if lines[i].startswith("| 2 |"):
        lines.insert(i + 1, insert_row)
        done_row = True
        break
assert done_row, "index row 2 not found"

# 4) insert new entry body before renumbered entry 4 heading
pos = None
for i in range(len(lines)):
    if lines[i].startswith("### 4. 实反对称矩阵"):
        pos = i
        break
assert pos is not None, "entry 4 heading not found"
lines[pos:pos] = entry.split("\n") + ["", "---", ""]

# 5) frontmatter updated / updated_prev
NEW_UPDATED = ("updated: 2026-10-19 (新增第二章 §7 严格三角矩阵与幂零矩阵：λE+N 拆分法与幂零求逆；"
               "插为第 3 条，原第 3–18 条顺延为 4–19，并同步修正正文「第 N 条」交叉引用)")
cur_idx = prev_idx = None
for i in range(1, fm_end):
    if lines[i].startswith("updated_prev:"):
        prev_idx = i
    elif lines[i].startswith("updated:"):
        cur_idx = i
assert cur_idx is not None and prev_idx is not None
old_cur = lines[cur_idx]
lines[cur_idx] = NEW_UPDATED
lines[prev_idx] = "updated_prev: " + old_cur[len("updated: "):]

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("OK: wrote", path)
