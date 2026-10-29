#!/usr/bin/env python3
"""List unrecorded pages with each one's previous found page of the same paper (for an indexing brief)."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from record import parse_file, printings, ROOT  # noqa: E402

rows = printings()
new = [l.split("\t")[0] for l in subprocess.run([sys.executable, str(ROOT / "tools" / "record.py"), "new"], capture_output=True, text=True).stdout.splitlines()
       if l.strip() and not l.startswith("??") and l != "nothing new"]
seen = []
for f in sorted(new, key=lambda f: parse_file(f)["date"]):
    info = parse_file(f); d, paper = info["date"], info["paper"]
    cands = [r for r in rows if r["paper"] == paper and r["date"] < d and not r["file"].startswith("clip:")
             and not r["notes"].lower().startswith(("no new puzzle", "no crossword"))]
    prev = max(cands, key=lambda r: r["date"], default=None)
    earlier_new = [(g, gi) for g, gi in seen if gi["paper"] == paper and gi["date"] < d]
    if earlier_new and (prev is None or earlier_new[-1][1]["date"] > prev["date"]):
        print(f"- {f}. Previous found page: the {earlier_new[-1][1]['date']} page in this same batch (use what you index there).")
    elif prev:
        print(f"- {f}. Previous found page {prev['date']}: {prev['shape']}; first clue {prev['fingerprint']}" + (f"; world_no {prev['world_no']}" if prev["world_no"] else ""))
    else:
        print(f"- {f}. No previous found page.")
    seen.append((f, info))
