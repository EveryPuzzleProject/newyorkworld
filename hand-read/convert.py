"""One-off (2026-11-17): the hand-read xd files from Saul's Numbering: map to the form of
docs/NUMBERING-GIVENS.md (worldxd.py). Rewrites hand-read/<xdid>.xd and the pairs in
<xdid>.boxes.json; prints every clue reference it changed.

    python convert.py            # dry run: what would change
    python convert.py --write
"""
import json, re, sys
from pathlib import Path
import worldxd as W

HERE = Path(__file__).resolve().parent
# the rule each puzzle fits, tested 2026-11-17 against the readings (docs/NUMBERING-GIVENS.md);
# No. 3 has no solution: across-first by eye, as Nos. 4-8
RULE = {x: "across-first" for x in """nyw1914-01-04 nyw1914-01-11 nyw1914-01-18 nyw1914-01-25 nyw1914-02-01
nyw1914-02-08 nyw1914-02-15 nyw1914-03-01 nyw1914-03-08 nyw1914-03-29 nyw1914-04-05 nyw1914-04-26
nyw1914-05-10 nyw1914-05-31 nyw1914-06-21 nyw1914-08-16 nyw1914-08-23""".split()}
RULE.update({"nyw1913-12-21": "apex-first", "nyw1914-02-22": "apex-first", "nyw1913-12-28": "reading-order",
             "nyw1914-04-12": "reading-order", "nyw1914-06-14": "reading-order", "nyw1914-07-19": "none"})
# given squares the old maps can't show unambiguously (0-based): No. 27's FUN cross, No. 13's centre E
GIVEN_FIX = {"nyw1914-07-12": {(5, 9), (5, 10), (5, 11), (4, 10), (6, 10)}, "nyw1914-03-15": {(6, 6)}}
# No. 3 (no solution, so its pairs can't be placed): its reader's two misprints, from the doubts file
FIX_NO3 = {"6-23": "6-28", "10-16": "10-26"}
UNCLUED = {"nyw1913-12-21": ["2-3"], "nyw1914-04-12": ["1-2", "33-34"], "nyw1914-06-14": ["63-77"],
            "nyw1914-06-21": ["11-19"], "nyw1914-08-16": ["17-18"]}
OFFGRID = {"nyw1914-03-15": {r: "its middle letter is printed on the corner between two squares (the inner star): the grid has no square for it"
                             for r in ("E-38", "40-E", "42-E", "E-44")}}
NOTE_UNCLUED = {("nyw1913-12-21", "2-3"): "no clue printed in the Sentinel; the World's own page (gxd, via T Campbell) has 'What bargain hunters enjoy.'"}


def old_parse(text):
    parts = re.split(r"\n\s*\n\s*\n", text.strip("\n"), maxsplit=3)
    heads = parts[0].splitlines()
    grid = [l.strip() for l in parts[1].splitlines() if l.strip()]
    clues, mp = [], []
    rest = "\n\n\n".join(parts[2:])
    i = rest.find("Numbering:")
    if i >= 0:
        mp = rest[i:].splitlines()
        rest = rest[:i]
    for l in rest.splitlines():
        if l.strip():
            clues.append(l.rstrip())
    return heads, grid, clues, mp


def symbols(key_line: str) -> dict:
    """{symbol: number} from a map's key line ('Numbering: a=10 z=35 A=36 Z=61 α=62 ω=86 ...'):
    explicit pairs, and the run between two pairs when their codepoints step with their numbers."""
    pairs = [(s, int(n)) for s, n in re.findall(r"(\S)=(\d+)", key_line)]
    out = {str(d): d for d in range(1, 10)}
    for (s1, n1), (s2, n2) in zip(pairs, pairs[1:] + [(None, None)]):
        out[s1] = n1
        if s2 and n2 - n1 == ord(s2) - ord(s1) and n2 > n1:
            for k in range(n2 - n1 + 1):
                out[chr(ord(s1) + k)] = n1 + k
    return out


