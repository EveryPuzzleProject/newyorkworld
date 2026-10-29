#!/usr/bin/env python3
"""Import a continuity agent's JSON ({file, continuity, evidence, confidence}) into printings.tsv.

    python tools/import_continuity.py index/cont_A_out.json
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def previous_date(file: str) -> str:
    """The previous found page of the same paper, as the record stands now (the page the verdict compares against)."""
    lines = (ROOT / "printings.tsv").read_text(encoding="utf-8").splitlines(); h = lines[0].split("	")
    rows = [dict(zip(h, l.split("	"))) for l in lines[1:]]
    me = next((r for r in rows if r["file"] == file), None)
    if not me:
        return ""
    prev = [r for r in rows if r["paper"] == me["paper"] and r["date"] < me["date"] and not r["file"].startswith("clip:")
            and not r["notes"].lower().startswith(("no new puzzle", "no crossword"))]
    return max(prev, key=lambda r: r["date"])["date"] if prev else ""


for o in json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")):
    v = str(o.get("continuity", "")).strip().lower()
    if v not in ("yes", "no", "none", "unclear"):
        print(f"?? {o.get('file')}: {v!r}"); continue
    ev = str(o.get("evidence", "")).strip(); conf = str(o.get("confidence", "")).strip()
    pd = previous_date(Path(o["file"]).name)
    val = (f"vs {pd} " if pd else "") + v + (f" ({conf})" if conf and conf.lower() != "high" else "") + (f": {ev}" if ev else "")
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "record.py"), "add", Path(o["file"]).name, f"continuity={val}"], capture_output=True, text=True)
    print(("ok " if r.returncode == 0 else "!! ") + o["file"], "" if r.returncode == 0 else r.stderr[-200:])
