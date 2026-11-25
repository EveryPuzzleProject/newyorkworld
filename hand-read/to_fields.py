"""One-off (2026-11-25): move the hand-read World xd files to EPP's four kinds of field (blitz
design/xd-fields.md, agreed by Alex 2026-11-25). The mechanical part:

- `## Printed`: the paper's other words, from the boxes file's printed lines (`label: text`, verbatim);
- `Source:` / `Solution-Source:`: the scan citations, from the boxes file's pages;
- a `^Note:` that only says "misprint: the pair that fits the grid is X" goes, since `^Fits:` says it;
- `Notes:` is replaced by `Description:` from <dir>/<xdid>.txt when that file exists (written per puzzle
  by hand or by an agent: our own description, with the printed text and the provenance taken out).

    python to_fields.py [<descriptions dir>]
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESC = Path(sys.argv[1]) if len(sys.argv) > 1 else None
SKIP = re.compile(r"^(clue |given letters)")
PAGE = re.compile(r"^(.*?)_(\d{4})_(\d\d)_(\d\d)_(\d+)")


def cite(name):
    m = PAGE.match(name or "")
    if not m:
        return name
    paper, y, mo, d, p = m.groups()
    return f"{paper.replace('_', ' ')}, {y}-{mo}-{d}, p. {int(p)}"


def misprint_only(note):
    rest = [p for p in note.split("; ") if not p.startswith("misprint: the pair that fits the grid is ")]
    return "; ".join(rest)


def convert(xdid):
    p = HERE / f"{xdid}.xd"
    z = json.loads((HERE / f"{xdid}.boxes.json").read_text(encoding="utf-8"))
    L = p.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    out, sec = [], None
    fits = {l.split(" ^Fits:")[0] for l in L if " ^Fits: " in l}
    for l in L:
        m = re.match(r"^##\s*(\w+)", l)
        if m:
            sec = m.group(1).lower()
            if sec == "grid":  # ## Printed goes after the metadata
                lines = [f'{it["label"].replace(":", "")}: {" ".join(it["text"].split())}'
                         for it in z.get("lines", []) if it.get("text") and not SKIP.match(it.get("label", ""))]
                if lines:
                    out += ["## Printed", *lines, "", ""]
            out.append(l)
            continue
        if sec == "metadata" and l.startswith("Notes: "):
            d = DESC / f"{xdid}.txt" if DESC else None
            if d and d.exists():
                desc = " ".join(d.read_text(encoding="utf-8").split())
                if desc:
                    out.append(f"Description: {desc}")
            else:
                out.append(l)
            pages = z.get("pages", {})
            if pages.get("puzzle"):
                out.append(f"Source: {cite(pages['puzzle'])}")
            if pages.get("solution"):
                out.append(f"Solution-Source: {cite(pages['solution'])}")
            continue
        m = re.match(r"^(\S+) \^Note: (.*)$", l)
        if sec == "clues" and m and m.group(1) in fits:
            rest = misprint_only(m.group(2))
            if rest:
                out.append(f"{m.group(1)} ^Note: {rest}")
            continue
        out.append(l)
    p.write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    for f in sorted(HERE.glob("nyw*.xd")):
        if f.with_name(f.stem + ".boxes.json").exists():
            convert(f.stem)
            print(f.stem)
