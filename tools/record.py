#!/usr/bin/env python3
"""Keep status.tsv: one row per Sunday of the New York World's FUN crossword series.

    python tools/record.py init                      # create status.tsv (211 Sundays); refuses if it exists
    python tools/record.py new [FOLDER]              # page images in FOLDER not yet recorded (default ../newyorkworld-scans/pages)
    python tools/record.py set SUNDAY key=value ...  # update one row, e.g.
        python tools/record.py set 1914-02-15 status=clipped world_no_printed=9 heading="Can You Solve Them?" \
            copy_page=45 file=The_Minneapolis_Journal_1914_02_15_45.jpg
    python tools/record.py queue [--n 30] [--priority FROM TO]   # assign the next batch of Sundays to clip
    python tools/record.py check                     # recompute flags (number mismatches, repeats, jumps)
    python tools/record.py show SUNDAY               # print one row

Every write re-runs `check`, so the flag column is always current. The World date
of a row is the Sunday itself: World No. n is expected on 1913-12-21 plus n-1 weeks.
That is an inference (see README), which is why the column is world_no_expected.
"""
import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS = ROOT / "status.tsv"
SCANS = ROOT.parent / "newyorkworld-scans"          # the private twin: pages/ and pages.tsv (xword-ocr folder-source format)
PAGES_TSV = SCANS / "pages.tsv"
FIRST = dt.date(1913, 12, 21)          # World No. 1
LAST = dt.date(1917, 12, 30)           # end of the run tracked here
JOURNAL_FIRST = dt.date(1914, 2, 1)    # the Minneapolis Journal's first FUN puzzle (checked: none earlier)
COLUMNS = [
    "sunday", "world_no_expected", "world_no_printed",
    "source", "copy_date", "copy_page", "heading", "credit", "clipping_url", "file",
    "solution_date", "solution_page", "solution_clipping_url", "solution_file",
    "status", "batch", "flag", "notes",
]
STATUSES = ["to-clip", "clipped", "missing-from-scans", "not-carried", "before-the-journal"]
SOURCES = {"minneapolis-journal": "The_Minneapolis_Journal", "pittsburgh-press": "The_Pittsburgh_Press",
           "tacoma-daily-ledger": "Tacoma_Daily_Ledger", "boston-globe": "The_Boston_Globe"}
FILE_RE = re.compile(r"^(?P<paper>.+?)_(?P<y>\d{4})_(?P<m>\d{2})_(?P<d>\d{2})_(?P<page>[A-Za-z]?\d+)(?: \(\d+\))?\.(?:jpe?g|png|pdf)$", re.I)


def expected_no(sunday: dt.date) -> int:
    return (sunday - FIRST).days // 7 + 1


