#!/usr/bin/env python3
"""Keep the record of the New York World's FUN crossword series and its reprints.

Three tables, all tab-separated, all edited only through this tool:

  printings.tsv  one row per crossword printing we have a page for (hand-indexed from the image)
  searches.tsv   one row per paper+Sunday looked for: queued (a batch), found, no-hit,
                 not-carried, missing-from-scans
  links.tsv      one row per checked link: which page's solution answers which page's puzzle
  status.tsv     one row per World number, 1 to 211, DERIVED from printings.tsv by `rebuild`
                 (only its notes column is kept by hand)
  chains.tsv, chain_breaks.tsv, chain_pages.tsv  DERIVED by `rebuild` (tools/chains.py, docs/CHAINS.md)

  python tools/record.py new [FOLDER]         page images not yet in printings.tsv (default ../newyorkworld-scans/pages)
  python tools/record.py add FILE key=value…  add or update the printing on FILE (a second puzzle on
                                              the same page: FILE#2; a clipping with no saved page:
                                              clip:<paper>:<date>). Keys: world_no_printed heading_no
                                              heading credit copyright_line fun_credit shape fingerprint
                                              solution_label solution_of (a number or a puzzle_key) url printed_page notes match world_no puzzle_key (copies of one unnumbered puzzle share a key) continuity (the solution on this page answers the previous found page's puzzle: yes / no / none printed / unclear)
  python tools/record.py link PUZZLE_FILE SOLUTION_FILE kind=grid|label|dated|series verdict=yes|no|unclear|tentative checked_by=… [next_page=FILE] [note=…]
                                              a checked link: the solution on SOLUTION_FILE answers the puzzle on PUZZLE_FILE
                                              (links.tsv; papers may differ; next_page: the puzzle that follows, when it isn't SOLUTION_FILE's own)
  python tools/record.py search PAPER DATE result=no-hit|not-carried|missing-from-scans [note=…]
  python tools/record.py queue [--paper minneapolis-journal] [--n 30] [--from DATE] [DATES…]
  python tools/record.py rebuild              status.tsv, flags, searches 'found', the scans repo's pages.tsv
  python tools/record.py show N|DATE|FILE

The World date of a number is inferred: No. n on 1913-12-21 plus n-1 weeks (see README).
A printing's `world_no` is its printed number when it has one; otherwise it is set by hand
with `match=` saying how (e.g. "fingerprint matches The_Tacoma_Daily_Ledger_1917_03_11_47.jpg").
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCANS = ROOT.parent / "newyorkworld-scans"
PAGES = SCANS / "pages"
PAGES_TSV = SCANS / "pages.tsv"
FIRST = dt.date(1913, 12, 21)   # World No. 1
LAST_NO = 565                   # 1924-10-12 (extended from 211 / 1917-12-30, then 263, 315, 532, 551, as the Globe run goes on)
PRINTING_COLS = ["file", "paper", "date", "page", "printed_page", "world_no_printed", "heading_no", "heading",
                 "credit", "copyright_line", "fun_credit", "shape", "fingerprint", "solution_label", "solution_of",
                 "url", "world_no", "puzzle_key", "sunday_inferred", "lag_weeks", "match", "continuity", "flag", "notes"]
SEARCH_COLS = ["paper", "date", "batch", "result", "note"]
LINK_COLS = ["puzzle_page", "solution_page", "next_page", "kind", "verdict", "checked_by", "note"]
LINK_KINDS = ["grid", "label", "dated", "series"]  # the solution grid compared by eye; a printed "solution of No. n"; a printed date;
# series: no solution, but the puzzles plainly belong together. Always verdict tentative, never counted as verified.
STATUS_COLS = ["world_no", "sunday_inferred", "status", "copies", "heading", "credit", "fingerprint",
               "solution_seen", "flag", "notes"]
RESULTS = ["queued", "found", "no-hit", "not-carried", "missing-from-scans"]
FILE_RE = re.compile(r"^(?P<paper>.+?)_(?P<y>\d{4})_(?P<m>\d{2})_(?P<d>\d{2})_(?:Page_)?(?P<page>[A-Za-z]?\d+)(?P<crop>_fun|_key)?(?: \(\d+\))?\.(?:jpe?g|png|pdf)$", re.I)


def sunday_of(n: int) -> dt.date:
    return FIRST + dt.timedelta(weeks=n - 1)


def number_of(sunday: dt.date) -> int:
    return (sunday - FIRST).days // 7 + 1


def paper_id(token: str) -> str:
    t = token.lower().replace("_", "-")
    return t[4:] if t.startswith("the-") else t


def parse_file(name: str):
    m = FILE_RE.match(name)
    if not m:
        return None
    return {"paper": paper_id(m.group("paper")), "date": dt.date(int(m.group("y")), int(m.group("m")), int(m.group("d"))).isoformat(),
            "page": m.group("page"), "crop": (m.group("crop") or "")[1:]}


def read_tsv(path: Path, cols: list[str]) -> list[dict]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    head = lines[0].split("\t") if lines else cols
    rows = []
    for line in lines[1:]:
        if not line.strip():
            continue
        vals = line.split("\t")
        r = {c: "" for c in cols}
        r.update({h: v for h, v in zip(head, vals)})
        rows.append(r)
    return rows


def write_tsv(path: Path, cols: list[str], rows: list[dict]) -> None:
    lines = ["\t".join(cols)] + ["\t".join((r.get(c) or "").replace("\t", " ").replace("\n", " ") for c in cols) for r in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def printings() -> list[dict]:
    return read_tsv(ROOT / "printings.tsv", PRINTING_COLS)


def searches() -> list[dict]:
    return read_tsv(ROOT / "searches.tsv", SEARCH_COLS)


def status() -> list[dict]:
    return read_tsv(ROOT / "status.tsv", STATUS_COLS)


def links() -> list[dict]:
    return read_tsv(ROOT / "links.tsv", LINK_COLS)


# ---------------------------------------------------------------- new

def new(args) -> None:
    folder = Path(args.folder)
    known = {r["file"].split("#")[0] for r in printings()}
    n = 0
    for p in sorted(folder.iterdir()):
        if p.suffix.lower() not in (".jpg", ".jpeg", ".png", ".pdf"):
            continue
        info = parse_file(p.name)
        if not info:
            print(f"?? {p.name}: name not in paper_yyyy_mm_dd_page form")
            continue
        if p.name in known:
            continue
        if info["crop"] and any(r["paper"] == info["paper"] and r["date"] == info["date"] for r in printings()):
            continue  # a Select-portion crop (_fun puzzle, _key solutions box) of a page already recorded
        n += 1
        d = dt.date.fromisoformat(info["date"])
        exp = f"World No. {number_of(d)} if on the World's date" if d.weekday() == 6 and FIRST <= d <= sunday_of(LAST_NO) else "outside the run"
        print(f"{p.name}\t{info['paper']}\t{info['date']}\tp.{info['page']}\t{exp}")
    if not n:
        print("nothing new")


# ---------------------------------------------------------------- add

def add(args) -> None:
    rows = printings()
    key = args.file
    base = key.split("#")[0]
    if key.startswith("clip:"):  # a printing seen only as a Newspapers.com clipping: clip:<paper>:<date>
        _, paper, date = key.split(":")
        info = {"paper": paper, "date": date, "page": ""}
    else:
        info = parse_file(Path(base).name)
    if not info:
        sys.exit(f"{base}: name not in paper_yyyy_mm_dd_page form (or clip:<paper>:<date>)")
    row = next((r for r in rows if r["file"] == key), None)
    if row is None:
        row = {c: "" for c in PRINTING_COLS}
        row.update(file=key, paper=info["paper"], date=info["date"], page=info["page"])
        rows.append(row)
    settable = {c for c in PRINTING_COLS} - {"file", "date", "page", "sunday_inferred", "lag_weeks", "flag"}  # paper= overrides a misnamed file
    for kv in args.pairs:
        k, _, v = kv.partition("=")
        if k not in settable:
            sys.exit(f"can't set {k}; keys: {' '.join(sorted(settable))}")
        if k in ("world_no_printed", "world_no") and v and not v.isdigit():
            sys.exit(f"{k} is a number (leave empty if none; say so in notes)")
        if k == "notes" and v.startswith("+"):
            v = (row["notes"] + "; " if row["notes"] else "") + v[1:].strip()
        row[k] = v
    if row["world_no_printed"] and not row["world_no"]:
        row["world_no"], row["match"] = row["world_no_printed"], "printed number"
    if not row["url"] and (PAGES / base).exists():
        row["url"] = url_from_zone(PAGES / base)
    rebuild_all(rows, searches(), status())
    show_printing(row)


def url_from_zone(path: Path) -> str:
    """The Newspapers.com page link from the download's Zone.Identifier stream, if present."""
    try:
        import subprocess
        out = subprocess.run(["powershell", "-NoProfile", "-Command", f"Get-Content '{path}' -Stream Zone.Identifier"],
                             capture_output=True, text=True, timeout=20).stdout
        m = re.search(r"[?&]id=(\d+)", out)
        return f"https://www.newspapers.com/image/{m.group(1)}/" if m else ""
    except Exception:
        return ""


