#!/usr/bin/env python3
"""Import a continuity agent's JSON ({file, continuity, evidence, confidence}) into printings.tsv.

    python tools/import_continuity.py index/cont_A_out.json
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for o in json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")):
    v = str(o.get("continuity", "")).strip().lower()
    if v not in ("yes", "no", "none", "unclear"):
        print(f"?? {o.get('file')}: {v!r}"); continue
    ev = str(o.get("evidence", "")).strip(); conf = str(o.get("confidence", "")).strip()
    val = v + (f" ({conf})" if conf and conf.lower() != "high" else "") + (f": {ev}" if ev else "")
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "record.py"), "add", Path(o["file"]).name, f"continuity={val}"], capture_output=True, text=True)
    print(("ok " if r.returncode == 0 else "!! ") + o["file"], "" if r.returncode == 0 else r.stderr[-200:])
