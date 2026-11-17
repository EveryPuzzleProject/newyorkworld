"""Build the review packets for the hand-read puzzles: one folder per puzzle with its page images,
the xd, the boxes file, the doubts, and index.html that shows each clue's text beside its place
on the scan (hover a clue to light its box; click a box to find its clue). The key's lattice is
drawn with the xd's letters in its squares, to check them against the printed solution.

    python build_packets.py            # every <xdid>.xd that has a <xdid>.boxes.json, into hand-read/packets
    python build_packets.py <out> <rel>  # into <out>, linking the page images at <rel>/<file> (from each
                                         # puzzle's folder) instead of copying them: the scans repo's packets
"""
import html, json, re, shutil
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
PAGES = Path(r"C:/Users/adeja/Projects/newyorkworld-scans/pages")
import sys
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "packets"
LINK = sys.argv[2] if len(sys.argv) > 2 else None  # relative path from a puzzle folder to the page images


def parse_xd(text: str):
    """(metadata, grid rows), from the headed form (worldxd.py)."""
    import worldxd
    z = worldxd.parse(text)
    return z["meta"], z["grid"]


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def cell(g, r, c):
    """Centre of square (r, c), 0-based, by bilinear interpolation of the corners."""
    tl, tr, br, bl = g["corners"]
    u, v = (c + 0.5) / g["cols"], (r + 0.5) / g["rows"]
    top, bot = lerp(tl, tr, u), lerp(bl, br, u)
    return lerp(top, bot, v)


def lattice_svg(g, color):
    tl, tr, br, bl = g["corners"]
    out = []
    for i in range(g["rows"] + 1):
        a, b = lerp(tl, bl, i / g["rows"]), lerp(tr, br, i / g["rows"])
        out.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{color}" stroke-width="1" opacity=".55"/>')
    for j in range(g["cols"] + 1):
        a, b = lerp(tl, tr, j / g["cols"]), lerp(bl, br, j / g["cols"])
        out.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{color}" stroke-width="1" opacity=".55"/>')
    return "".join(out)


def letters_svg(g, grid):
    tl, tr, br, bl = g["corners"]
    h = abs(bl[1] - tl[1]) / g["rows"]
    out = []
    for r, row in enumerate(grid[: g["rows"]]):
        for c, ch in enumerate(row[: g["cols"]]):
            if ch.isalpha():
                x, y = cell(g, r, c)
                out.append(f'<text x="{x + h * .18:.0f}" y="{y - h * .12:.0f}" font-size="{h * .45:.0f}" fill="#e0006a" '
                           f'font-family="Arial" font-weight="bold">{ch}</text>')
    return "".join(out)


def page_view(role, page, z, grid, folder):
    im = Image.open(PAGES / page)
    if LINK:
        name = f"{LINK}/{page}"
    else:
        name = f"{role}.jpg"
        im.convert("RGB").save(folder / name, quality=88)
    w, h = im.size
    svg = []
    for key, color in (("grid", "#00a000"), ("key", "#0070ff")):
        g = z.get(key)
        if g and g.get("page") == role:
            svg.append(lattice_svg(g, color))
            if key == "key":
                svg.append(letters_svg(g, grid))
    for kind in ("clues", "lines"):
        for n, it in enumerate(z.get(kind, [])):
            if it.get("page", "puzzle") == role and it.get("box"):
                x0, y0, x1, y1 = it["box"]
                svg.append(f'<rect id="b-{kind}-{n}" data-row="r-{kind}-{n}" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
                           f'class="box {it.get("how", "")}"/>')
    return (f'<h3>{html.escape(role)}: {html.escape(page)}</h3><div class="pg"><svg viewBox="0 0 {w} {h}" width="{w}">'
            f'<image href="{name}" width="{w}" height="{h}"/>{"".join(svg)}</svg></div>')