# ---------------------------------------------------------------- link

def link(args) -> None:
    pr = {r["file"] for r in printings()}
    for f in (args.puzzle_page, args.solution_page):
        if f not in pr:
            sys.exit(f"{f}: not in printings.tsv")
    kv = dict(p.split("=", 1) for p in args.pairs)
    unknown = set(kv) - {"kind", "verdict", "checked_by", "next_page", "note"}
    if unknown:
        sys.exit(f"can't set {' '.join(sorted(unknown))}")
    if kv.get("kind") not in LINK_KINDS or kv.get("verdict") not in ("yes", "no", "unclear", "tentative") or not kv.get("checked_by"):
        sys.exit(f"kind ({'/'.join(LINK_KINDS)}), verdict (yes/no/unclear/tentative) and checked_by are required")
    if (kv["kind"] == "series") != (kv["verdict"] == "tentative"):
        sys.exit("a series link is tentative, and only a series link is")
    if kv.get("next_page") and kv["next_page"] not in pr:
        sys.exit(f"{kv['next_page']}: not in printings.tsv")
    rows = links()
    row = next((r for r in rows if r["puzzle_page"] == args.puzzle_page and r["solution_page"] == args.solution_page), None)
    if row is None:
        row = {c: "" for c in LINK_COLS}
        row.update(puzzle_page=args.puzzle_page, solution_page=args.solution_page)
        rows.append(row)
    row.update(kv)
    write_tsv(ROOT / "links.tsv", LINK_COLS, sorted(rows, key=lambda r: (r["solution_page"], r["puzzle_page"])))
    rebuild_all(printings(), searches(), status())
    print(f"{args.puzzle_page} <- {args.solution_page}: {row['verdict']} ({row['kind']})")


