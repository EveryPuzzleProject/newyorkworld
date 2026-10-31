#!/usr/bin/env python3
"""Give 1917 printings a World number from the one dated anchor we have.

The Tacoma Daily Ledger of 1917-07-22 prints a "Cross-Word Puzzle Solutions" box from The World
Magazine, each solution under the date the World published its puzzle: "July 1" is the puzzle
Tacoma printed 07-15 and "June 17" the one it printed 07-01, so Tacoma ran each puzzle two weeks
after the World. The Boston Globe and the Minneapolis Journal ran each puzzle two weeks before
Tacoma (matched copies), so their 1917 dates are the World's own. This script sets world_no on
1917 printings accordingly: Globe/Journal date, or Tacoma date minus two weeks, applied to every
copy of the same puzzle_key; it never overrides a printed number. Re-run after an intake.

Stops at STOP (1918-01-01): the Globe's date is the World's only in 1917. From 1918 the Globe ran increasingly late
(T Campbell: its 1920-05-02 puzzle is the World's 1919-10-12; docs/CAMPBELL-CROSSCHECK.md), so no World number is
inferred for Globe rows after 1917-12-30.
"""
import datetime as dt
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from record import printings, number_of, solution_only  # noqa: E402

STOP = "1918-01-01"
HOW = "(anchor: the World Magazine solutions box on Tacoma 1917-07-22 gives World dates two weeks before Tacoma's; the Globe and the Journal ran two weeks before Tacoma)"
rows = printings()
anchor = {}
for r in rows:
    if r["world_no_printed"] or solution_only(r) or r["date"] < "1917" or r["date"] >= STOP:
        continue
    if r["paper"] in ("boston-globe", "minneapolis-journal"):
        wd, how = r["date"], f"World date = the {r['paper']} date"
    elif r["paper"] == "tacoma-daily-ledger":
        wd, how = (dt.date.fromisoformat(r["date"]) - dt.timedelta(weeks=2)).isoformat(), "World date = the Tacoma date minus two weeks"
    else:
        continue
    k = r["puzzle_key"] or r["file"]
    if k not in anchor or r["paper"] != "tacoma-daily-ledger":
        anchor[k] = (wd, how)
n = 0
for r in rows:
    if r["world_no"] or r["world_no_printed"] or r["date"] < "1917" or r["date"] >= STOP or solution_only(r):
        continue
    k = r["puzzle_key"] or r["file"]
    if k in anchor:
        wd, how = anchor[k]
        subprocess.run([sys.executable, str(ROOT / "tools" / "record.py"), "add", r["file"], f"world_no={number_of(dt.date.fromisoformat(wd))}",
                        f"match=inferred: {how} {HOW}; " + (r["match"] or "")], capture_output=True)
        n += 1
print(n, "printings given a World number")
