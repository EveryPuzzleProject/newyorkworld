#!/usr/bin/env python3
"""Import an indexing agent's JSON (one object per page image) into printings.tsv via record.py add.

    python tools/import_index.py index/A.json [--dry]

The JSON fields are those in the indexing brief: file, printed_no, heading_no, heading,
credit, copyright_line, fun_credit, shape, fingerprint, intro, printed_page (or section),
solution (label), solution_no, other_puzzles, confidence, notes. Anything the agent could not
read stays empty and goes into notes, so it shows as a flag rather than a silent blank.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def field(o: dict, *names: str) -> str:
    for n in names:
        v = o.get(n)
        if isinstance(v, dict):
            v = "; ".join(f"{k}: {x}" for k, x in v.items() if x)
        if isinstance(v, list):
            v = "; ".join(str(x) for x in v if x)
        if v not in (None, "", "none", "None", "N/A", "n/a"):
            return str(v).strip()
    return ""


def number(s: str) -> str:
    m = re.search(r"\d+", s or "")
    return m.group(0) if m and s.strip().lower() not in ("none", "unreadable") else ""


def main() -> None:
    dry = "--dry" in sys.argv
    path = Path([a for a in sys.argv[1:] if not a.startswith("--")][0])
    data = json.loads(path.read_text(encoding="utf-8"))
    for o in data:
        f = Path(field(o, "file")).name
        if not f:
            continue
        if "no crossword" in json.dumps(o).lower() and not field(o, "printed_no", "heading"):
            print(f"!! {f}: agent found no crossword; record with `search` by hand")
            continue
        printed = field(o, "printed_no", "world_no_printed", "grid_no")
        printed_n = number(printed)
        notes = []
        if printed and not printed_n:
            notes.append(f"grid number: {printed}")
        conf = field(o, "confidence")
        if conf and not conf.lower().startswith("high"):
            notes.append(f"number read with {conf} confidence")
        for k in ("intro", "other_puzzles", "notes", "masthead", "paper_name", "city"):
            v = field(o, k)
            if v:
                notes.append(f"{k}: {v}")
        sol = field(o, "solution", "solution_label")
        sol_no = number(field(o, "solution_no", "solution_of")) or (number(sol) if re.search(r"No\.?\s*\d+", sol or "") else "")
        pairs = {
            "world_no_printed": printed_n,
            "heading_no": number(field(o, "heading_no")),
            "heading": field(o, "heading"),
            "credit": field(o, "credit"),
            "copyright_line": field(o, "copyright_line", "copyright"),
            "fun_credit": field(o, "fun_credit"),
            "shape": field(o, "shape"),
            "fingerprint": field(o, "fingerprint", "first_clue"),
            "solution_label": sol,
            "solution_of": sol_no,
            "printed_page": field(o, "printed_page", "section/printed_page", "section", "page_header"),
            "notes": "; ".join(notes),
        }
        args = [sys.executable, str(ROOT / "tools" / "record.py"), "add", f] + [f"{k}={v}" for k, v in pairs.items() if v]
        print(f"{f}: No. {printed_n or '-'}  {pairs['heading']!r}  sol {sol_no or '-'}")
        if not dry:
            r = subprocess.run(args, capture_output=True, text=True)
            if r.returncode:
                print(r.stderr or r.stdout)


if __name__ == "__main__":
    main()