# ---------------------------------------------------------------- search / queue

def search(args) -> None:
    rows = searches()
    if args.result not in RESULTS or args.result in ("queued", "found"):
        sys.exit("result must be no-hit, not-carried or missing-from-scans (found and queued are set by the tool)")
    row = next((r for r in rows if r["paper"] == args.paper and r["date"] == args.date), None)
    if row is None:
        row = {c: "" for c in SEARCH_COLS}
        row.update(paper=args.paper, date=args.date)
        rows.append(row)
    row["result"] = args.result
    if args.note:
        row["note"] = args.note
    rebuild_all(printings(), rows, status())
    print(f"{args.paper} {args.date}: {args.result}")


def queue(args) -> None:
    rows = searches()
    pr = printings()
    have = {(r["paper"], r["date"]) for r in pr} | {(r["paper"], r["date"]) for r in rows}
    batches = [int(r["batch"]) for r in rows if r["batch"].isdigit()]
    open_rows = [r for r in rows if r["result"] == "queued"]
    if open_rows and not args.force and not args.dates:
        sys.exit(f"batch {open_rows[0]['batch']} still has {len(open_rows)} to do; --force to start another")
    nxt = max(batches, default=0) + 1
    if args.dates:
        dates = args.dates
    else:
        start = dt.date.fromisoformat(args.start)
        d = start + dt.timedelta(days=(6 - start.weekday()) % 7)
        dates = []
        while d <= sunday_of(LAST_NO) and len(dates) < args.n:
            if (args.paper, d.isoformat()) not in have:
                dates.append(d.isoformat())
            d += dt.timedelta(days=7)
    added = 0
    for d in dates:
        if (args.paper, d) in have:
            print(f"skip {args.paper} {d}: already have a printing or a search result")
            continue
        rows.append({"paper": args.paper, "date": d, "batch": str(nxt), "result": "queued", "note": args.note or ""})
        added += 1
    rebuild_all(pr, rows, status())
    print(f"batch {nxt}: {added} {args.paper} Sundays queued")


