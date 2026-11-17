"""Draw a puzzle's boxes file onto its page images, to check that every box sits on what it names.

    python draw.py <xdid>                       # hand-read/<xdid>.boxes.json -> overlays/<xdid>-<role>.png
    python draw.py <xdid> --crop puzzle 400 80 1100 980   # one region at full size, -> overlays/<xdid>-crop.png

Each clue's box is the union of the OCR lines it cites ("ocr": ["o101"]) unless it gives its own
("box": [x0, y0, x1, y1]). The grid and key are drawn as lattices from their corners (TL, TR, BR,
BL) and size. Also prints what is missing: clues with no box, a pair whose answer length doesn't
match the grid cells between its end squares can't be checked here (the xd's Numbering does that).
Writes <xdid>.boxes.json back with every clue's "box" filled in from its OCR lines.
"""
import csv, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PAGES = Path(r"C:/Users/adeja/Projects/newyorkworld-scans/pages")
COLORS = [(220, 30, 30), (20, 120, 220), (20, 160, 60), (200, 120, 0), (150, 40, 180)]


def ocr_lines(page: str) -> dict:
    f = HERE / "ocr" / (Path(page).stem + ".tsv")
    if not f.exists():
        return {}
    return {r["id"]: [int(r["x0"]), int(r["y0"]), int(r["x1"]), int(r["y1"])]
            for r in csv.DictReader(open(f, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)}


def union(bs):
    return [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def lattice(d: ImageDraw.ImageDraw, g: dict, color):
    tl, tr, br, bl = g["corners"]
    for i in range(g["rows"] + 1):
        t = i / g["rows"]
        d.line([lerp(tl, bl, t), lerp(tr, br, t)], fill=color, width=1)
    for j in range(g["cols"] + 1):
        t = j / g["cols"]
        d.line([lerp(tl, tr, t), lerp(bl, br, t)], fill=color, width=1)


def fill(z: dict) -> list[str]:
    """Fill each item's box from its OCR ids; return problems."""
    problems, cache = [], {}
    for kind in ("clues", "lines"):
        for it in z.get(kind, []):
            page = z["pages"][it.get("page", "puzzle")]
            lines = cache.setdefault(page, ocr_lines(page))
            ids = it.get("ocr") or []
            bad = [i for i in ids if i not in lines]
            if bad:
                problems.append(f"{kind} {it.get('pair') or it.get('label')}: no OCR line {bad} on {page}")
            if not it.get("box") and ids and not bad:
                it["box"] = union([lines[i] for i in ids])
            if not it.get("box"):
                problems.append(f"{kind} {it.get('pair') or it.get('label')}: no box")
    return problems


def main():
    xdid = sys.argv[1]
    f = HERE / f"{xdid}.boxes.json"
    z = json.loads(f.read_text(encoding="utf-8"))
    problems = fill(z)
    f.write_text(json.dumps(z, indent=1, ensure_ascii=False), encoding="utf-8")
    out = HERE / "overlays"
    out.mkdir(exist_ok=True)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    images = {}
    for role, page in z["pages"].items():
        if page:
            images[role] = Image.open(PAGES / page).convert("RGB")
    draws = {r: ImageDraw.Draw(im) for r, im in images.items()}
    for key, color in (("grid", (0, 170, 0)), ("key", (0, 120, 255))):
        g = z.get(key)
        if g and g.get("page") in draws:
            lattice(draws[g["page"]], g, color)
    for n, it in enumerate(z.get("clues", []) + z.get("lines", [])):
        role = it.get("page", "puzzle")
        if it.get("box") and role in draws:
            c = COLORS[n % len(COLORS)]
            draws[role].rectangle(it["box"], outline=c, width=2)
            draws[role].text((it["box"][0], it["box"][1] - 15), it.get("pair") or it.get("label", ""), fill=c, font=font)
    if "--crop" in sys.argv:
        k = sys.argv.index("--crop")
        role, box = sys.argv[k + 1], [int(v) for v in sys.argv[k + 2:k + 6]]
        images[role].crop(box).save(out / f"{xdid}-crop.png")
        print("wrote", out / f"{xdid}-crop.png")
    else:
        for role, im in images.items():
            im.save(out / f"{xdid}-{role}.png")
            print("wrote", out / f"{xdid}-{role}.png")
    print(f"{len(z.get('clues', []))} clues, {len(z.get('lines', []))} lines; problems: {len(problems)}")
    for p in problems:
        print("  ", p)


if __name__ == "__main__":
    main()
