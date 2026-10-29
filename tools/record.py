#!/usr/bin/env python3
"""Keep the record of the New York World's FUN crossword series and its reprints.

Three tables, all tab-separated, all edited only through this tool:

  printings.tsv  one row per crossword printing we have a page for (hand-indexed from the image)
  searches.tsv   one row per paper+Sunday looked for: queued (a batch), found, no-hit,
                 not-carried, missing-from-scans
  status.tsv     one row per World number, 1 to 211, DERIVED from printings.tsv by `rebuild`
                 (only its notes column is kept by hand)

  python tools/record.py new [FOLDER]         page images not yet in printings.tsv (default ../newyorkworld-scans/pages)
  python tools/record.py add FILE key=value…  add or update the printing on FILE (a second puzzle on
                                              the same page: FILE#2; a clipping with no saved page:
                                              clip:<paper>:<date>). Keys: world_no_printed heading_no
                                              heading credit copyright_line fun_credit shape fingerprint
                                              solution_label solution_of (a number or a puzzle_key) url printed_page notes match world_no puzzle_key (copies of one unnumbered puzzle share a key) continuity (the solution on this page answers the previous found page's puzzle: yes / no / none printed / unclear)
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
LAST_NO = 211                   # 1917-12-30
PRINTING_COLS = ["file", "paper", "date", "page", "printed_page", "world_no_printed", "heading_no", "heading",
                 "credit", "copyright_line", "fun_credit", "shape", "fingerprint", "solution_label", "solution_of",
                 "url", "world_no", "puzzle_key", "sunday_inferred", "lag_weeks", "match", "continuity", "flag", "notes"]
SEARCH_COLS = ["paper", "date", "batch", "result", "note"]
STATUS_COLS = ["world_no", "sunday_inferred", "status", "copies", "heading", "credit", "fingerprint",
               "solution_seen", "flag", "notes"]
RESULTS = ["queued", "found", "no-hit", "not-carried", "missing-from-scans"]
FILE_RE = re.compile(r"^(?P<paper>.+?)_(?P<y>\d{4})_(?P<m>\d{2})_(?P<d>\d{2})_(?:Page_)?(?P<page>[A-Za-z]?\d+)(?: \(\d+\))?\.(?:jpe?g|png|pdf)$", re.I)


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
            "page": m.group("page")}


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
    # same World number claimed by printings with different fingerprints
    by_no: dict[str, list[dict]] = {}
    for r in pr:
        if r["world_no"]:
            by_no.setdefault(r["world_no"], []).append(r)
    for n, rs in by_no.items():
        fps = {fp_key(r["fingerprint"]) for r in rs if r["fingerprint"]}
        if len(fps) > 1:
            for r in rs:
                r["flag"] = "; ".join(x for x in (r["flag"], f"No. {n} has copies with different first clues") if x)
    # searches: found when a printing exists
    have = {(r["paper"], r["date"]) for r in pr}
    for s in se:
        if (s["paper"], s["date"]) in have:
            s["result"] = "found"
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
    for g in write_gaps(pr):
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
            word = b["continuity"].split(":")[0].split("(")[0].strip()
            if between:
                kind = {"yes": "skip-confirmed", "no": "missing-puzzle"}.get(word, "unknown")
            elif word == "no":
                kind = "mystery"
            else:
                continue
            rows.append({"paper": paper, "after": a["date"], "before": b["date"], "sundays": " ".join(between), "kind": kind, "evidence": b["continuity"]})
    write_tsv(ROOT / "gaps.tsv", GAP_COLS, sorted(rows, key=lambda r: (r["after"], r["paper"])))
    return rows


def fp_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())[:24]


def sync_pages_tsv(pr: list[dict]) -> None:
    """The scans repo's pages.tsv (xword-ocr folder-source format): one row per image we have."""
    if not SCANS.exists():
        return
    old = {r["file"]: r for r in read_tsv(PAGES_TSV, ["file", "issue", "date", "page", "url", "captured", "note"])}
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
                     "note": o.get("note", "") or (f"printed {r['printed_page']}" if r["printed_page"] else "")})
    write_tsv(PAGES_TSV, ["file", "issue", "date", "page", "url", "captured", "note"], rows)


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