# ---------------------------------------------------------------- rebuild

def rebuild(args) -> None:
    n = rebuild_all(printings(), searches(), status())
    for r in printings():
        if r["flag"]:
            print(f"{r['file']}\t{r['flag']}")
    for r in status():
        if r["flag"]:
            print(f"No. {r['world_no']}\t{r['flag']}")
    print(f"{n} flags")


def rebuild_all(pr: list[dict], se: list[dict], st: list[dict]) -> int:
    # printings: inferred Sunday, lag, flags
    for r in pr:
        n = r["world_no"]
        if n:
            r["puzzle_key"] = f"no-{n}"
        r["sunday_inferred"] = sunday_of(int(n)).isoformat() if n else ""
        r["lag_weeks"] = str((dt.date.fromisoformat(r["date"]) - sunday_of(int(n))).days // 7) if n else ""
        flags = []
        if r["world_no_printed"] and r["world_no"] and r["world_no_printed"] != r["world_no"]:
            flags.append(f"matched to No. {r['world_no']} but the grid says No. {r['world_no_printed']}")
        if r["heading_no"] and r["world_no_printed"] and r["heading_no"] != r["world_no_printed"]:
            flags.append(f"heading says No. {r['heading_no']}, grid says No. {r['world_no_printed']}")
        if not r["world_no_printed"] and not (r["shape"] and r["fingerprint"]) and not solution_only(r):
            flags.append("no grid number, and no shape or first clue recorded to match it by")
        r["flag"] = "; ".join(flags)
    # per paper: jumps and repeats between consecutive numbered printings
    by_paper: dict[str, list[dict]] = {}
    for r in sorted(pr, key=lambda r: (r["paper"], r["date"], r["file"])):
        if r["world_no_printed"]:
            by_paper.setdefault(r["paper"], []).append(r)
    for paper, rs in by_paper.items():
        for a, b in zip(rs, rs[1:]):
            weeks = (dt.date.fromisoformat(b["date"]) - dt.date.fromisoformat(a["date"])).days // 7
            dn = int(b["world_no_printed"]) - int(a["world_no_printed"])
            if dn == 0:
                b["flag"] = "; ".join(x for x in (b["flag"], f"repeats No. {a['world_no_printed']} of {a['date']}") if x)
            elif dn != weeks:
                b["flag"] = "; ".join(x for x in (b["flag"], f"No. {a['world_no_printed']} on {a['date']} to No. {b['world_no_printed']} in {weeks} weeks: {dn - weeks:+d}") if x)
    # copies with the same first clue and no key yet: group them automatically
    by_fp: dict[str, list[dict]] = {}
    for r in pr:
        if r["fingerprint"] and not r["world_no"]:
            k = fp_key(r["fingerprint"])
            if len(k) >= 8:
                by_fp.setdefault(k, []).append(r)
    for k, rs in by_fp.items():
        if len(rs) < 2:
            continue
        shapes = {(r["shape"].split()[0].lower() if r["shape"] else "") for r in rs}
        if len(k) < 14 and len(shapes) > 1:
            continue  # a short common clue ("A vegetable") on different grid shapes is no match
        keys = {r["puzzle_key"] for r in rs if r["puzzle_key"]}
        key = sorted(keys)[0] if keys else "fp-" + k[:16]
        for r in rs:
            if not r["puzzle_key"]:
                r["puzzle_key"] = key
                r["match"] = r["match"] or f"same first clue as {', '.join(x['paper'] + ' ' + x['date'] for x in rs if x is not r)} (automatic)"
    # same World number claimed by printings with different fingerprints
    by_no: dict[str, list[dict]] = {}
    for r in pr:
        if r["world_no"]:
            by_no.setdefault(r["world_no"], []).append(r)
    for n, rs in by_no.items():
        if len({r["puzzle_key"] for r in rs}) == 1 and rs[0]["puzzle_key"]:
            continue  # the copies were keyed as one puzzle (spelling variants of a clue are fine)
        fps = {fp_key(r["fingerprint"]) for r in rs if r["fingerprint"]}
        if len(fps) > 1:
            for r in rs:
                r["flag"] = "; ".join(x for x in (r["flag"], f"No. {n} has copies with different first clues") if x)
    # searches: found when a printing exists for that paper and date; a QUEUED row is also
    # satisfied by any paper's copy of that Sunday (one good copy per Sunday is the aim)
    have = {(r["paper"], r["date"]) for r in pr}
    by_date: dict[str, list[str]] = {}
    for r in pr:
        by_date.setdefault(r["date"], []).append(r["paper"])
    for s in se:
        if (s["paper"], s["date"]) in have:
            s["result"] = "found"
        elif s["result"] == "queued" and s["date"] in by_date:
            s["result"] = "found"
            s["note"] = "copy taken from " + ", ".join(sorted(set(by_date[s["date"]]))) + (f"; {s['note']}" if s["note"] else "")
    # status: one row per number
    notes = {r["world_no"]: r["notes"] for r in st}
    new_st = []
    nflags = sum(bool(r["flag"]) for r in pr)
    for n in range(1, LAST_NO + 1):
        rs = sorted(by_no.get(str(n), []), key=lambda r: r["date"])
        sols = [r for r in pr if r["solution_of"] in (str(n), f"no-{n}")]
        row = {c: "" for c in STATUS_COLS}
        row["world_no"], row["sunday_inferred"], row["notes"] = str(n), sunday_of(n).isoformat(), notes.get(str(n), "")
        row["status"] = "have" if rs else "wanted"
        row["copies"] = "; ".join(f"{r['paper']} {r['date']}" + (f" (lag {r['lag_weeks']}w)" if r["lag_weeks"] not in ("", "0") else "") for r in rs)
        if rs:
            row["heading"] = rs[0]["heading"]
            row["credit"] = next((r["credit"] for r in rs if r["credit"]), "")
            row["fingerprint"] = next((r["fingerprint"] for r in rs if r["fingerprint"]), "")
        row["solution_seen"] = "; ".join(f"{r['paper']} {r['date']}" for r in sols)
        fl = [r["flag"] for r in rs if r["flag"]]
        row["flag"] = " | ".join(dict.fromkeys(fl))
        new_st.append(row)
    gaps_rows = write_gaps(pr)
    for g in gaps_rows:
        if g["kind"] == "skip-confirmed":
            for d in g["sundays"].split():
                row = next((x for x in se if x["paper"] == g["paper"] and x["date"] == d), None)
                if row is None:
                    row = {"paper": g["paper"], "date": d, "batch": "", "result": "", "note": ""}
                    se.append(row)
                if row["result"] in ("", "queued", "no-hit"):
                    row["result"], row["note"] = "not-carried", f"nothing ran in between: the {g['before']} page's solution answers the {g['after']} puzzle"
    write_tsv(ROOT / "printings.tsv", PRINTING_COLS, sorted(pr, key=lambda r: (r["date"], r["paper"], r["file"])))
    write_tsv(ROOT / "searches.tsv", SEARCH_COLS, sorted(se, key=lambda r: (r["date"], r["paper"])))
    write_tsv(ROOT / "status.tsv", STATUS_COLS, new_st)
    import chains  # imports this module; here so that `rebuild` writes the chains too
    breaks = chains.write(pr, se, links())
    write_wanted(pr, se, new_st, gaps_rows, breaks)
    sync_pages_tsv(pr)
    return nflags


GAP_COLS = ["paper", "after", "before", "sundays", "kind", "evidence"]


def solution_only(r: dict) -> bool:
    """A page we hold that carries no puzzle (only a solution, or another feature): its notes say so."""
    n = r["notes"].lower()
    return n.startswith("no new puzzle") or n.startswith("no crossword")


def write_gaps(pr: list[dict]) -> None:
    """gaps.tsv: what the continuity column says about the Sundays between consecutive found
    pages of one paper. kind: missing-puzzle (the later page's solution is not the earlier page's
    puzzle, so a puzzle ran in between: find it), skip-confirmed (its solution IS the earlier
    puzzle, so nothing ran in between), mystery (no Sunday in between, yet the solution is not
    the earlier puzzle), unknown (no solution printed, or unclear, or not yet checked)."""
    rows = []
    by_paper: dict[str, list[dict]] = {}
    for r in pr:
        if not r["file"].startswith("clip:") and not solution_only(r):
            by_paper.setdefault(r["paper"], []).append(r)
    for paper, rs in by_paper.items():
        rs.sort(key=lambda r: r["date"])
        for a, b in zip(rs, rs[1:]):
            d0, d1 = dt.date.fromisoformat(a["date"]), dt.date.fromisoformat(b["date"])
            between = []
            d = d0 + dt.timedelta(days=7)
            while d < d1:
                between.append(d.isoformat()); d += dt.timedelta(days=7)
            c = b["continuity"]
            vs = ""
            if c.startswith("vs "):
                vs, c = c[3:13], c[14:]
            word = c.split(":")[0].split("(")[0].strip()
            if vs and vs != a["date"]:
                word = "recheck"  # compared against an earlier page; a page has been found in between since
            if between:
                kind = {"yes": "skip-confirmed", "no": "missing-puzzle", "recheck": "recheck"}.get(word, "unknown")
            elif word in ("no", "recheck"):
                kind = "mystery" if word == "no" else "recheck"
            else:
                continue
            rows.append({"paper": paper, "after": a["date"], "before": b["date"], "sundays": " ".join(between), "kind": kind, "evidence": b["continuity"]})
    write_tsv(ROOT / "gaps.tsv", GAP_COLS, sorted(rows, key=lambda r: (r["after"], r["paper"])))
    return rows


# Each partner's delay behind the reference paper (the Journal in 1914-16, the Globe from 1917,
# both on the World's own date in 1917), in weeks, as measured from matched copies; and the span
# in which that paper is known to have carried FUN. Candidates outside the span aren't offered.
LAGS = {
    "pittsburgh-press": (1, 2, "1916-06-11", "1919-12-28"),
    "tacoma-daily-ledger": (1, 2, "1916-08-27", "1919-12-28"),
    "shreveport-times": (2, 2, "1916-08-06", "1919-12-28"),
    "new-orleans-states": (2, 3, "1917-02-11", "1919-12-28"),
    "salt-lake-telegram": (3, 3, "1917-09-02", "1919-12-28"),
    "fort-wayne-journal-gazette": (1, 1, "1916-11-19", "1919-12-28"),
    "seattle-post-intelligencer": (1, 2, "1916-10-08", "1917-12-30"),
    "los-angeles-tribune": (3, 8, "1916-08-06", "1919-12-28"),
    "boston-globe": (0, 0, "1917-02-25", "1917-12-30"),  # on the World's date in 1917 only (docs/CAMPBELL-CROSSCHECK.md)
    "minneapolis-journal": (0, 0, "1914-02-01", "1917-01-28"),
}
WANTED_COLS = ["puzzle", "reference_date", "why", "paper", "date", "status"]


def write_wanted(pr: list[dict], se: list[dict], st: list[dict], gaps: list[dict], breaks: list[dict]) -> None:
    """wanted.tsv: one row per (missing puzzle, candidate paper, date). A missing puzzle is a World
    number with no copy in the anchored years (1917 on, within the Globe's run), or a Journal week
    in 1915-16 whose puzzle the next page's solution proves existed. Candidate dates come from LAGS;
    a candidate already searched keeps its result as status, a copy already held isn't offered."""
    have = {(r["paper"], r["date"]) for r in pr}
    searched = {(x["paper"], x["date"]): x["result"] for x in se}
    rows = []
    def offer(puzzle, ref, why):
        d0 = dt.date.fromisoformat(ref)
        for paper, (lo, hi, first, last) in LAGS.items():
            for w in range(lo, hi + 1):
                d = (d0 + dt.timedelta(weeks=w)).isoformat()
                if not (first <= d <= last) or (paper, d) in have:
                    continue
                rows.append({"puzzle": puzzle, "reference_date": ref, "why": why, "paper": paper, "date": d,
                             "status": searched.get((paper, d), "")})
    # anchored years: World numbers without a copy, from the Globe's first copy on
    globe_dates = sorted(r["date"] for r in pr if r["paper"] == "boston-globe" and r["date"] <= "1917-12-30")
    if globe_dates:
        for r in st:
            if r["status"] == "wanted" and globe_dates[0] <= r["sunday_inferred"] <= globe_dates[-1]:
                offer(f"No. {r['world_no']}", r["sunday_inferred"], "World number with no copy (the Globe ran on the World's date)")
    # unanchored years: Journal weeks proven by a later solution
    for g in gaps:
        if g["paper"] == "minneapolis-journal" and g["kind"] == "missing-puzzle":
            for d in g["sundays"].split():
                offer(f"Journal week {d}", d, f"the Journal's {g['before']} page answers a puzzle it printed between {g['after']} and {g['before']}")
    # chain breaks: the page that would join the two chains either side
    for b in breaks:
        if b["want_paper"] and ((b["want_paper"], b["want_date"]) not in have or b["want_why"].startswith("full page")):
            rows.append({"puzzle": f"chain break {b['break']}", "reference_date": b["want_date"], "why": b["want_why"], "paper": b["want_paper"],
                         "date": b["want_date"], "status": searched.get((b["want_paper"], b["want_date"]), "")})
    # pages held only as a clip, whose full page is still to come
    for r in pr:
        if r["file"].startswith("clip:") and "full page still to download" in r["notes"] and not any(w["paper"] == r["paper"] and w["date"] == r["date"] for w in rows):
            rows.append({"puzzle": f"full page of {r['paper']} {r['date']}", "reference_date": r["date"], "why": "full page: only a clip is held", "paper": r["paper"],
                         "date": r["date"], "status": ""})
    write_tsv(ROOT / "wanted.tsv", WANTED_COLS, sorted(rows, key=lambda r: (r["paper"], r["date"], r["puzzle"])))


def fp_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())[:24]