def read() -> list[dict]:
    with open(STATUS, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
    for r in rows:
        for c in COLUMNS:
            r.setdefault(c, "")
    return rows


def write(rows: list[dict]) -> None:
    rows.sort(key=lambda r: r["sunday"])
    # Plain tab-separated text, written whole: quotes in notes are literal (no csv quoting),
    # and a failure can't leave a half-written file.
    lines = ["\t".join(COLUMNS)]
    for r in rows:
        lines.append("\t".join((r.get(c) or "").replace("\t", " ").replace("\n", " ") for c in COLUMNS))
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def init(args) -> None:
    if STATUS.exists():
        sys.exit("status.tsv exists; edit it with `set`, don't re-init")
    rows = []
    d = FIRST
    while d <= LAST:
        r = {c: "" for c in COLUMNS}
        r["sunday"] = d.isoformat()
        r["world_no_expected"] = str(expected_no(d))
        if d < JOURNAL_FIRST:
            r["status"] = "before-the-journal"
            r["notes"] = "before the Minneapolis Journal's first FUN puzzle (1914-02-01); needs another source"
        else:
            r["status"] = "to-clip"
            r["source"] = "minneapolis-journal"
        rows.append(r)
        d += dt.timedelta(days=7)
    write(rows)
    print(f"status.tsv: {len(rows)} Sundays, {FIRST} to {LAST}")


def parse_file(name: str):
    m = FILE_RE.match(name)
    if not m:
        return None
    paper = m.group("paper")
    source = next((k for k, v in SOURCES.items() if v.lower() == paper.lower()), paper)
    return {"source": source, "date": dt.date(int(m.group("y")), int(m.group("m")), int(m.group("d"))), "page": m.group("page")}


def new(args) -> None:
    folder = Path(args.folder)
    rows = read()
    known = {r["file"] for r in rows} | {r["solution_file"] for r in rows}
    found = 0
    for p in sorted(folder.iterdir()):
        info = parse_file(p.name)
        if not info:
            if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".pdf"):
                print(f"?? {p.name}: name not in paper_yyyy_mm_dd_page form")
            continue
        if p.name in known:
            continue
        found += 1
        d = info["date"]
        sunday = d if d.weekday() == 6 else None
        row = next((r for r in rows if r["sunday"] == d.isoformat()), None)
        where = (f"row {row['sunday']} (expected No. {row['world_no_expected']}, {row['status']})" if row
                 else f"not a Sunday in the run" if sunday is None else "outside 1913-12-21..1917-12-30")
        print(f"{p.name}\t{info['source']}\t{d}\tp.{info['page']}\t{where}")
    if not found:
        print("nothing new")


def set_row(args) -> None:
    rows = read()
    row = next((r for r in rows if r["sunday"] == args.sunday), None)
    if row is None:
        sys.exit(f"no row for {args.sunday}: not a Sunday in 1913-12-21..1917-12-30?")
    for kv in args.pairs:
        k, _, v = kv.partition("=")
        if k not in COLUMNS or k in ("sunday", "world_no_expected", "flag"):
            sys.exit(f"can't set {k}; columns: {', '.join(c for c in COLUMNS if c not in ('sunday', 'world_no_expected', 'flag'))}")
        if k == "status" and v not in STATUSES:
            sys.exit(f"status must be one of {STATUSES}")
        if k == "world_no_printed" and v and not v.isdigit():
            sys.exit("world_no_printed is a number (leave empty if the grid has none; say so in notes)")
        if k == "notes" and v.startswith("+"):
            v = (row["notes"] + "; " if row["notes"] else "") + v[1:].strip()
        if k == "file" and v and not row["copy_date"]:
            info = parse_file(Path(v).name)
            if info:
                row["copy_date"], row["copy_page"], row["source"] = info["date"].isoformat(), info["page"], info["source"]
        if k == "solution_file" and v and not row["solution_date"]:
            info = parse_file(Path(v).name)
            if info:
                row["solution_date"], row["solution_page"] = info["date"].isoformat(), info["page"]
        row[k] = v
    if row["status"] == "clipped" and row["batch"]:
        pass  # keep the batch number: it says which day's batch found it
    check_rows(rows)
    write(rows)
    for f, url, d, pg in ((row["file"], row["clipping_url"], row["copy_date"], row["copy_page"]),
                          (row["solution_file"], row["solution_clipping_url"], row["solution_date"], row["solution_page"])):
        if f:
            scans_row(f, row["source"], d, pg, url)
    show_row(row)


def scans_row(file: str, source: str, date: str, page: str, url: str) -> None:
    """Add or update this image's row in the scans repo's pages.tsv, so xword-ocr can harvest the folder."""
    if not PAGES_TSV.exists():
        return
    lines = PAGES_TSV.read_text(encoding="utf-8").splitlines()
    rel = f"pages/{Path(file).name}"
    new = "	".join([rel, f"{source}-{date}", date, page, url, dt.date.today().isoformat(), ""])
    for i, line in enumerate(lines[1:], 1):
        if line.split("	")[0] == rel:
            old = line.split("	")
            new = "	".join([rel, f"{source}-{date}", date, page, url or old[4], old[5] or dt.date.today().isoformat(), old[6] if len(old) > 6 else ""])
            lines[i] = new
            break
    else:
        lines.append(new)
    PAGES_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")


