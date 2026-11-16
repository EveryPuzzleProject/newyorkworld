#!/usr/bin/env python3
"""World numbers for 1915's copies, from the Milwaukee Sentinel's FUN pages, by inference.

The Milwaukee Sentinel carried the World's FUN section itself, on the World's own Sundays: in
1914 its grids carry FUN's numbers week by week (No. 47 on 1914-11-22 ... No. 54 on 1915-01-10,
one a week), and its holiday puzzles fall on the holidays (Christmas 1914-12-20, New Year 12-27,
the valentine whose solution it printed on 1915-02-21). Its 1915 pages (GenealogyBank, saved by
Alex DeJarnatt, 2026-11-16) are FUN's own pages ("FUN." in the header, FUN's page numbers).
So a Sentinel puzzle's World date is the Sentinel's own date: World No. = the number of that date.

The Minneapolis Journal printed the same puzzle on the same Sunday as the Sentinel at every
overlap from 1915-01-24 to 07-25 (first clue and shape; thirteen Sundays), so a Journal page of
those months also takes the number of its own date. The exception is No. 54, which the Sentinel
printed on 01-10 and the Journal a week late on 01-17 (it skipped 01-10). That overturns the old
reading (world_dates_1916.py) that the Journal ran three to six weeks behind the World in 1915:
the gap was in the weekly count, from the Sundays the World itself ran no crossword in 1914.

Printed numbers stay as printed, so the Sentinel's 01-03 puzzle is No. 53 (its 01-10 box is
labelled the solution to No. 53) and 01-10 is No. 54; the count's Nos. 55 and 56 (01-03, 01-10 by
the count) are empty weeks. From 01-17 on, a 1915 number is a convenience index for a date.
Marked inferred on every row. Re-run after an intake.
"""
import datetime as dt
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from record import printings, number_of, solution_only  # noqa: E402

FROM, TO = "1915-01-17", "1915-11-14"
SENTINEL = ("inferred: World No. = the Sentinel's own date. The Milwaukee Sentinel carried FUN itself on the "
            "World's Sundays (its grids follow FUN's numbers week by week to No. 54 on 1915-01-10); "
            "tools/world_dates_1915.py")
JOURNAL = ("inferred: World No. = the Journal's own date. In 1915 the Journal printed the same puzzle on the same "
           "Sunday as the Milwaukee Sentinel at every overlap from 01-24 to 07-25, and the Sentinel ran FUN on the "
           "World's date; tools/world_dates_1915.py")


def add(r: dict, no: int, how: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "tools" / "record.py"), "add", r["file"], f"world_no={no}",
                    f"match={how}"], capture_output=True)


n = {"milwaukee-sentinel": 0, "minneapolis-journal": 0}
for r in printings():
    if r["paper"] not in n or r["world_no_printed"] or solution_only(r):
        continue
    if r["paper"] == "milwaukee-sentinel" and r["date"] == "1915-01-03":
        if r["world_no"] != "53":
            add(r, 53, "the Sentinel's 1915-01-10 page labels its solution to this puzzle No. 53")
            n[r["paper"]] += 1
        continue
    if not (FROM <= r["date"] <= TO) or (r["world_no"] and not r["match"].startswith("inferred")):
        continue
    no = number_of(dt.date.fromisoformat(r["date"]))
    if r["world_no"] != str(no):
        add(r, no, SENTINEL if r["paper"] == "milwaukee-sentinel" else JOURNAL)
        n[r["paper"]] += 1
print(n["milwaukee-sentinel"], "Sentinel and", n["minneapolis-journal"], "Journal printings given a World number")
