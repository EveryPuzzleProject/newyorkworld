#!/usr/bin/env python3
"""World numbers for the Minneapolis Journal's run from 1915-11-21 to 1917-01-28, by inference.

In January 1917 the Journal printed each puzzle on the World's own date (its December 1916
puzzles are the ones the Los Angeles Tribune ran eight weeks later, and the Boston Globe, which ran
on the World's date per the World Magazine solutions box of 1917-07-22, keys to the same chain).
From the day the Journal resumed FUN's puzzle, 1915-11-21, every week's page answers the week
before (printings.tsv `continuity`), and on the two Sundays it printed comics instead (1916-08-13,
09-10) the syndicate's solution still ran the next week, so the Journal skipped those World
puzzles rather than falling behind. A zero offset in January 1917 therefore holds back to
1915-11-21: World No. = the number of the Journal's own date. Marked inferred on every row.
The exception is November 1916, when the Journal ran a week late: tools/world_dates_copies.py corrects it.

Not covered: 1915-01-17 to 07-25, where the offset is three weeks at No. 54 and grows by one for
each Sunday the Journal skipped, with three February Sundays unknown: a range, not a number.
"""
import datetime as dt
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from record import printings, number_of, solution_only  # noqa: E402

HOW = ("inferred: World No. = the Journal's own date. The Journal was on the World's date in January 1917 "
       "(its December 1916 puzzles match the LA Tribune eight weeks later and the Globe's World-dated chain), "
       "and every week from 1915-11-21 answers the week before, so the zero offset holds back to 1915-11-21")
n = 0
for r in printings():
    if r["paper"] != "minneapolis-journal" or r["world_no"] or r["world_no_printed"] or solution_only(r):
        continue
    if not ("1915-11-21" <= r["date"] <= "1917-01-28"):
        continue
    subprocess.run([sys.executable, str(ROOT / "tools" / "record.py"), "add", r["file"],
                    f"world_no={number_of(dt.date.fromisoformat(r['date']))}", f"match={HOW}; " + (r["match"] or "")], capture_output=True)
    n += 1
print(n, "Journal printings given a World number")
