#!/usr/bin/env python3
"""The longest unbroken chains of World FUN puzzles, from every page we hold (docs/CHAINS.md).

A puzzle is an inferred World Sunday (world_no is its index) or, where there is none yet, a page.
The puzzles stand in one order: 1914-02-01 to 1914-12-27 (Nos. 7-54), the Journal's undated pages of
1915, 1915-11-21 to 1917-12-30 (Nos. 101-211), the Globe's Sundays of 1918 on. Each adjacent pair is linked if some page's printed solution answers the earlier puzzle
and the later puzzle comes next on that paper's run. The evidence is `continuity` and `solution_of`
in printings.tsv, links.tsv, or two printed consecutive numbers. A chain is a maximal run of linked
puzzles; every other adjacent pair is a break, with its reason and the page that would join it.

Written by `record.py rebuild`:
  chains.tsv        one row per chain: span, anchor, links
  chain_breaks.tsv  one row per break: between what, why, which page joins it
  chain_pages.tsv   every held page: its chain, or why it has none
  reruns.tsv        same first clue more than RERUN_WEEKS apart: candidates for one puzzle printed twice

    python tools/chains.py          # print the chains and breaks
"""
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from record import LAGS, links, printings, searches, solution_only, sunday_of, write_tsv  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CHAIN_COLS = ["chain", "first", "last", "first_date", "last_date", "puzzles", "verified_links", "tentative_links", "empty_slots", "anchor", "standing"]
BREAK_COLS = ["break", "after", "before", "after_date", "before_date", "reason", "detail", "want_paper", "want_date", "want_why"]
PAGE_COLS = ["file", "paper", "date", "puzzle", "chain", "why_none"]
OTHER_SERIES = ("boston-globe-saturday", "boston-globe-wednesday", "boston-globe-other-days")
LAST_PRINTED = 54     # the last number the World printed: a gap up to here is a puzzle that exists
WORLD_END = 211       # 1917-12-30: past this the Globe's date is not the World's (docs/CAMPBELL-CROSSCHECK.md)
BOX = 182             # the World Magazine solutions box dates Nos. 182, 183 and 185
DEAD = ("no-hit", "not-carried", "missing-from-scans")
RERUN_COLS = ["clue_key", "first_paper", "first_date", "first_shape", "later_paper", "later_date", "later_shape", "weeks"]
RERUN_WEEKS = 26
TENTATIVE = "tentative:"


def is_tentative(evidence: list[str]) -> bool:
    """A link is tentative if nothing but tentative evidence holds it."""
    return all(e.startswith(TENTATIVE) for e in evidence)


def label(node) -> str:
    """A puzzle's name: its World date in gxd's form, the number only in brackets (the series is dated, not numbered).
    A puzzle with no World date yet goes by the page it's on: paper and printing date."""
    return f"nyw{sunday_of(node).isoformat()} (No. {node})" if isinstance(node, int) else f"{node[0]} {node[1]}"


def verdict(c: str) -> tuple[str, str]:
    """A continuity value's (word, date compared against)."""
    vs = ""
    if c.startswith("vs "):
        vs, c = c[3:13], c[14:]
    return c.split(":")[0].split("(")[0].strip(), vs


def node_of(r: dict):
    return int(r["world_no"]) if r["world_no"] else (r["paper"], r["date"])