def build(xdid: str) -> dict:
    z = json.loads((HERE / f"{xdid}.boxes.json").read_text(encoding="utf-8"))
    xd = (HERE / f"{xdid}.xd").read_text(encoding="utf-8")
    heads, grid = parse_xd(xd)
    folder = OUT / xdid
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(HERE / f"{xdid}.xd", folder)
    shutil.copy(HERE / f"{xdid}.boxes.json", folder)
    dfile = HERE / f"doubts-{xdid}.md"
    doubts = dfile.read_text(encoding="utf-8") if dfile.exists() else ""
    if doubts:
        shutil.copy(dfile, folder)
    views = "".join(page_view(role, page, z, grid, folder) for role, page in z["pages"].items() if page)
    rows = []
    for kind in ("lines", "clues"):
        for n, it in enumerate(z.get(kind, [])):
            label = it.get("pair") or it.get("label", "")
            if it.get("ref"):  # the modern clue number, with the World's pair as printed
                label = f'{it["ref"]} ({it.get("printed") or label})'
            ans = f' <b>~ {html.escape(it["answer"])}</b>' if it.get("answer") else ""
            rows.append(f'<tr id="r-{kind}-{n}" data-box="b-{kind}-{n}" class="{kind}"><td>{html.escape(label)}</td>'
                        f'<td>{html.escape(it.get("text", ""))}{ans}</td><td class="how">{html.escape(it.get("how", ""))}'
                        f'{" (" + ", ".join(it["ocr"]) + ")" if it.get("ocr") else ""}</td></tr>')
    no = z.get("no", "")
    doc = f"""<!doctype html><meta charset=utf-8><title>No. {no} {xdid}</title>
<meta name="color-scheme" content="light"><style>:root{{color-scheme:light}}body{{font:14px Arial;margin:0;display:flex;height:100vh;background:#fff;color:#111}}a{{color:#0645ad}}#l{{width:38%;overflow:auto;padding:8px;border-right:1px solid #ccc}}
#r{{flex:1;overflow:auto;padding:8px}}table{{border-collapse:collapse;width:100%}}td{{padding:2px 4px;border-bottom:1px solid #eee;vertical-align:top}}
tr:hover,tr.on{{background:#ffe9a8}}td.how{{color:#888;font-size:11px}}tr.lines td:first-child{{color:#555;font-style:italic}}
.box{{fill:rgba(255,200,0,.12);stroke:#e08000;stroke-width:2}}.box.eye{{stroke:#c000c0}}.box.on{{fill:rgba(255,80,0,.35);stroke:#f00;stroke-width:4}}
.pg svg{{max-width:100%;height:auto}}pre{{white-space:pre-wrap;background:#f6f6f6;padding:6px;font-size:12px}}</style>
<div id=l><h2>No. {no} &middot; {xdid}</h2><p><a href="{xdid}.xd">{xdid}.xd</a> &middot; <a href="{xdid}.boxes.json">boxes</a>
{f'&middot; <a href="doubts-{xdid}.md">doubts</a>' if doubts else ''} &middot; <a href="../index.html">all puzzles</a></p>
<p>{html.escape(heads.get("Title", ""))} {html.escape(heads.get("Author", ""))}</p>
<p style="font-size:12px;color:#666">Hover a row to light its box on the scan; click a box to find its row. Orange: from an OCR line; purple: placed by eye.
Green lattice: the puzzle grid; blue: the solution, with the xd's letters in pink.</p>
<table>{"".join(rows)}</table><h3>Doubts</h3><pre>{html.escape(doubts) or "none"}</pre><h3>xd</h3><pre>{html.escape(xd)}</pre></div>
<div id=r>{views}</div>
<script>
document.querySelectorAll('tr[data-box]').forEach(tr=>{{const b=document.getElementById(tr.dataset.box);if(!b)return;
tr.onmouseenter=()=>{{b.classList.add('on');b.scrollIntoView({{block:'center',inline:'center'}})}};tr.onmouseleave=()=>b.classList.remove('on')}});
document.querySelectorAll('rect.box').forEach(b=>{{b.style.cursor='pointer';b.onclick=()=>{{const tr=document.getElementById(b.dataset.row);
document.querySelectorAll('tr.on').forEach(x=>x.classList.remove('on'));tr.classList.add('on');tr.scrollIntoView({{block:'center'}})}}}});
</script>"""
    (folder / "index.html").write_text(doc, encoding="utf-8")
    nd = len(re.findall(r"^\s*(?:[-*]|\d+[.)])\s", doubts, re.M))
    eye = sum(1 for it in z.get("clues", []) if it.get("how") == "eye")
    return {"xdid": xdid, "no": no, "clues": len(z.get("clues", [])), "eye": eye, "doubts": nd,
            "size": f'{z.get("grid", {}).get("rows", "?")}x{z.get("grid", {}).get("cols", "?")}', "title": heads.get("Title", "")}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = [build(f.name[:-len(".boxes.json")]) for f in sorted(HERE.glob("nyw*.boxes.json")) if (HERE / f.name.replace(".boxes.json", ".xd")).exists()]
    made.sort(key=lambda m: (int(m["no"]) if str(m["no"]).isdigit() else 99))
    rows = "".join(f'<tr><td>{m["no"]}</td><td><a href="{m["xdid"]}/index.html">{m["xdid"]}</a></td><td>{m["size"]}</td>'
                   f'<td>{m["clues"]}</td><td>{m["eye"]}</td><td>{m["doubts"]}</td><td>{html.escape(m["title"])}</td></tr>' for m in made)
    (OUT / "index.html").write_text(f"""<!doctype html><meta charset=utf-8><title>World FUN Nos. 1-33, read from the scans</title>
<meta name="color-scheme" content="light"><style>body{{font:14px Arial;margin:16px;background:#fff;color:#111}}td,th{{padding:3px 8px;border-bottom:1px solid #ddd;text-align:left}}</style>
<h2>World FUN Nos. 1-33, read by hand from the Milwaukee Sentinel's pages</h2>
<p>Each puzzle's packet ties every clue and line to its box on the scan. Read by Claude, 2026-11-16 (batch nyw-1914-s1).</p>
<table><tr><th>No.</th><th>xdid</th><th>grid</th><th>clues</th><th>boxed by eye</th><th>doubts</th><th>title</th></tr>{rows}</table>""",
                                    encoding="utf-8")
    print(len(made), "packets in", OUT)


if __name__ == "__main__":
    main()