def main(write: bool):
    changed_all = []
    for f in sorted(HERE.glob("nyw*.xd")):
        x = f.stem
        heads, grid, clues, mp = old_parse(f.read_text(encoding="utf-8"))
        if x == "nyw1914-01-04":
            grid = [row.replace(".", "?") for row in grid]
        sym = symbols(mp[0]) if mp else {}
        old_labels, given = {}, set()
        for r, row in enumerate(mp[1:]):
            for c, ch in enumerate(row):
                if ch in sym:
                    old_labels[(r, c)] = str(sym[ch])
                elif "A" <= ch <= "Z" and r < len(grid) and c < len(grid[0]) and grid[r][c] == ch:
                    given.add((r, c))  # Saul's map shows a printed letter as itself
        given = GIVEN_FIX.get(x, given)
        rule = RULE.get(x, "as-printed")
        lab = W.number(grid, rule, given) if rule in W.RULES else dict(old_labels)
        if rule == "as-printed":
            for sq in given:
                lab.setdefault(sq, grid[sq[0]][sq[1]])
        where = {}
        for sq, v in lab.items():
            where.setdefault(v, []).append(sq)
        # clue lines: the reference that fits the grid under the labels, the printed one kept
        new_clues, changes = [], []
        for l in clues:
            m = W.REF.match(l)
            a, b, body, ans = m.group(1), m.group(2), m.group(3) or "", m.group(4) or ""
            ref = f"{a}-{b}"
            new = ref
            if x == "nyw1914-01-04":
                new = FIX_NO3.get(ref, ref)
            elif rule != "none" and ans:
                fits = []
                for (s, e, d) in place(grid, ans):
                    if s in lab and e in lab:
                        fits.append(f"{lab[s]}-{lab[e]}")
                fits = list(dict.fromkeys(fits))
                if ref not in fits and len(fits) > 1:  # a word that reads the same both ways: keep the end it shares with the print
                    fits = [q for q in fits if set(q.split("-")) & {a, b}][:1] or fits
                if ref not in fits and len(fits) == 1:
                    new = fits[0]
                elif ref not in fits:
                    print(f"  {x} {ref} ~ {ans}: can't place it under the labels ({fits})")
            line = f"{new}. {body}" + (f" ~ {ans}" if ans else "")
            new_clues.append(line.rstrip())
            if new != ref:
                new_clues.append(f"{new} ^Printed: {ref}")
                changes.append((ref, new, ans))
        # words the readers found with no printed clue (their doubts files); not printed whole as givens
        for ref in UNCLUED.get(x, []):
            a, b = ref.split("-")
            s_, e_ = where[a][0], where[b][0]
            n = max(abs(e_[0] - s_[0]), abs(e_[1] - s_[1]))
            word = "".join(grid[s_[0] + (e_[0] - s_[0]) // n * k][s_[1] + (e_[1] - s_[1]) // n * k] for k in range(n + 1))
            new_clues.append(f"{ref}. ~ {word}")
            new_clues.append(f"{ref} ^Note: {NOTE_UNCLUED.get((x, ref), 'no clue printed')}")
            changes.append(("(none)", ref, word))
        for ref, why in OFFGRID.get(x, {}).items():
            new_clues.append(f"{ref} ^Offgrid: {why}")
        # the file
        out = ["## Metadata"] + [h for h in heads if not h.startswith("Numbering")] + [f"Numbering: {rule}", "", "", "## Grid"] + grid
        out += ["", "", "## Clues"] + new_clues
        if rule == "as-printed":
            out += ["", "", "## Labels"]
            for sq, v in sorted(lab.items(), key=lambda t: (not t[1].isdigit(), int(t[1]) if t[1].isdigit() else 0, t[0])):
                if v.isdigit():
                    out.append(f"{v} r{sq[0] + 1}c{sq[1] + 1}")
        if given:
            out += ["", "", "## Design", "G { given: true }", ""]
            out += ["".join("G" if (r, c) in given else "." for c in range(len(grid[0]))) for r in range(len(grid))]
        for ch in changes:
            changed_all.append((x,) + ch)
        if write:
            f.write_text("\n".join(out) + "\n", encoding="utf-8")
            bj = HERE / f"{x}.boxes.json"
            z = json.loads(bj.read_text(encoding="utf-8"))
            for old, new, ans in changes:
                if old == "(none)":
                    continue
                for c in z.get("clues", []):
                    if c.get("pair") == old and (not ans or c.get("answer") == ans):
                        c.setdefault("printed", old)
                        c["pair"] = new
            bj.write_text(json.dumps(z, indent=1, ensure_ascii=False), encoding="utf-8")
    for row in changed_all:
        print("  ".join(row))
    print(len(changed_all), "clue lines changed or added")


def place(grid, ans):
    out = []
    H, Wd = len(grid), len(grid[0])
    for r in range(H):
        for c in range(Wd):
            for dr, dc in W.DIRS:
                if all(0 <= r + dr * k < H and 0 <= c + dc * k < Wd and grid[r + dr * k][c + dc * k] == ch for k, ch in enumerate(ans)):
                    out.append(((r, c), (r + dr * (len(ans) - 1), c + dc * (len(ans) - 1)), (dr, dc)))
    return out


if __name__ == "__main__":
    main("--write" in sys.argv)
