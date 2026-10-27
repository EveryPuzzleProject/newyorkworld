#!/usr/bin/env python3
"""Render site/index.html from status.tsv and series.tsv: every Sunday of the World's
FUN run as clipped / missing / to do, mismatches flagged, and the batch to clip next.

    python tools/render.py        # then open site/index.html

Runs in CI on every push (see .github/workflows/pages.yml). It draws only what
status.tsv records; flags are computed by tools/record.py check, not here.
"""
import collections
import csv
import datetime as dt
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/EveryPuzzleProject/newyorkworld"
CATALOG = "https://github.com/EveryPuzzleProject/catalog/blob/main/publications/new-york-world.md"
# Newspapers.com search for one date. The paper filter is added by hand on the site if needed;
# if this link form stops working, change it here only.
SEARCH = "https://www.newspapers.com/search/?query=%22cross-word%22&date={date}"
STATES = [  # (status, label, meaning)
    ("clipped", "Clipped", "page saved and indexed: number and heading recorded"),
    ("to-clip", "To clip", "expected in the paper; not yet saved"),
    ("missing-from-scans", "Missing from scans", "the page isn't on Newspapers.com (not a skip by the World)"),
    ("not-carried", "Not carried", "the paper ran no FUN puzzle that Sunday"),
    ("before-the-journal", "Before the Journal", "World Nos. 1-6, before the Journal's first reprint; another source needed"),
]
PAPERS = {"minneapolis-journal": "Minneapolis Journal", "pittsburgh-press": "Pittsburgh Press",
          "tacoma-daily-ledger": "Tacoma Daily Ledger", "boston-globe": "Boston Globe"}