def build(pr: list[dict], li: list[dict]):
    """order, nodes {puzzle: pages}, edges {(a, b): [evidence]}, seen {b: [(word, page)]}: every non-link verdict."""
    main = [r for r in pr if r["paper"] not in OTHER_SERIES]
    nodes: dict = {}
    for r in main:
        if not solution_only(r):
            nodes.setdefault(node_of(r), []).append(r)

    def key(n):
        if isinstance(n, int):
            return (0 if n <= LAST_PRINTED else 2, n, "")
        return (1 if n[1] < "1916" else 3, 0, n[1])

    order = sorted((n for n in nodes if not (isinstance(n, int) and n < 7)), key=key)
    pos = {n: i for i, n in enumerate(order)}
    by_file = {r["file"]: r for r in main}
    runs: dict[str, list[dict]] = {}
    for r in main:
        if not solution_only(r):
            runs.setdefault(r["paper"], []).append(r)
    for rs in runs.values():
        rs.sort(key=lambda r: r["date"])

    def successor(s: dict):
        """The puzzle that follows a solution printed on page s: its own, or on a solution-only page the paper's next."""
        if not solution_only(s):
            return node_of(s)
        d0 = dt.date.fromisoformat(s["date"])
        for r in runs.get(s["paper"], []):
            if s["date"] <= r["date"] and (dt.date.fromisoformat(r["date"]) - d0).days <= 14:
                return None if verdict(r["continuity"])[0] == "no" else node_of(r)  # its solution proves a puzzle between
        return None

    edges: dict = {}
    seen: dict = {}
    refuted = {(l["puzzle_page"], l["solution_page"]) for l in li if l["verdict"] in ("no", "unclear")}  # a checked verdict overrides a continuity "yes"

    def add(a, b, ev):
        if a in pos and b in pos and pos[a] < pos[b]:
            edges.setdefault((a, b), []).append(ev)

    for s in main:
        b = successor(s)
        if b is None:
            continue
        word, vs = verdict(s["continuity"])
        if word == "yes":
            d = vs
            if not d:
                earlier = [r for r in runs.get(s["paper"], []) if r["date"] < s["date"]]
                d = earlier[-1]["date"] if earlier else ""
            for a in [r for r in runs.get(s["paper"], []) if r["date"] == d and (r["file"], s["file"]) not in refuted]:
                add(node_of(a), b, f"{s['paper']} {s['date']}: solution checked against its {a['date']} page")
        elif word:
            seen.setdefault(b, []).append((word, s, None))
        if s["solution_of"]:
            a = int(s["solution_of"]) if s["solution_of"].isdigit() else next((node_of(r) for r in main if r["puzzle_key"] == s["solution_of"]), None)
            if a is not None:
                add(a, b, f"{s['paper']} {s['date']}: printed solution identified")
    for l in li:
        a, s = by_file.get(l["puzzle_page"]), by_file.get(l["solution_page"])
        if a is None or s is None:
            continue
        b = node_of(by_file[l["next_page"]]) if l["next_page"] else successor(s)
        if b is None:
            continue
        if l["verdict"] == "yes":
            add(node_of(a), b, f"{s['paper']} {s['date']}: {l['kind']} check against {a['paper']} {a['date']} ({l['checked_by']})")
        elif l["verdict"] == "tentative":
            add(node_of(a), b, f"{TENTATIVE} {l['kind']}, {l['checked_by']}: {l['note']}")
        else:
            seen.setdefault(b, []).append((l["verdict"], s, node_of(a)))
    printed = {int(r["world_no_printed"]) for r in main if r["world_no_printed"]}
    for n in printed:
        if n + 1 in printed:
            edges.setdefault((n, n + 1), []).append("printed numbers")
    return order, nodes, edges, seen


def linked(a, b, edges) -> bool:
    if (a, b) not in edges:
        return False
    if isinstance(a, int) and isinstance(b, int) and b <= LAST_PRINTED:
        return b == a + 1  # a number between them was printed by the World: a puzzle we don't hold
    return True


def date_of(node) -> str:
    return sunday_of(node).isoformat() if isinstance(node, int) else node[1]


def anchor_of(ns: list, nodes: dict) -> str:
    nums = [n for n in ns if isinstance(n, int)]
    if not nums:
        return "floating"
    if any(r["world_no_printed"] for n in nums for r in nodes[n]):
        return "printed grid numbers"
    if nums[0] <= BOX <= nums[-1]:
        return "World Magazine solutions box"
    return "floating (World dates inferred)"