def sync_pages_tsv(pr: list[dict]) -> None:
    """The scans repo's pages.tsv (xword-ocr folder-source format): one row per image we have. Select-portion
    crops (<page>_fun.jpg the puzzle, <page>_key.jpg the solutions box) get a row of their own with crop_of."""
    if not SCANS.exists():
        return
    cols = ["file", "issue", "date", "page", "url", "captured", "note", "crop_of"]
    old = {r["file"]: r for r in read_tsv(PAGES_TSV, cols)}
    rows = []
    seen = set()
    for r in pr:
        base = r["file"].split("#")[0]
        if base in seen or not (PAGES / base).exists():
            continue
        seen.add(base)
        o = old.get(f"pages/{base}", {})
        rows.append({"file": f"pages/{base}", "issue": f"{r['paper']}-{r['date']}", "date": r["date"], "page": r["page"],
                     "url": r["url"] or o.get("url", ""), "captured": o.get("captured") or dt.date.today().isoformat(),
                     "note": o.get("note", "") or (f"printed {r['printed_page']}" if r["printed_page"] else ""), "crop_of": o.get("crop_of", "")})
    crops = []
    by_day = {}
    for r in pr:
        if not r["file"].startswith("clip:"):
            by_day.setdefault((r["paper"], r["date"]), []).append(r["file"].split("#")[0])
    for p in sorted(PAGES.iterdir()):
        info = parse_file(p.name)
        if not info or not info["crop"] or p.name in seen:
            continue
        held = by_day.get((info["paper"], info["date"]))
        if not held:
            continue
        whole = p.name.replace("_" + info["crop"], "")
        parent = whole if (PAGES / whole).exists() else next((h for h in held if h != p.name), "")
        o = old.get(f"pages/{p.name}", {})
        crops.append({"file": f"pages/{p.name}", "issue": f"{info['paper']}-{info['date']}", "date": info["date"], "page": "", "url": "",
                     "captured": o.get("captured") or dt.date.today().isoformat(),
                     "note": o.get("note") or ("puzzle: heading, intro, grid and clues (Newspapers.com Select portion)" if info["crop"] == "fun"
                                               else "solutions box (Newspapers.com Select portion)"),
                     "crop_of": o.get("crop_of") or (f"pages/{parent}" if parent else "")})
    for c in crops:  # each crop follows the last row of its day
        at = max((i for i, r in enumerate(rows) if r["issue"] == c["issue"]), default=len(rows) - 1)
        rows.insert(at + 1, c)
    write_tsv(PAGES_TSV, cols, rows)


