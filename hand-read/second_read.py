"""Compare a blind second reading of the World clue lists with the hand-read xd (2026-11-25).

    python second_read.py <dir>     # <dir>/<xdid>.txt: PAIR<TAB>TEXT per printed line, read from the
                                     # scans by an agent that never saw the xd; writes <dir>/REPORT.md

Each printed line in the xd (the clue body, keyed by the pair the paper printed: `^Printed:` in the
modern form, the clue's own pair in the World's form, and any second printing kept in a `^Note:`) is
matched with the blind line of the same pair. Agreement is reported in three grades:
  same     the text is identical
  minor    identical once spacing, case and punctuation are ignored (a period, a comma)
  differs  the words differ, or a line is on one side only: these need a look at the scan
A blind word marked [?] (the reader wasn't sure) that matches ours counts as agreeing but is listed.
"""
import difflib, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import worldxd as W  # noqa: E402

OTHER = re.compile(r'the other line reads "([^ .]+)\. (.*?)"')


def ours(xdid):
    z = W.parse((HERE / f"{xdid}.xd").read_text(encoding="utf-8"))
    out = []
    for a, b, body, ans in z["clues"]:
        ref = f"{a}-{b}" if b else a
        meta = z["cmeta"].get(ref, {})
        pair = meta.get("Printed") or ref
        if body:
            out.append((pair, body, ref))
        for m in OTHER.finditer(meta.get("Note", "")):
            out.append((m.group(1), m.group(2), ref))
    return out


def theirs(path):
    out, notes = [], []
    for l in path.read_text(encoding="utf-8").splitlines():
        if l.startswith("#"):
            notes.append(l[1:].strip())
        elif "\t" in l:
            p, t = l.split("\t", 1)
            out.append((re.sub(r"\s", "", p).replace("[?]", ""), t.strip()))
    return out, notes


def norm(t):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", t.lower())).strip()


def grade(o, t):
    if o == t:
        return "same"
    clean = t.replace("[?]", "")
    clean = re.sub(r"\s+", " ", clean).strip()
    if o == clean:
        return "same?"
    if norm(o) == norm(clean):
        return "minor?" if "[?]" in t else "minor"
    return "differs"


def compare(xdid, d):
    mine = ours(xdid)
    blind, notes = theirs(d / f"{xdid}.txt")
    left = list(blind)
    rows = []
    sim = lambda a, b: difflib.SequenceMatcher(None, norm(a), norm(b.replace("[?]", ""))).ratio()
    unpaired = []
    for pair, text, ref in mine:
        cands = [x for x in left if x[0] == pair]
        if not cands:
            unpaired.append((pair, text, ref))
            continue
        best = max(cands, key=lambda x: sim(text, x[1]))
        left.remove(best)
        rows.append((grade(text, best[1]), ref, pair, text, best[1]))
    for pair, text, ref in unpaired:  # the readings disagree on the printed pair: match by text
        cands = [x for x in left if sim(text, x[1]) > .8]
        if not cands:
            rows.append(("differs", ref, pair, text, "(no blind line with this pair)"))
            continue
        best = max(cands, key=lambda x: sim(text, x[1]))
        left.remove(best)
        g = grade(text, best[1])
        rows.append(("pair" if g != "differs" else "differs", ref, pair, text, f"{best[0]}. {best[1]}"))
    for pair, text in left:
        rows.append(("differs", "", pair, "(no line of ours with this pair)", text))
    return rows, notes


def main():
    d = Path(sys.argv[1])
    tally = {"same": 0, "same?": 0, "minor": 0, "minor?": 0, "pair": 0, "differs": 0}
    body = []
    for f in sorted(d.glob("nyw*.txt")):
        x = f.stem
        rows, notes = compare(x, d)
        for r in rows:
            tally[r[0]] += 1
        look = [r for r in rows if r[0] != "same"]
        n = sum(r[0] in ("differs", "pair") for r in rows)
        body.append(f"\n## {x}: {len(rows)} lines, {n} differ\n")
        if look:
            body.append("| grade | ref | printed | ours | blind |\n|---|---|---|---|---|")
            body += [f"| {g} | {ref} | {p} | {o} | {t} |" for g, ref, p, o, t in
                     sorted(look, key=lambda r: ("differs", "pair", "minor", "minor?", "same?").index(r[0]))]
        if notes:
            body.append("\nThe blind reader noted: " + " / ".join(notes))
    head = ["# Blind second reading of the World clue lists, Nos. 1-33\n",
            "Grades: same = identical; same? = identical once the reader's [?] marks are dropped; "
            "minor = differs only in spacing, case or punctuation (a word broken at a line end is joined); pair = the text agrees but the two readings disagree on the printed number pair; differs = the words differ or a line is on one side only.\n",
            "Totals: " + ", ".join(f"{k} {v}" for k, v in tally.items())]
    (d / "REPORT.md").write_text("\n".join(head + body) + "\n", encoding="utf-8")
    print(tally)


if __name__ == "__main__":
    main()