def want(a, b, dead, absent, have) -> tuple:
    """The one page most likely to join a break: (paper, date, why). Past partners first, then the
    Journal's own Sundays in between, searched or not (a text search misses these pages), then the World."""
    n = a + 1 if isinstance(a, int) and isinstance(b, int) and b - a > 1 else b
    if isinstance(n, int):
        for paper, (lo, hi, first, last) in LAGS.items():
            for w in range(lo, hi + 1):
                d = (sunday_of(n) + dt.timedelta(weeks=w)).isoformat()
                if first <= d <= last and (paper, d) not in have and d not in dead.get(paper, ()):
                    return paper, d, f"should print {label(n)}" + (f" with {label(a)}'s solution" if n == b else "")
    d = dt.date.fromisoformat(date_of(a)) + dt.timedelta(weeks=1)
    if isinstance(a, tuple) and a[0] == "minneapolis-journal":
        between = 0
        while d.isoformat() < date_of(b):
            between += 1
            if ("minneapolis-journal", d.isoformat()) not in have and d.isoformat() not in absent.get("minneapolis-journal", ()):
                return "minneapolis-journal", d.isoformat(), f"between {date_of(a)} and {date_of(b)}: browse the whole issue, a text search misses these pages"
            d += dt.timedelta(weeks=1)
        if between:
            return "", "", "another paper's copy: the Journal's issues in between have no puzzle, and no partner is known in 1915"
    if isinstance(n, int) and n <= LAST_PRINTED:
        return "new-york-world", sunday_of(n).isoformat(), f"the World's own page: no partner printed {label(n)}" if n != b else f"the World's own page: the Journal's copy of {label(a)}'s solution is too small to read"
    return "", "", ""


def compute(pr, se, li):
    order, nodes, edges, seen = build(pr, li)
    dead: dict[str, set] = {}
    absent: dict[str, set] = {}
    for s in se:
        if s["result"] in DEAD:
            dead.setdefault(s["paper"], set()).add(s["date"])
        if s["result"] == "not-carried":
            absent.setdefault(s["paper"], set()).add(s["date"])
    have = {(r["paper"], r["date"]) for r in pr}
    chains, breaks, cur = [], [], [order[0]]
    for a, b in zip(order, order[1:]):
        if a != WORLD_END and linked(a, b, edges):
            cur.append(b)
            continue
        chains.append(cur)
        cur = [b]
        about = [(w, s) for w, s, x in seen.get(b, []) if x in (None, a)]  # a checked verdict speaks only for the puzzle it was checked against
        words = [w for w, _ in about]
        pages = lambda word: "; ".join(sorted({f"{s['paper']} {s['date']}" for w, s in about if w == word}))
        if isinstance(a, int) and isinstance(b, int) and b - a > 1:
            reason, detail = "no page held", label(a + 1) + (f" to {label(b - 1)}" if b - a > 2 else "") + " not held"
        elif a == WORLD_END:
            reason, detail = "World dates stop", "the Globe's solutions go on unbroken, but from here its order and dates are not the World's"
        elif "no" in words:
            reason, detail = "contradictory", "solution answers something else: " + pages("no")
        elif "unclear" in words:
            reason, detail = "link unclear", pages("unclear")
        elif "none" in words:
            reason, detail = "no solution printed", pages("none")
        else:
            reason, detail = "not checked", "no page compared yet"
        pw, dw, why = ("", "", "") if a == WORLD_END else want(a, b, dead, absent, have)
        clip = next((r for r in nodes.get(a, []) if r["file"].startswith("clip:") and r["date"] > "1914-03"), None)
        if clip:
            pw, dw, why = clip["paper"], clip["date"], "full page: only a low-resolution clip is held, and it has no clue list"
        breaks.append({"break": f"{label(a)} | {label(b)}", "after": label(a), "before": label(b), "after_date": date_of(a), "before_date": date_of(b),
                       "reason": reason, "detail": detail, "want_paper": pw, "want_date": dw, "want_why": why})
    chains.append(cur)
    rows = []
    for i, ns in enumerate(chains, 1):
        empty = [label(x) for a, b in zip(ns, ns[1:]) if isinstance(a, int) and isinstance(b, int) for x in range(a + 1, b)]
        tent = sum(is_tentative(edges[p]) for p in zip(ns, ns[1:]))
        rows.append({"chain": f"C{i}", "first": label(ns[0]), "last": label(ns[-1]), "first_date": date_of(ns[0]), "last_date": date_of(ns[-1]),
                     "puzzles": str(len(ns)), "verified_links": str(len(ns) - 1 - tent), "tentative_links": str(tent), "standing": "tentative" if tent else "verified", "empty_slots": "; ".join(empty), "anchor": anchor_of(ns, nodes), "_nodes": ns})
    of = {n: c["chain"] for c in rows for n in c["_nodes"]}
    pages_out = []
    for r in sorted(pr, key=lambda r: (r["date"], r["paper"], r["file"])):
        row = {"file": r["file"], "paper": r["paper"], "date": r["date"], "puzzle": "", "chain": "", "why_none": ""}
        if r["paper"] in OTHER_SERIES:
            row["why_none"] = "the Globe's own series, not FUN"
        elif solution_only(r):
            row["why_none"] = "no puzzle on this page"
        else:
            n = node_of(r)
            row["puzzle"], row["chain"] = label(n), of.get(n, "")
            if n not in of:
                row["why_none"] = "before No. 7, where the chains start"
        pages_out.append(row)
    return rows, breaks, pages_out, (order, nodes, edges, seen)


