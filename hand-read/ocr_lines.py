"""Dump the pipeline's OCR text boxes for every page of the nyw-s1 run, one TSV per page image:
id, x0, y0, x1, y1 (pixels of the page file in newyorkworld-scans/pages), score, text.
Run from an xword-ocr checkout: uv run python <this> """
import argparse, csv, sys
from pathlib import Path
from xword_ocr import cli, stages, statefile

RUN = Path(r"C:/Users/adeja/Projects/blitz-work/runs/nyw-s1")
OUT = RUN / "hand-read" / "ocr"
a = argparse.Namespace(pubid="nyw", fixes=r"C:/Users/adeja/Projects/newyorkworld/.claude/worktrees/adoring-hermann-906bd6/fixes/fixes.toml",
                       cache=r"C:/Users/adeja/Projects/xword-ocr/.cache/ia", run=None, upgrade=False, fresh=None, records=None)
ctx, fixes = cli._stage_ctx(a, run=stages.MAIN)
rows = list(csv.DictReader(open(RUN / "source" / "pages.tsv", encoding="utf-8"), delimiter="\t"))
leaf = {}
n = 0
for r in rows:
    i = r["issue"]; lf = leaf.get(i, 0); leaf[i] = lf + 1
    rec = ctx.index.get(stages.page_unit(i, lf), "ocr")
    if not rec:
        print("no ocr:", r["file"], file=sys.stderr); continue
    boxes = statefile.decode(ctx.store.get("ocr", rec["output"]))
    name = Path(r["file"]).name
    with open(OUT / (Path(name).stem + ".tsv"), "w", encoding="utf-8", newline="") as f:
        f.write("id\tx0\ty0\tx1\ty1\tscore\ttext\n")
        for k, b in enumerate(sorted(boxes, key=lambda b: (round(b["y0"] / 8), b["x0"]))):
            t = " ".join(str(b["text"]).split())
            f.write(f"o{k}\t{int(b['x0'])}\t{int(b['y0'])}\t{int(b['x1'])}\t{int(b['y1'])}\t{b['score']:.2f}\t{t}\n")
    n += 1
print(n, "pages dumped to", OUT)

# the detector's grids on every page (layout stage): rows, cols, corners TL TR BR BL
import json
leaf = {}
for r in rows:
    i = r["issue"]; lf = leaf.get(i, 0); leaf[i] = lf + 1
    rec = ctx.index.get(stages.page_unit(i, lf), "layout")
    grids = []
    if rec:
        for g in statefile.decode(ctx.store.get("layout", rec["output"])):
            grids.append({"rows": g.rows, "cols": g.cols, "corners": [[int(round(v)) for v in p] for p in g.quad.tolist()]})
    (OUT / (Path(r["file"]).stem + ".grids.json")).write_text(json.dumps(grids), encoding="utf-8")
print("grids written")