def check_rows(rows: list[dict]) -> int:
    """Recompute the flag column. Returns the number of flagged rows."""
    prev = None  # last clipped row with a printed number
    n = 0
    for r in rows:
        flags = []
        printed = r["world_no_printed"]
        if r["status"] == "clipped" and printed:
            p, e = int(printed), int(r["world_no_expected"])
            if p != e:
                flags.append(f"printed No. {p}, expected No. {e} ({p - e:+d})")
            if prev is not None:
                pp = int(prev["world_no_printed"])
                weeks = (dt.date.fromisoformat(r["sunday"]) - dt.date.fromisoformat(prev["sunday"])).days // 7
                if p == pp:
                    flags.append(f"repeats No. {pp} of {prev['sunday']}")
                elif p - pp != weeks:
                    flags.append(f"No. {pp} on {prev['sunday']} to No. {p} in {weeks} week{'s' * (weeks != 1)}: {p - pp - weeks:+d}")
            prev = r
        if r["status"] == "clipped" and not printed and not r["notes"]:
            flags.append("clipped, no number recorded: say in notes whether the grid has one")
        if r["status"] == "clipped" and not r["file"] and not r["clipping_url"]:
            flags.append("clipped, but no file or clipping URL")
        r["flag"] = "; ".join(flags)
        n += bool(flags)
    return n


def check(args) -> None:
    rows = read()
    n = check_rows(rows)
    write(rows)
    for r in rows:
        if r["flag"]:
            print(f"{r['sunday']}\t{r['flag']}")
    print(f"{n} flagged")


def queue(args) -> None:
    rows = read()
    batches = [int(r["batch"]) for r in rows if r["batch"].isdigit()]
    open_batch = [r for r in rows if r["status"] == "to-clip" and r["batch"]]
    if open_batch and not args.force:
        sys.exit(f"batch {open_batch[0]['batch']} still has {len(open_batch)} Sundays to clip; finish or --force")
    nxt = max(batches, default=0) + 1
    todo = [r for r in rows if r["status"] == "to-clip" and not r["batch"]]
    if args.sundays:
        pick = [r for r in todo if r["sunday"] in args.sundays]
        missing = set(args.sundays) - {r["sunday"] for r in pick}
        if missing:
            sys.exit(f"not to-clip or already queued: {sorted(missing)}")
    else:
        pri = []
        if args.priority:
            lo, hi = args.priority
            pri = [r for r in todo if lo <= r["sunday"] <= hi]
        rest = [r for r in todo if r not in pri]
        pick = (pri + rest)[: args.n]
    for r in pick:
        r["batch"] = str(nxt)
    write(rows)
    print(f"batch {nxt}: {len(pick)} Sundays")
    for r in pick:
        print(f"  {r['sunday']}\tNo. {r['world_no_expected']}\t{r['source']}")


def show_row(r: dict) -> None:
    for c in COLUMNS:
        if r[c]:
            print(f"{c:22} {r[c]}")


def show(args) -> None:
    r = next((r for r in read() if r["sunday"] == args.sunday), None)
    if r is None:
        sys.exit(f"no row for {args.sunday}")
    show_row(r)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=init)
    p = sub.add_parser("new"); p.add_argument("folder", nargs="?", default=str(SCANS / "pages")); p.set_defaults(fn=new)
    p = sub.add_parser("set"); p.add_argument("sunday"); p.add_argument("pairs", nargs="+"); p.set_defaults(fn=set_row)
    p = sub.add_parser("queue"); p.add_argument("--n", type=int, default=30); p.add_argument("--priority", nargs=2, metavar=("FROM", "TO"))
    p.add_argument("--force", action="store_true", help="start a new batch although the open one isn't finished")
    p.add_argument("sundays", nargs="*", help="exact Sundays for this batch (else the next --n to-clip rows)"); p.set_defaults(fn=queue)
    sub.add_parser("check").set_defaults(fn=check)
    p = sub.add_parser("show"); p.add_argument("sunday"); p.set_defaults(fn=show)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
