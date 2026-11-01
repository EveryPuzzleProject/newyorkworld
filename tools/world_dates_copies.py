#!/usr/bin/env python3
"""World numbers for every partner copy of 1916-17, from the order the papers' runs agree on.

world_dates_1916.py numbers the Journal by its own date and world_dates_1917.py numbers Tacoma by
its date minus two weeks. Both are right most of the time, and the copies left without a number
hide what the other papers show:

- The Pittsburgh Press ran one week behind the World from 1916-06-11 to 1917-02-18, every week.
  It prints five puzzles the Journal does not: 1916-08-20 (the Journal's comics Sunday 08-13),
  09-03 and 09-17, 12-03, 1917-02-11. They take the numbers between their neighbours.
- The Journal printed 1916-10-29's puzzle again on 11-05, so it ran a week late for three weeks
  (Nos. 151-153 on 11-12..11-26) and dropped No. 154 to catch up. Fort Wayne's 1916-11-19 copy of
  the Journal's 11-26 puzzle proves it: a copy can't precede the World.
- Tacoma's lag was one week, not two, until 1917-02-04, so its January rows were one number low.
- Los Angeles 1917-03-11 is the puzzle whose solution Pittsburgh and Tacoma printed on 01-28, and
  Shreveport 1917-03-04 the one Shreveport answers on 03-11: Nos. 161 and 166.

A copy takes the number of the Journal or Globe copy with the same first clue within WINDOW weeks
(README: first clue and shape tie a copy). The same clue further apart is a possible rerun, not a
copy, and is left alone: docs/CHAINS.md lists those. Printed numbers are never touched.
Re-run after an intake.
"""
import datetime as dt
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from record import printings, rebuild_all, searches, solution_only, status  # noqa: E402

START, STOP = "1915-11-01", "1918-01-01"
WINDOW = 9  # weeks; the Los Angeles Tribune ran up to eight behind
REFERENCE = ("minneapolis-journal", "boston-globe")

# The Journal's copies that its own date numbers wrongly (see above).
MOVED = {"1916-11-05": 150, "1916-11-12": 151, "1916-11-19": 152, "1916-11-26": 153}
MOVED_HOW = ("inferred: the Journal printed its 10-29 puzzle again on 11-05 and ran a week late until it dropped No. 154; "
             "Fort Wayne printed the 11-26 puzzle on 11-19, and Pittsburgh ran every one of them a week behind the World")
# Puzzles with no reference copy, with the number their place in a partner's run gives them.
PLACED = {"partoftheequipme": (139, "between Nos. 138 and 140 in the Pittsburgh Press's run, 1916-08-20"),
          "thedriedstalk": (141, "Pittsburgh ran it 1916-09-03, a week behind the World, between Nos. 140 and 142; the Journal's 08-27 copy has no readable first clue"),
          "apunctuationmark": (143, "between Nos. 142 and 144 in the Pittsburgh Press's run, 1916-09-17"),
          "amusicalcompositi": (154, "between Nos. 153 and 155 in the Pittsburgh Press's run, 1916-12-03"),
          "toshatter": (161, "between Nos. 160 and 162 in the Los Angeles Tribune's run, 1917-03-11; Pittsburgh and Tacoma print its solution 1917-01-28"),
          "ajapanesemusical": (164, "between Nos. 163 and 165 in the Pittsburgh Press's run, 1917-02-11"),
          "aquickinclinatio": (166, "before No. 167 in the Shreveport Times's run, 1917-03-04")}
# A copy outside the window, checked by eye: same grid, same numbering and first clue (links.tsv note).
LATE = {("los-angeles-tribune", "1916-10-22"): (135, "same grid and first clue as minneapolis-journal 1916-07-16, compared on the scans; 14 weeks behind, far later than Los Angeles's usual lag")}
# solution_of values that named a puzzle by key before it had a number.
KEYS = {"deaf-1916-09": 144, "inplaceof-1916-09": 145, "santa-claus": 159, "nugent-meagre": 160, "botjer-aromatic": 162,
        "johnson-koto": 164, "globe-kale": 167}


def clue(s: str) -> str:
    s = re.sub(r"\(.*", "", s.lower())
    s = re.sub(r"horizontal|upper left\w*( section| diagonal)?|outer part|center figure|inner part", "", s)
    s = re.sub(r"^[^a-z]*(\d+\s*(-|to)\s*\??\d*)?", "", s)
    return re.sub(r"[^a-z]", "", s)[:20]


def same(a: str, b: str) -> bool:
    m = min(len(a), len(b))
    if m < 4:
        return False
    x, y = a[:m], b[:m]
    return sorted(x) == sorted(y) or difflib.SequenceMatcher(None, x, y).ratio() >= 0.9  # meager/meagre, weal/meal


def weeks(a: dict, b: dict) -> int:
    return abs((dt.date.fromisoformat(a["date"]) - dt.date.fromisoformat(b["date"])).days) // 7


rows = printings()
span = [r for r in rows if START <= r["date"] < STOP and r["paper"] in REFERENCE + (
    "pittsburgh-press", "tacoma-daily-ledger", "los-angeles-tribune", "shreveport-times", "new-orleans-states",
    "fort-wayne-journal-gazette", "seattle-post-intelligencer", "salt-lake-telegram") and not solution_only(r)]
changed = 0


def number(r: dict, n: int, how: str) -> None:
    global changed
    if r["world_no_printed"] or r["world_no"] == str(n):
        return
    was = f" (was No. {r['world_no']})" if r["world_no"] else ""
    r["world_no"], r["puzzle_key"], r["match"] = str(n), "", how + was
    changed += 1
    print(f"{r['paper']} {r['date']}: No. {n}{was}")


for r in span:
    if (r["paper"], r["date"]) in LATE:
        number(r, *LATE[(r["paper"], r["date"])])
    elif r["paper"] == "minneapolis-journal" and r["date"] in MOVED:
        number(r, MOVED[r["date"]], MOVED_HOW)
    elif r["paper"] == "minneapolis-journal" and r["date"] == "1916-08-27":
        number(r, 141, r["match"] or "inferred")
refs = [r for r in span if r["world_no"] and clue(r["fingerprint"])
        and (r["paper"] in REFERENCE or (r["paper"] == "tacoma-daily-ledger" and r["date"] >= "1917-02-18"))]  # Tacoma holds Nos. 183 and 185 alone
for key, (n, how) in PLACED.items():
    for r in span:
        if same(clue(r["fingerprint"]), key):
            number(r, n, f"inferred: {how}")
placed = [r for r in span if any(same(clue(r["fingerprint"]), k) for k in PLACED)]
for r in span:
    if r["paper"] in REFERENCE or r in placed:
        continue
    k = clue(r["fingerprint"])
    near = [x for x in refs if same(k, clue(x["fingerprint"])) and weeks(r, x) <= WINDOW]
    if near:
        x = min(near, key=lambda x: weeks(r, x))
        number(r, int(x["world_no"]), f"same first clue as {x['paper']} {x['date']}")
for r in rows:
    r["solution_of"] = str(KEYS.get(r["solution_of"], r["solution_of"]))
rebuild_all(rows, searches(), status())
print(changed, "copies numbered")
print("left without a number:", *[f"{r['paper']} {r['date']}" for r in span if not r["world_no"]], sep="\n  ")
