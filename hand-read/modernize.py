"""One-off (2026-11-17): renumber the hand-read World xd files the modern way, keeping the World's
own end-square pair on each clue as `^Printed:` (Alex's scheme, docs/NUMBERING-GIVENS.md).

    python modernize.py            # every hand-read/nyw*.xd except the three kept in the World's form

Each clue `a-b.` becomes `A<n>.` or `D<n>.` for the across or down run it fills, numbered as any
crossword is (a square that starts an across or down run of two or more takes the next number, in
reading order; a given square is numbered like any other). The World's pair goes to `^Printed:`;
where the pair was misprinted, `^Printed:` holds the print and a `^Note:` names the pair that fits.
The `Numbering:` header and the `## Labels` section go. The boxes file's clues gain the new `ref`.

Nos. 13 (nyw1914-03-15), 18 (nyw1914-04-19) and 27 (nyw1914-07-12) stay in the World's form: their
words are not all whole across/down runs (an inner star, diagonals, and a word that would need a
bar), so they keep `Numbering:` and get a note in their Notes.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import worldxd as W  # noqa: E402

KEEP = {
    "nyw1914-03-15": "Kept in the World's own numbering (clues named by their printed end-square pair, with a Labels section): the inner star's words lie inside longer runs and three meet at the shared centre E, so modern across/down numbering can't name them. A puzzle to treat as a meta (Alex, 2026-11-17).",
    "nyw1914-04-19": "Kept in the World's own numbering (clues named by their printed end-square pair, with a Labels section): four words run diagonally (GAMMA, SNARE, FRETS, SITES), which across/down numbering can't name. A puzzle to treat as a meta (Alex, 2026-11-17).",
    "nyw1914-07-12": "Kept in the World's own numbering (clues named by their printed end-square pair, with a Labels section): the given FUN, across and down, runs on into other words (the down FUN continues as FUND), so some clued words are shorter than their runs. In effect there is a bar between 1 Down and 10 Down, and xd has no bars yet (Alex, 2026-11-17).",
}


def modern_numbers(grid):
    sq = lambda r, c: 0 <= r < len(grid) and 0 <= c < len(grid[0]) and W.is_square(grid[r][c])
    num, n = {}, 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if sq(r, c) and ((not sq(r, c - 1) and sq(r, c + 1)) or (not sq(r - 1, c) and sq(r + 1, c))):
                n += 1
                num[(r, c)] = n
    return num


def label_squares(z):
    rule = z["meta"].get("Numbering", "")
    if rule in W.RULES:
        where = {}
        for s, lab in W.number(z["grid"], rule, z["given"]).items():
            where.setdefault(lab, []).append(s)
        return where
    where = dict(z["labels"])
    for s in z["given"]:
        where.setdefault(z["grid"][s[0]][s[1]], []).append(s)
    return where


def locate(z, where, a, b, ans):
    g = z["grid"]
    for s in where.get(a, []):
        for e in where.get(b, []):
            dr, dc = e[0] - s[0], e[1] - s[1]
            n = max(abs(dr), abs(dc))
            if n == 0 or (dr and dc and abs(dr) != abs(dc)):
                continue
            cells = [(s[0] + dr // n * k, s[1] + dc // n * k) for k in range(n + 1)]
            if not ans or (len(cells) == len(ans) and all(g[r][c] in (ch, "?") for (r, c), ch in zip(cells, ans))):
                return cells
    return None


def convert(xdid: str) -> list[str]:
    path = HERE / f"{xdid}.xd"
    text = path.read_text(encoding="utf-8")
    z = W.parse(text)
    if z["meta"].get("Numbering") == "none" or not z["clues"]:  # No. 28: no clue list
        out = re.sub(r"^Numbering: .*\n", "", text, flags=re.M)
        path.write_text(out, encoding="utf-8")
        return []
    g, where, num = z["grid"], label_squares(z), modern_numbers(z["grid"])
    runs = {(d, num[cells[0]]): cells for d, cells in W.runs(g)}
    by_cells = {tuple(cells): k for k, cells in runs.items()}
    probs, new, pair_ref = [], {}, {}
    for a, b, body, ans in z["clues"]:
        pair = f"{a}-{b}"
        cells = locate(z, where, a, b, ans)
        k = by_cells.get(tuple(cells)) if cells else None
        if not k:
            probs.append(f"{pair} {ans}: not a whole across/down run")
            continue
        ref = f"{k[0]}{k[1]}"
        if ref in new:  # the paper printed a line twice (No. 26's 27-34, No. 29's 77-79): keep the clue that fits
            old = new[ref]
            elsewhere = lambda t: sum(q[2] == t for q in z["clues"]) > 1
            keep_new = elsewhere(old[1]) and not elsewhere(body)
            kept, dropped = ((body, old[1]) if keep_new else (old[1], body))
            meta = dict(old[3])
            dup = f'the list prints this pair twice; the other line reads "{pair}. {dropped}"' + (
                " (a repeated line)" if dropped != kept else "")
            meta["Note"] = "; ".join(filter(None, [meta.get("Note"), dup]))
            new[ref] = (k, kept, ans, meta)
            pair_ref[pair] = ref
            continue
        cm = dict(z["cmeta"].get(pair, {}))
        printed = cm.pop("Printed", None)
        meta = {"Printed": printed or pair}
        notes = [cm.pop("Note")] if "Note" in cm else []
        if printed:
            notes.insert(0, f"misprint: the pair that fits the grid is {pair}")
        if notes:
            meta["Note"] = "; ".join(notes)
        meta.update(cm)
        new[ref] = (k, body, ans, meta)
        pair_ref[pair] = ref
        if printed:
            pair_ref[printed] = ref
    if probs:
        return probs
    lines = []
    for d in "AD":
        group = sorted((v for v in new.values() if v[0][0] == d), key=lambda v: v[0][1])
        for (dd, n), body, ans, meta in group:
            ref = f"{dd}{n}"
            lines.append(f"{ref}. {body} ~ {ans}".replace(". ~", ". ~") if body else f"{ref}. ~ {ans}")
            lines += [f"{ref} ^{key}: {val}" for key, val in meta.items()]
        if group:
            lines.append("")
    # rebuild the file: drop Numbering and Labels, replace Clues
    parts = re.split(r"(?m)^(?=## )", text)
    out = []
    for p in parts:
        head = p.split("\n", 1)[0].strip().lower()
        if head == "## labels":
            continue
        if head == "## metadata":
            p = re.sub(r"^Numbering: .*\n", "", p, flags=re.M)
        if head == "## clues":
            p = "## Clues\n" + "\n".join(lines).rstrip("\n") + "\n\n\n"
        out.append(p)
    path.write_text("".join(out).rstrip("\n") + "\n", encoding="utf-8")
    bp = HERE / f"{xdid}.boxes.json"
    if bp.exists():
        bx = json.loads(bp.read_text(encoding="utf-8"))
        for it in bx.get("clues", []):
            ref = pair_ref.get(it.get("pair")) or pair_ref.get(it.get("printed", ""))
            if ref:
                it["ref"] = ref
            else:
                probs.append(f"boxes: no ref for {it.get('pair')}")
        bp.write_text(json.dumps(bx, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return probs


def keep(xdid: str):
    path = HERE / f"{xdid}.xd"
    text = path.read_text(encoding="utf-8")
    if KEEP[xdid] not in text:
        text = re.sub(r"^(Notes: .*)$", lambda m: m.group(1) + " " + KEEP[xdid], text, count=1, flags=re.M)
        path.write_text(text, encoding="utf-8")


def main():
    bad = 0
    for p in sorted(HERE.glob("nyw*.xd")):
        x = p.stem
        if x in KEEP:
            keep(x)
            print(f"{x}  kept in the World's form")
            continue
        probs = convert(x)
        print(f"{x}  {'ok' if not probs else '; '.join(probs)}")
        bad += bool(probs)
    sys.exit(bad)


if __name__ == "__main__":
    main()
