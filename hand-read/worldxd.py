"""The World's FUN crosswords (1913-14) in .xd: their numbering rules, the new form's parser, and
its checker (docs/NUMBERING-GIVENS.md).

    python worldxd.py check [xdid ...]     # every hand-read/*.xd, or the ones named

The form: v4 headed sections. `Numbering:` in the metadata names the rule that places the printed
end-square numbers (across-first, apex-first, reading-order), or says as-printed (a `## Labels`
section lists every label and its square) or none. A clue `a-b.` is the word from label a to
label b in a straight line. A given square (a letter printed in the puzzle's grid) is marked `G`
in the `## Design` section; it takes no number, and a clue that names it as an end uses its letter.
"""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULES = ("across-first", "apex-first", "reading-order")
DIRS = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
REF = re.compile(r"^([^\s.^]+)-([^\s.^]+)\.(?: (.*?))?(?: ~ (\S+))?\s*$")
META = re.compile(r"^([AD]\d+|[^\s.^]+-[^\s.^]+) \^([A-Za-z]+): (.*)$")
MODERN = re.compile(r"^([AD]\d+)\.(.*)$")


def is_square(ch: str) -> bool:
    return ch.isalpha() or ch == "?"


def runs(grid):
    """The across and down runs of 2+ squares: [(cells...)], in reading order of their first square."""
    out = []
    H, W = len(grid), len(grid[0])
    for r in range(H):
        c = 0
        while c < W:
            if is_square(grid[r][c]):
                e = c
                while e + 1 < W and is_square(grid[r][e + 1]):
                    e += 1
                if e > c:
                    out.append(("A", [(r, k) for k in range(c, e + 1)]))
                c = e + 1
            else:
                c += 1
    for c in range(W):
        r = 0
        while r < H:
            if is_square(grid[r][c]):
                e = r
                while e + 1 < H and is_square(grid[e + 1][c]):
                    e += 1
                if e > r:
                    out.append(("D", [(k, c) for k in range(r, e + 1)]))
                r = e + 1
            else:
                r += 1
    return out


def number(grid, rule: str, given: set) -> dict:
    """{(r, c): label} under the rule (0-based squares). A given square that ends a word is labelled
    by its letter and takes no number."""
    rs = runs(grid)
    across = sorted([cells for d, cells in rs if d == "A"])
    every = sorted({cells[i] for _, cells in rs for i in (0, -1)})
    out, n = {}, 0

    def take(sq):
        nonlocal n
        if sq in out:
            return
        if sq in given:
            out[sq] = grid[sq[0]][sq[1]]
            return
        n += 1
        out[sq] = str(n)

    if rule == "reading-order":
        for sq in every:
            take(sq)
        return out
    if rule == "apex-first":
        top = min(r for r, _ in every)
        for sq in every:
            if sq[0] == top:
                take(sq)
    elif rule != "across-first":
        raise ValueError(rule)
    for cells in across:
        take(cells[0])
        take(cells[-1])
    for sq in every:
        take(sq)
    return out


def parse(text: str) -> dict:
    """The new form: {meta, grid, clues: [(a, b, body, answer)], cmeta: {ref: {key: value}}, labels, design}."""
    secs, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s*(\w+)\s*$", line)
        if m:
            cur = m.group(1).lower()
            secs[cur] = []
        elif cur:
            secs[cur].append(line)
    meta = dict(l.split(": ", 1) for l in secs.get("metadata", []) if ": " in l)
    grid = [l.strip() for l in secs.get("grid", []) if l.strip()]
    clues, cmeta = [], {}
    for l in secs.get("clues", []):
        if not l.strip():
            continue
        m = META.match(l)
        if m:
            cmeta.setdefault(m.group(1), {})[m.group(2)] = m.group(3)
            continue
        m = MODERN.match(l)
        if m:  # the modern form: A<n>. / D<n>., with the World's pair as ^Printed:
            body, _, ans = m.group(2).partition("~")
            clues.append((m.group(1), "", body.strip(), (ans.split() or [""])[0]))
            continue
        m = re.match(r"^([^\s.^]+)-([^\s.^]+)\.(.*)$", l)
        if not m:
            raise ValueError(f"clue line: {l!r}")
        body, _, ans = m.group(3).partition(" ~ ")
        clues.append((m.group(1), m.group(2), body.strip(), (ans.split() or [""])[0]))
    labels = {}
    for l in secs.get("labels", []):
        if l.strip():
            lab, sq = l.split()
            r, c = re.match(r"r(\d+)c(\d+)$", sq).groups()
            labels[lab] = labels.get(lab, []) + [(int(r) - 1, int(c) - 1)]
    design = [l.strip() for l in secs.get("design", []) if l.strip() and "{" not in l]
    given = {(r, c) for r, row in enumerate(design) for c, ch in enumerate(row) if ch == "G"}
    return {"meta": meta, "grid": grid, "clues": clues, "cmeta": cmeta, "labels": labels, "design": design, "given": given}