def read(name: str) -> list[dict]:
    with open(ROOT / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


def e(s) -> str:
    return html.escape(s or "")


def link(url: str, text: str) -> str:
    return f'<a href="{e(url)}">{e(text)}</a>' if url else e(text)


def main() -> None:
    rows = read("status.tsv")
    series = read("series.tsv")
    label = {s: lab for s, lab, _ in STATES}
    count = collections.Counter(r["status"] for r in rows)
    by_year = collections.defaultdict(collections.Counter)
    for r in rows:
        by_year[r["sunday"][:4]][r["status"]] += 1
    flagged = [r for r in rows if r["flag"]]
    batch_rows = [r for r in rows if r["status"] == "to-clip" and r["batch"]]
    batch_no = batch_rows[0]["batch"] if batch_rows else ""
    done_batches = sorted({r["batch"] for r in rows if r["batch"] and r["status"] != "to-clip"}, key=int)
    numbered = [r for r in rows if r["status"] == "clipped" and r["world_no_printed"]]
    last_numbered = numbered[-1] if numbered else None
    unnumbered = [r for r in rows if r["status"] == "clipped" and not r["world_no_printed"]]
    first_unnumbered = unnumbered[0] if unnumbered else None
    clipped_by_year = {y: c["clipped"] for y, c in by_year.items()}

    def pill(status: str) -> str:
        return f'<span class="pill {e(status)}">{e(label.get(status, status))}</span>'

    def batch_table() -> str:
        if not batch_rows:
            return "<p>No batch is queued. Run <code>python tools/record.py queue</code> to assign the next 30 Sundays.</p>"
        body = "\n".join(
            f"<tr><td>{e(r['sunday'])}</td><td>No. {e(r['world_no_expected'])}</td><td>{e(PAPERS.get(r['source'], r['source']))}</td>"
            f"<td><a href=\"{SEARCH.format(date=r['sunday'])}\">search that date</a></td><td class=muted>{e(r['notes'])}</td></tr>"
            for r in batch_rows)
        return (f"<p>Batch <b>{e(batch_no)}</b>: {len(batch_rows)} Sunday{'s' * (len(batch_rows) != 1)} to save. "
                "Save each page as <i>Entire page, JPG</i>; the file name Newspapers.com gives it "
                "(<code>The_Minneapolis_Journal_1914_02_15_45.jpg</code>) is all the intake needs. "
                "If the next week's solution is on the same page as the next puzzle, one save covers both.</p>"
                '<div class="scroll"><table><thead><tr><th>Sunday</th><th>Expected World No.</th><th>Paper</th><th>Newspapers.com</th><th>Notes</th></tr></thead>'
                f"<tbody>{body}</tbody></table></div>")

    def flags_table() -> str:
        if not flagged:
            return "<p>Nothing flagged: every printed number is the expected one.</p>"
        body = "\n".join(
            f"<tr><td>{e(r['sunday'])}</td><td>No. {e(r['world_no_expected'])}</td><td>{('No. ' + e(r['world_no_printed'])) if r['world_no_printed'] else '<span class=muted>none</span>'}</td>"
            f"<td>{e(r['flag'])}</td><td class=muted>{e(r['notes'])}</td></tr>" for r in flagged)
        return ('<div class="scroll"><table><thead><tr><th>Sunday</th><th>Expected</th><th>Printed</th><th>Flag</th><th>Notes</th></tr></thead>'
                f"<tbody>{body}</tbody></table></div>")

    def bars() -> str:
        out = []
        for y in sorted(by_year):
            c = by_year[y]
            total = sum(c.values())
            seg = "".join(f'<span class="seg {s}" style="flex:{c[s]}" title="{lab}: {c[s]}"></span>' for s, lab, _ in STATES if c[s])
            out.append(f'<div class=bar><span class=yr>{y}</span><span class=track>{seg}</span><span class=n>{c["clipped"]}/{total}</span></div>')
        return "\n".join(out)

    def legend() -> str:
        return "".join(f'<span class=key><span class="sw {s}"></span>{lab} <span class=muted>({count[s]})</span></span>' for s, lab, _ in STATES)

    def series_rows() -> str:
        return "\n".join(
            f"<tr><td>{e(s['name'])}</td><td>{e(s['from'])}</td><td>{e(s['to'])}</td><td>{e(s['numbering'])}</td><td>{e(s['status'])}</td></tr>"
            for s in series)

    def table_rows() -> str:
        out = []
        for r in rows:
            printed = f"No. {e(r['world_no_printed'])}" if r["world_no_printed"] else ("<span class=muted>none</span>" if r["status"] == "clipped" else "")
            copy = " ".join(x for x in (e(PAPERS.get(r["source"], r["source"])) if r["status"] not in ("before-the-journal",) else "",
                                        e(r["copy_date"]) if r["copy_date"] and r["copy_date"] != r["sunday"] else "",
                                        f"p. {e(r['copy_page'])}" if r["copy_page"] else "") if x)
            clip = link(r["clipping_url"], "clipping") if r["clipping_url"] else ""
            sol = " ".join(x for x in (e(r["solution_date"]), f"p. {e(r['solution_page'])}" if r["solution_page"] else "",
                                       link(r["solution_clipping_url"], "clipping") if r["solution_clipping_url"] else "") if x)
            out.append(
                f'<tr data-state="{e(r["status"])}" class="{"flagged" if r["flag"] else ""}"><td>{e(r["sunday"])}</td><td>No. {e(r["world_no_expected"])}<span class=muted title="inferred: 1913-12-21 plus n-1 weeks">*</span></td>'
                f"<td>{printed}</td><td>{pill(r['status'])}</td><td>{copy} {clip}</td><td>{e(r['heading'])}</td><td>{sol}</td>"
                f"<td>{e(r['batch'])}</td><td>{('<b>' + e(r['flag']) + '</b> ') if r['flag'] else ''}{e(r['notes'])}</td></tr>")
        return "\n".join(out)

    numbering_note = ""
    if last_numbered:
        numbering_note += f"The latest clipped grid with a printed number is {last_numbered['sunday']} (No. {last_numbered['world_no_printed']}). "
    if first_unnumbered:
        numbering_note += f"The earliest clipped grid with no number is {first_unnumbered['sunday']}. "
    if not numbering_note:
        numbering_note = "Nothing clipped yet beyond February 1914."

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The World's FUN Crosswords</title>
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --muted:#6b6a65; --line:#e3e0d8; --card:#ffffff; --accent:#1c4f8a; --warn:#a33a1c;
  --s-clipped:#2f6f4f; --s-to-clip:#d9d5cc; --s-missing-from-scans:#c4572c; --s-not-carried:#9a5fb0; --s-before-the-journal:#b9b5aa; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#7aaee0; --warn:#e0794f;
  --s-clipped:#5fae86; --s-to-clip:#3b3a36; --s-missing-from-scans:#e0794f; --s-not-carried:#b98ad0; --s-before-the-journal:#55534d; }} }}
:root[data-theme="dark"] {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#7aaee0; --warn:#e0794f;
  --s-clipped:#5fae86; --s-to-clip:#3b3a36; --s-missing-from-scans:#e0794f; --s-not-carried:#b98ad0; --s-before-the-journal:#55534d; }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 Georgia, "Times New Roman", serif }}
main {{ max-width:1040px; margin:0 auto; padding:32px 16px 64px }}
h1 {{ font-size:2rem; margin:0 0 4px }} h2 {{ margin:40px 0 8px; font-size:1.35rem; border-bottom:2px solid var(--fg); padding-bottom:4px }}
a {{ color:var(--accent) }} .muted {{ color:var(--muted) }} .lede {{ font-size:1.1rem }} code {{ font-size:0.9em }}
.cta {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent); padding:16px 20px; margin:20px 0 }}
.rule {{ background:var(--card); border:1px solid var(--line); padding:12px 20px; margin:16px 0; font-size:0.95rem }}
table {{ width:100%; border-collapse:collapse; font:14px/1.4 system-ui, sans-serif }}
th, td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); vertical-align:top }}
th {{ font-weight:600 }} .scroll {{ overflow-x:auto }} td:first-child {{ white-space:nowrap }}
tr.flagged td {{ background:color-mix(in srgb, var(--warn) 10%, transparent) }}
.bar {{ display:flex; align-items:center; gap:8px; font:12px system-ui, sans-serif; margin:2px 0 }}
.yr {{ width:3em; color:var(--muted) }} .n {{ width:4.5em; text-align:right; color:var(--muted) }}
.track {{ flex:1; display:flex; height:12px; border-radius:2px; overflow:hidden; background:var(--s-to-clip) }}
.seg.clipped, .sw.clipped, .pill.clipped {{ background:var(--s-clipped) }} .seg.to-clip, .sw.to-clip, .pill.to-clip {{ background:var(--s-to-clip) }}
.seg.missing-from-scans, .sw.missing-from-scans, .pill.missing-from-scans {{ background:var(--s-missing-from-scans) }}
.seg.not-carried, .sw.not-carried, .pill.not-carried {{ background:var(--s-not-carried) }}
.seg.before-the-journal, .sw.before-the-journal, .pill.before-the-journal {{ background:var(--s-before-the-journal) }}
.legend {{ display:flex; flex-wrap:wrap; gap:14px; font:13px system-ui, sans-serif; margin:8px 0 }}
.key {{ display:inline-flex; align-items:center; gap:6px }} .sw {{ width:12px; height:12px; border-radius:2px; display:inline-block }}
.pill {{ font-size:12px; padding:1px 6px; border-radius:9px; color:#fff; white-space:nowrap }}
.pill.to-clip, .pill.before-the-journal {{ color:var(--fg) }}
.filters {{ display:flex; flex-wrap:wrap; gap:8px; margin:8px 0; font:14px system-ui, sans-serif }}
input, select {{ font:inherit; padding:4px 8px; background:var(--card); color:var(--fg); border:1px solid var(--line); border-radius:4px }}
footer {{ margin-top:48px; font:13px system-ui, sans-serif; color:var(--muted) }}
</style></head><body><main>
<h1>The New York World's FUN crosswords, 1913–1917</h1>
<p class="lede">The first crossword ran in the New York World's Sunday FUN supplement on December 21, 1913, and a new one every Sunday after.
Other papers reprinted the section, so where the World's own pages are lost, a partner's copy is a second copy of the puzzle.
This page tracks one row per Sunday, {rows[0]['sunday']} to {rows[-1]['sunday']}: {len(rows)} puzzles, clipped from the Minneapolis Journal
(and, where it stops carrying FUN, the Pittsburgh Press or the Tacoma Daily Ledger).</p>
<p>Clipped so far: <b>{count['clipped']}</b> of {len(rows)}. {numbering_note}</p>

<div class="rule"><b>The dating rule.</b> The World printed its series number in the grid (No. 7 on 1914-02-01, No. 8 on 1914-02-08, in the Journal).
That fits one puzzle every Sunday from No. 1 on 1913-12-21, so World No. <i>n</i> is expected on 1913-12-21 plus <i>n</i>−1 weeks, and the Journal
ran each on the World's own date. <b>Every "expected" number and World date here is an inference from that count</b>, marked *; the printed number is
what the clipping shows. A printed number that differs from the expected one, repeats, or jumps is flagged: that is a skip, a repeat or a misprint by the World,
which is what this run is looking for. A page missing from the scans is never counted as a skip.</div>

<h2 id="next">Next batch to clip</h2>
{batch_table()}
<p class=muted>Batches done: {', '.join(done_batches) or 'none yet'}. Newspapers.com allows about 30 high-resolution saves a day.</p>

<h2 id="flags">Flags</h2>
<p>Sundays whose printed number isn't the expected one, or that repeat or jump against the nearest numbered clipping before them (a skip, repeat or misprint by the World), and clipped rows still missing their saved page or number.</p>
{flags_table()}

<h2>Progress by year</h2>
<div class="legend">{legend()}</div>
{bars()}

<h2>The series and its copies</h2>
<div class="scroll"><table><thead><tr><th>Series</th><th>From</th><th>To</th><th>Numbering</th><th>Status</th></tr></thead><tbody>
{series_rows()}
</tbody></table></div>

<h2>Every Sunday</h2>
<div class="filters"><input id="q" type="search" placeholder="Search date, number, heading, notes…">
<select id="st"><option value="">All</option>{''.join(f'<option value="{s}">{lab}</option>' for s, lab, _ in STATES)}</select>
<label><input type="checkbox" id="fl"> flagged only</label></div>
<div class="scroll"><table id="all"><thead><tr><th>Sunday</th><th>Expected*</th><th>Printed</th><th>Status</th><th>Copy</th><th>Heading</th><th>Solution</th><th>Batch</th><th>Notes</th></tr></thead><tbody>
{table_rows()}
</tbody></table></div>

<footer>Part of the <a href="https://github.com/EveryPuzzleProject">Every Puzzle Project</a>. Data: <a href="{REPO}">{REPO.split('github.com/')[1]}</a>
(status.tsv); what's known about the World's puzzles: the <a href="{CATALOG}">catalog entry</a>. Page images stay out of this repo.
Generated {dt.date.today().isoformat()}.</footer>
</main>
<script>
const q=document.getElementById('q'), st=document.getElementById('st'), fl=document.getElementById('fl'), rows=[...document.querySelectorAll('#all tbody tr')];
function f(){{const t=q.value.toLowerCase(), s=st.value, o=fl.checked; for(const r of rows) r.hidden=(s&&r.dataset.state!==s)||(o&&!r.classList.contains('flagged'))||(t&&!r.textContent.toLowerCase().includes(t));}}
q.addEventListener('input',f); st.addEventListener('change',f); fl.addEventListener('change',f);
</script>
</body></html>
"""
    out = ROOT / "site"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"site/index.html: {len(rows)} Sundays, {count['clipped']} clipped, {len(flagged)} flagged, batch {batch_no or '-'} with {len(batch_rows)} to clip")


if __name__ == "__main__":
    main()