# ---------------------------------------------------------------- show

def show_printing(r: dict) -> None:
    for c in PRINTING_COLS:
        if r[c]:
            print(f"{c:18} {r[c]}")


def show(args) -> None:
    k = args.key
    if k.isdigit():
        for r in status():
            if r["world_no"] == k:
                for c in STATUS_COLS:
                    if r[c]:
                        print(f"{c:18} {r[c]}")
        for r in printings():
            if r["world_no"] == k:
                print("--"); show_printing(r)
    else:
        for r in printings():
            if r["file"].startswith(k) or r["date"] == k:
                show_printing(r); print("--")
        for s in searches():
            if s["date"] == k:
                print(f"search {s['paper']} {s['date']}: {s['result']} {s['note']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new"); p.add_argument("folder", nargs="?", default=str(PAGES)); p.set_defaults(fn=new)
    p = sub.add_parser("add"); p.add_argument("file"); p.add_argument("pairs", nargs="*"); p.set_defaults(fn=add)
    p = sub.add_parser("link"); p.add_argument("puzzle_page"); p.add_argument("solution_page"); p.add_argument("pairs", nargs="*"); p.set_defaults(fn=link)
    p = sub.add_parser("search"); p.add_argument("paper"); p.add_argument("date"); p.add_argument("result"); p.add_argument("note", nargs="?", default="")
    p.set_defaults(fn=search)
    p = sub.add_parser("queue"); p.add_argument("--paper", default="minneapolis-journal"); p.add_argument("--n", type=int, default=30)
    p.add_argument("--from", dest="start", default="1914-02-15"); p.add_argument("--note", default="")
    p.add_argument("--force", action="store_true"); p.add_argument("dates", nargs="*"); p.set_defaults(fn=queue)
    sub.add_parser("rebuild").set_defaults(fn=rebuild)
    p = sub.add_parser("show"); p.add_argument("key"); p.set_defaults(fn=show)
    args = ap.parse_args()
    if args.cmd == "search":
        args.result = args.result.split("=")[-1]
        args.note = args.note.split("=", 1)[-1] if args.note else ""
    args.fn(args)


if __name__ == "__main__":
    main()