def check(path: Path, notes: list | None = None) -> list[str]:
    z = parse(path.read_text(encoding="utf-8"))
    g, probs = z["grid"], []
    if not g:
        return ["no grid"]
    W = len(g[0])
    if any(len(r) != W for r in g):
        probs.append("grid rows differ in length")
    if z["design"] and (len(z["design"]) != len(g) or any(len(r) != W for r in z["design"])):
        probs.append("design grid is not the grid's size")
    rule = z["meta"].get("Numbering", "")
    if not rule:
        return probs + check_modern(z, notes)
    if rule in RULES:
        num = number(g, rule, z["given"])
        where = {}
        for sq, lab in num.items():
            where.setdefault(lab, []).append(sq)
        if z["labels"]:
            probs.append(f"Numbering: {rule} and a Labels section")
    elif rule == "as-printed":
        where = dict(z["labels"])
        for sq in z["given"]:  # a given letter can always name its own square
            where.setdefault(g[sq[0]][sq[1]], []).append(sq)
    elif rule == "none":
        where = {}
    else:
        return [f"Numbering: {rule!r} is not a rule"]
    covered = set()
    for a, b, body, ans in z["clues"]:
        ref = f"{a}-{b}"
        if "Offgrid" in z["cmeta"].get(ref, {}):  # a word the grid can't hold (No. 13's inner star)
            continue
        if a not in where or b not in where:
            probs.append(f"{ref}: label {a if a not in where else b} is not on the grid")
            continue
        fits = []
        for s in where[a]:
            for e in where[b]:
                dr, dc = e[0] - s[0], e[1] - s[1]
                n = max(abs(dr), abs(dc))
                if n == 0 or (dr and dc and abs(dr) != abs(dc)):
                    continue
                cells = [(s[0] + dr // n * k, s[1] + dc // n * k) for k in range(n + 1)]
                fits.append(cells)
        if not fits:
            probs.append(f"{ref}: its labels are not on one line")
            continue
        if not ans:
            if "?" not in "".join(g):  # a puzzle with no solution printed (No. 3) has no answers
                probs.append(f"{ref}: no answer")
            covered |= {tuple(c) for c in fits}
            continue
        ok = [c for c in fits if len(c) == len(ans) and all(g[r][k] in (ch, "?") for (r, k), ch in zip(c, ans))]
        if not ok:
            probs.append(f"{ref}: {ans} doesn't run from {a} to {b} ({len(fits[0])} squares)")
        else:
            covered.add(tuple(ok[0]))
    for ref in z["cmeta"]:
        if ref not in {f"{a}-{b}" for a, b, _, _ in z["clues"]}:
            probs.append(f"metadata for {ref}, which has no clue line")
    if rule in RULES:  # every word of the grid has a clue line, but a word printed whole as a given
        for d, cells in runs(g):
            if tuple(cells) not in covered and tuple(reversed(cells)) not in covered and not set(cells) <= z["given"]:
                (notes if notes is not None else probs).append(
                    f"run {''.join(g[r][c] for r, c in cells)} ({num[cells[0]]}-{num[cells[-1]]}) has no clue line (two words' ends side by side, or a word to look at)")
    return probs


def modern_numbers(grid) -> dict:
    """{(r, c): n}: the usual crossword numbering (a square that starts an across or down run of two or more)."""
    sq = lambda r, c: 0 <= r < len(grid) and 0 <= c < len(grid[0]) and is_square(grid[r][c])
    num, n = {}, 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if sq(r, c) and ((not sq(r, c - 1) and sq(r, c + 1)) or (not sq(r - 1, c) and sq(r + 1, c))):
                n += 1
                num[(r, c)] = n
    return num


def check_modern(z, notes) -> list[str]:
    """The modern form: each A<n>/D<n> names a whole run, its answer is the grid's letters, and it
    carries the World's pair as ^Printed:. A run with no clue line is a note (a given word, or a
    word the paper printed no clue for, which then has a clue line with no text)."""
    g, probs = z["grid"], []
    num = modern_numbers(g)
    runs_by = {f"{d}{num[cells[0]]}": cells for d, cells in runs(g)}
    seen = set()
    for ref, _, body, ans in z["clues"]:
        if ref in seen:
            probs.append(f"{ref}: two clue lines")
        seen.add(ref)
        cells = runs_by.get(ref)
        if not cells:
            probs.append(f"{ref}: no such run in the grid")
            continue
        if ans and (len(ans) != len(cells) or any(g[r][c] not in (ch, "?") for (r, c), ch in zip(cells, ans))):
            probs.append(f"{ref}: {ans} is not the grid's {''.join(g[r][c] for r, c in cells)}")
        if not ans and "?" not in "".join(g):
            probs.append(f"{ref}: no answer")
        pr = z["cmeta"].get(ref, {}).get("Printed", "")
        if not re.match(r"^[^\s-]+-[^\s-]+$", pr):
            probs.append(f"{ref}: no ^Printed: pair")
        fits = z["cmeta"].get(ref, {}).get("Fits")
        if fits is not None and not re.match(r"^[^\s-]+-[^\s-]+$", fits):
            probs.append(f"{ref}: ^Fits: {fits!r} is not a pair")
    for ref in z["cmeta"]:
        if ref not in seen:
            probs.append(f"metadata for {ref}, which has no clue line")
    for ref, cells in runs_by.items():
        if ref not in seen and not set(cells) <= z["given"]:
            (notes if notes is not None else probs).append(f"run {ref} {''.join(g[r][c] for r, c in cells)} has no clue line")
    return probs


def main():
    names = sys.argv[2:] or sorted(p.stem for p in HERE.glob("nyw*.xd"))
    bad = 0
    for x in names:
        nt = []
        p = check(HERE / f"{x}.xd", nt)
        z = parse((HERE / f"{x}.xd").read_text(encoding="utf-8"))
        print(f"{x}  {z['meta'].get('Numbering', 'modern'):14} {len(z['clues']):3} clues  {'ok' if not p else str(len(p)) + ' problems'}")
        for q in p:
            print("    ", q)
        for q in nt:
            print("     note:", q)
        bad += bool(p)
    print(f"{len(names) - bad} of {len(names)} clean")


if __name__ == "__main__" and sys.argv[1:2] == ["check"]:
    main()
