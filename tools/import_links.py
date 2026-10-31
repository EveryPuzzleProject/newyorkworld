#!/usr/bin/env python3
"""Import a link checker's JSON (docs/CHAIN-BRIEF.md) into links.tsv.

    python tools/import_links.py out_A.json --by "Sonnet subagent, 2026-10-31" [--kind ID=dated ...] [--next ID=FILE ...]

--kind sets a pair's evidence kind (default grid); --next names the puzzle that follows when it
isn't the solution page's own. Pairs whose JSON has no verdict are skipped and reported.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ap = argparse.ArgumentParser()
ap.add_argument("json")
ap.add_argument("--by", required=True)
ap.add_argument("--kind", action="append", default=[])
ap.add_argument("--next", action="append", default=[])
args = ap.parse_args()
kinds = dict(k.split("=", 1) for k in args.kind)
nexts = dict(k.split("=", 1) for k in args.next)
for o in json.loads(Path(args.json).read_text(encoding="utf-8")):
    v = str(o.get("verdict", "")).strip().lower()
    if v not in ("yes", "no", "unclear"):
        print(f"?? {o.get('id')}: {v!r}"); continue
    conf = str(o.get("confidence", "")).strip()
    note = (f"({conf}) " if conf and conf.lower() != "high" else "") + str(o.get("note", "")).strip()
    cmd = [sys.executable, str(ROOT / "tools" / "record.py"), "link", o["puzzle_page"], o["solution_page"], f"kind={kinds.get(o['id'], 'grid')}",
           f"verdict={v}", f"checked_by={args.by}", f"note={note}"]
    if o["id"] in nexts:
        cmd.append(f"next_page={nexts[o['id']]}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(("ok " if r.returncode == 0 else "!! ") + o["id"], v, "" if r.returncode == 0 else r.stderr[-200:])