def clue_key(fp: str) -> tuple[str, str]:
    """A first-clue fingerprint as (its square numbers, its words)."""
    s = re.sub(r"\(.*", "", fp.lower())
    s = re.sub(r"horizontal|upper left\w*( section| diagonal)?|outer part|inner part|center figure", "", s)
    m = re.search(r"(\d+)\s*(?:-|to)\s*(\d+)", s)
    return (f"{m.group(1)}-{m.group(2)}" if m else ""), re.sub(r"[^a-z]", "", s)[:20]


def reruns(pr) -> list[dict]:
    """Copies with one first clue over RERUN_WEEKS apart. Candidates only: first clues, not grids, were compared."""
    groups: dict[str, list[dict]] = {}
    for r in pr:
        if r["paper"] not in OTHER_SERIES and r["fingerprint"]:
            k = clue_key(r["fingerprint"])[1]
            if len(k) >= 8:
                groups.setdefault(k, []).append(r)
    rows = []
    for k, rs in groups.items():
        rs.sort(key=lambda r: r["date"])
        first = rs[0]
        for r in rs:
            w = (dt.date.fromisoformat(r["date"]) - dt.date.fromisoformat(first["date"])).days // 7
            la, lb = clue_key(first["fingerprint"])[0], clue_key(r["fingerprint"])[0]
            if w > RERUN_WEEKS and (not la or not lb or la == lb):
                rows.append({"clue_key": k, "first_paper": first["paper"], "first_date": first["date"], "first_shape": first["shape"],
                             "later_paper": r["paper"], "later_date": r["date"], "later_shape": r["shape"], "weeks": str(w)})
    return sorted(rows, key=lambda r: (r["later_date"], r["later_paper"]))


def write(pr, se, li) -> list[dict]:
    rows, breaks, pages, _ = compute(pr, se, li)
    write_tsv(ROOT / "reruns.tsv", RERUN_COLS, reruns(pr))
    write_tsv(ROOT / "chains.tsv", CHAIN_COLS, rows)
    write_tsv(ROOT / "chain_breaks.tsv", BREAK_COLS, breaks)
    write_tsv(ROOT / "chain_pages.tsv", PAGE_COLS, pages)
    return breaks


def main() -> None:
    rows, breaks, _, _ = compute(printings(), searches(), links())
    for c in rows:
        print(c["chain"], c["first"], c["first_date"], "..", c["last"], c["last_date"], f"{c['puzzles']} puzzles,", c["anchor"], ("empty: " + c["empty_slots"]) if c["empty_slots"] else "")
    print(len(breaks), "breaks;", sum(int(c["verified_links"]) for c in rows), "verified links,", sum(int(c["tentative_links"]) for c in rows), "tentative")
    for b in breaks:
        print(" ", b["break"], "|", b["reason"], "|", b["detail"][:110], "|", b["want_paper"], b["want_date"])


if __name__ == "__main__":
    main()
