#!/usr/bin/env python3
"""Render site/index.html from status.tsv (one row per World number), printings.tsv (one
row per copy we have a page for), searches.tsv (what was looked for) and papers.tsv.

    python tools/render.py        # then open site/index.html

Runs in CI on every push. It draws only what the tables record; flags and lags are
computed by tools/record.py rebuild, not here.
"""
import collections
import datetime as dt
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/EveryPuzzleProject/newyorkworld"
CATALOG = "https://github.com/EveryPuzzleProject/catalog/blob/main/publications/new-york-world.md"
# Newspapers.com search for one date. If this link form stops working, change it here only.
SEARCH = "https://www.newspapers.com/search/results/?date={date}&keyword=%22cross-word%22"  # Newspapers.com results URL; add &publication-ids=<id> per paper in papers.tsv `search`
RESULT_LABEL = {"found": "Found", "queued": "To do", "no-hit": "No hit", "not-carried": "Not carried", "missing-from-scans": "Missing from scans"}


def read(name: str) -> list[dict]:
    p = ROOT / name
    if not p.exists():
        return []
    lines = p.read_text(encoding="utf-8").splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, (l.split("\t") + [""] * len(head))[:len(head)])) for l in lines[1:] if l.strip()]


def e(s) -> str:
    return html.escape(s or "")


def link(url: str, text: str) -> str:
    return f'<a href="{e(url)}">{e(text)}</a>' if url else e(text)


def no_on(date: str) -> str:
    return str((dt.date.fromisoformat(date) - dt.date(1913, 12, 21)).days // 7 + 1)


def main() -> None:
    status = read("status.tsv")
    printings = read("printings.tsv")
    searches = read("searches.tsv")
    papers = {p["id"]: p for p in read("papers.tsv")}

    def pname(pid: str) -> str:
        return papers.get(pid, {}).get("name", pid)

    have = [r for r in status if r["status"] == "have"]
    numbered = [r for r in printings if r["world_no_printed"]]
    last_numbered = max(numbered, key=lambda r: r["date"]) if numbered else None
    unnumbered = [r for r in printings if not r["world_no_printed"]]
    first_unnumbered = min(unnumbered, key=lambda r: r["date"]) if unnumbered else None
    queued = [s for s in searches if s["result"] == "queued"]
    batch_no = queued[0]["batch"] if queued else ""
    flagged = [r for r in printings if r["flag"]]
    by_year = collections.defaultdict(collections.Counter)
    for r in status:
        by_year[r["sunday_inferred"][:4]][r["status"]] += 1

    def batch_table() -> str:
        if not queued:
            return "<p>No batch is queued. Run <code>python tools/record.py queue</code> for the next 30 Sundays.</p>"
        body = "\n".join(
            f"<tr><td>{e(s['date'])}</td><td>{e(pname(s['paper']))}</td><td>No. {no_on(s['date'])}</td><td>{e(s['batch'])}</td>"
            f"<td>{date_links(s)}</td><td class=muted>{e(s['note'])}</td></tr>"
            for s in sorted(queued, key=lambda s: (int(s["batch"] or 0), s["date"])))
        batches = sorted({s["batch"] for s in queued}, key=int)
        return (f"<p>Batch{'es' * (len(batches) != 1)} <b>{', '.join(batches)}</b>: {len(queued)} Sunday{'s' * (len(queued) != 1)} to find. Download the page as "
                "<i>Entire page, JPG</i> into <code>newyorkworld-scans/pages/</code>, keeping the name Newspapers.com gives it. "
                "If the search finds the puzzle in more than one paper that day, every distinct paper's copy is welcome. "
                "A date with no hit stays listed until it's recorded as no-hit, not carried or missing from scans.</p>"
                '<div class="scroll"><table><thead><tr><th>Sunday</th><th>Paper</th><th>World No. if on the World\'s date</th><th>Batch</th><th>Newspapers.com</th><th>Notes</th></tr></thead>'
                f"<tbody>{body}</tbody></table></div>")

    def date_links(s: dict) -> str:
        """Links for one queued paper+date: the paper's issue browse page (papers.tsv `browse`,
        a template with {y} {m} {d}) when known, and the site search: the paper's own template
        (papers.tsv `search`, with {date} or {y} {m} {d}) when known, else a plain date search."""
        y, m, d = s["date"].split("-")
        tpl = papers.get(s["paper"], {}).get("browse", "")
        out = []
        if tpl:
            out.append(f'<a href="{e(tpl.format(y=y, m=m, d=d))}">browse the issue</a>')
        tpl2 = papers.get(s["paper"], {}).get("search", "")
        if tpl2:
            url = tpl2.format(date=s["date"], y=y, m=m, d=d)
            out.append(f'<a href="{e(url)}">search this paper, this date</a>')
            if "%22cross-word%22" in url:
                out.append(f'<a href="{e(url.replace("%22cross-word%22", "puzzle"))}">same, for "puzzle"</a>')
        else:
            out.append(f'<a href="{SEARCH.format(date=s["date"])}">search that date</a>')
        return " · ".join(out)

    def gaps_table() -> str:
        gaps = read("gaps.tsv")
        miss = [g for g in gaps if g["kind"] == "missing-puzzle"]
        myst = [g for g in gaps if g["kind"] in ("mystery", "recheck")]
        skips = [g for g in gaps if g["kind"] == "skip-confirmed"]
        out = []
        if miss:
            body = "\n".join(
                f"<tr><td>{e(pname(g['paper']))}</td><td>{e(g['after'])} to {e(g['before'])}</td><td>"
                + " · ".join(f"{d[5:]} ({date_links({'paper': g['paper'], 'date': d})})" for d in g["sundays"].split())
                + f"</td><td class=muted>{e(g['evidence'])}</td></tr>" for g in miss)
            out.append('<div class="scroll"><table><thead><tr><th>Paper</th><th>Between</th><th>Sundays to probe</th><th>Evidence</th></tr></thead>'
                       f"<tbody>{body}</tbody></table></div>")
        else:
            out.append("<p>None open.</p>")
        if myst:
            out.append("<p><b>Mysteries</b> (consecutive pages, yet the solution is not the previous puzzle): " +
                       "; ".join(f"{pname(g['paper'])} {g['before']} <span class=muted>({e(g['evidence'])})</span>" for g in myst) + "</p>")
        if skips:
            out.append("<p class=muted><b>Skips confirmed</b> (nothing ran in between): " +
                       "; ".join(f"{pname(g['paper'])} {g['sundays'].replace(' ', ', ')}" for g in skips) + "</p>")
        return "\n".join(out)

    def lag_table() -> str:
        groups = collections.defaultdict(list)
        for r in printings:
            groups[r["paper"]].append(r)
        out = []
        for pid, rs in sorted(groups.items(), key=lambda kv: min(r["date"] for r in kv[1])):
            lags = sorted(int(r["lag_weeks"]) for r in rs if r["lag_weeks"] != "")
            nn = sum(1 for r in rs if r["world_no_printed"])
            dates = sorted(r["date"] for r in rs)
            if not lags:
                lag = "no numbered copy yet"
            elif lags[0] == lags[-1]:
                lag = f"{lags[0]} week{'s' * (lags[0] != 1)}"
            else:
                lag = f"{lags[0]} to {lags[-1]} weeks"
            heads = "; ".join(dict.fromkeys(r["heading"] for r in rs if r["heading"]))
            out.append(f"<tr><td>{e(pname(pid))}</td><td>{len(rs)}</td><td>{nn}</td><td>{e(dates[0])} to {e(dates[-1])}</td><td>{e(lag)}</td><td class=muted>{e(heads)}</td></tr>")
        return ('<div class="scroll"><table><thead><tr><th>Paper</th><th>Copies</th><th>Numbered</th><th>Dates seen</th><th>Behind the World\'s date</th><th>Headings</th></tr></thead>'
                f"<tbody>{''.join(out)}</tbody></table></div>")

    def flags_table() -> str:
        if not flagged:
            return "<p>Nothing flagged.</p>"
        body = "\n".join(
            f"<tr><td>{e(r['date'])}</td><td>{e(pname(r['paper']))}</td><td>{('No. ' + e(r['world_no_printed'])) if r['world_no_printed'] else '<span class=muted>none</span>'}</td>"
            f"<td>{e(r['flag'])}</td><td class=muted>{e(r['notes'])}</td></tr>" for r in flagged)
        return ('<div class="scroll"><table><thead><tr><th>Date</th><th>Paper</th><th>Printed</th><th>Flag</th><th>Notes</th></tr></thead>'
                f"<tbody>{body}</tbody></table></div>")

    def bars() -> str:
        out = []
        for y in sorted(by_year):
            c = by_year[y]
            total = sum(c.values())
            out.append(f'<div class=bar><span class=yr>{y}</span><span class=track><span class="seg have" style="flex:{c["have"]}"></span>'
                       f'<span class="seg wanted" style="flex:{c["wanted"]}"></span></span><span class=n>{c["have"]}/{total}</span></div>')
        return "\n".join(out)

    def cont(r: dict) -> str:
        """The continuity verdict as a short word with the evidence on hover."""
        v = r.get("continuity", "")
        if not v:
            return ""
        if v.startswith("vs "):
            v = v[14:]
        word = v.split(":")[0].split("(")[0].strip()
        label = {"yes": "yes, consecutive", "no": "no: a puzzle missing between", "none": "no solution printed", "unclear": "unclear", "recheck": "recheck"}.get(word, word)
        cls = {"yes": "have", "no": "warn", "none": "muted"}.get(word, "muted")
        return f'<span class="{cls}" title="{e(v)}">{e(label)}</span>'

    def printings_table() -> str:
        out = []
        for r in sorted(printings, key=lambda r: (r["date"], r["paper"])):
            printed = f"No. {e(r['world_no_printed'])}" if r["world_no_printed"] else "<span class=muted>none</span>"
            lag = f", lag {e(r['lag_weeks'])}w" if r["lag_weeks"] not in ("", "0") else ""
            world = f"No. {e(r['world_no'])} <span class=muted>({e(r['sunday_inferred'])}{lag})</span>" if r["world_no"] else ""
            sol = f"No. {e(r['solution_of'])}" if r["solution_of"] else e(r["solution_label"])
            flag = f"<b>{e(r['flag'])}</b> " if r["flag"] else ""
            out.append(f'<tr data-paper="{e(r["paper"])}" class="{"flagged" if r["flag"] else ""}"><td>{e(r["date"])}</td><td>{e(pname(r["paper"]))}</td>'
                       f"<td>{link(r['url'], 'p. ' + (r['page'] or '?'))}</td><td>{printed}</td><td>{world}</td><td>{e(r['heading'])}</td>"
                       f"<td>{e(r['credit'])}</td><td>{sol}</td><td>{cont(r)}</td><td class=muted>{e(r['copyright_line'])}</td><td>{flag}{e(r['notes'])}</td></tr>")
        return "\n".join(out)

    def groups_table() -> str:
        groups = collections.defaultdict(list)
        for r in printings:
            if r["puzzle_key"] and not r["world_no"]:
                groups[r["puzzle_key"]].append(r)
        sols = collections.defaultdict(list)
        for r in printings:
            if r["solution_of"] and not r["solution_of"].isdigit():
                sols[r["solution_of"]].append(r)
        if not groups:
            return "<p>None keyed yet.</p>"
        out = []
        for k, rs in sorted(groups.items(), key=lambda kv: min(r["date"] for r in kv[1])):
            rs.sort(key=lambda r: r["date"])
            copies = "; ".join(f"{pname(r['paper'])} {r['date']}" for r in rs)
            sol = "; ".join(f"{pname(r['paper'])} {r['date']}" for r in sorted(sols.get(k, []), key=lambda r: r["date"]))
            out.append(f"<tr><td>{e(k)}</td><td>{e(rs[0]['credit'])}</td><td class=muted>{e(rs[0]['fingerprint'])}</td><td>{e(copies)}</td><td>{e(sol)}</td><td class=muted>{e(rs[0]['match'])}</td></tr>")
        return ('<div class="scroll"><table><thead><tr><th>Key</th><th>Credit</th><th>First clue</th><th>Printed in</th><th>Solution printed in</th><th>How matched</th></tr></thead>'
                f"<tbody>{''.join(out)}</tbody></table></div>")

    def coverage() -> str:
        rows = [s for s in searches if s["result"] in ("no-hit", "not-carried", "missing-from-scans")]
        if not rows:
            return "<p>No Sundays recorded as no-hit, not carried or missing yet.</p>"
        body = "\n".join(f"<tr><td>{e(s['date'])}</td><td>{e(pname(s['paper']))}</td><td>{e(RESULT_LABEL[s['result']])}</td><td class=muted>{e(s['note'])}</td></tr>" for s in rows)
        return f'<div class="scroll"><table><thead><tr><th>Sunday</th><th>Paper</th><th>Result</th><th>Notes</th></tr></thead><tbody>{body}</tbody></table></div>'

    def status_table() -> str:
        out = []
        for r in status:
            flag = f"<b>{e(r['flag'])}</b> " if r["flag"] else ""
            label = "Have a copy" if r["status"] == "have" else "Wanted"
            out.append(f'<tr data-state="{e(r["status"])}" class="{"flagged" if r["flag"] else ""}"><td>No. {e(r["world_no"])}</td>'
                       f'<td>{e(r["sunday_inferred"])}<span class=muted title="inferred: 1913-12-21 plus n-1 weeks">*</span></td>'
                       f'<td><span class="pill {e(r["status"])}">{label}</span></td><td>{e(r["copies"])}</td>'
                       f"<td>{e(r['heading'])}</td><td>{e(r['credit'])}</td><td class=muted>{e(r['fingerprint'])}</td><td>{e(r['solution_seen'])}</td><td>{flag}{e(r['notes'])}</td></tr>")
        return "\n".join(out)

    numbering_note = ""
    if last_numbered:
        numbering_note += f"The latest copy with a printed number is {pname(last_numbered['paper'])} {last_numbered['date']} (No. {last_numbered['world_no_printed']}). "
    if first_unnumbered:
        numbering_note += f"The earliest copy with no number is {pname(first_unnumbered['paper'])} {first_unnumbered['date']}. "
    paper_options = "".join(f'<option value="{e(pid)}">{e(pname(pid))}</option>' for pid in sorted({r["paper"] for r in printings}, key=pname))

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The World's FUN Crosswords</title>
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --muted:#6b6a65; --line:#e3e0d8; --card:#ffffff; --accent:#1c4f8a; --warn:#a33a1c;
  --s-have:#2f6f4f; --s-wanted:#d9d5cc; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#7aaee0; --warn:#e0794f;
  --s-have:#5fae86; --s-wanted:#3b3a36; }} }}
:root[data-theme="dark"] {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#7aaee0; --warn:#e0794f;
  --s-have:#5fae86; --s-wanted:#3b3a36; }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 Georgia, "Times New Roman", serif }}
main {{ max-width:1100px; margin:0 auto; padding:32px 16px 64px }}
h1 {{ font-size:2rem; margin:0 0 4px }} h2 {{ margin:40px 0 8px; font-size:1.35rem; border-bottom:2px solid var(--fg); padding-bottom:4px }}
a {{ color:var(--accent) }} .muted {{ color:var(--muted) }} .lede {{ font-size:1.1rem }} code {{ font-size:0.9em }}
.rule {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent); padding:12px 20px; margin:16px 0; font-size:0.95rem }}
table {{ width:100%; border-collapse:collapse; font:14px/1.4 system-ui, sans-serif }}
th, td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); vertical-align:top }}
th {{ font-weight:600 }} .scroll {{ overflow-x:auto }} td:first-child {{ white-space:nowrap }}
tr.flagged td {{ background:color-mix(in srgb, var(--warn) 10%, transparent) }}
.bar {{ display:flex; align-items:center; gap:8px; font:12px system-ui, sans-serif; margin:2px 0 }}
.yr {{ width:3em; color:var(--muted) }} .n {{ width:4.5em; text-align:right; color:var(--muted) }}
.track {{ flex:1; display:flex; height:12px; border-radius:2px; overflow:hidden; background:var(--s-wanted) }}
.seg.have, .pill.have {{ background:var(--s-have) }} .seg.wanted, .pill.wanted {{ background:var(--s-wanted) }}
.warn {{ color:var(--warn) }} .have {{ color:var(--s-have) }}
.pill {{ font-size:12px; padding:1px 6px; border-radius:9px; color:#fff; white-space:nowrap }} .pill.wanted {{ color:var(--fg) }}
.filters {{ display:flex; flex-wrap:wrap; gap:8px; margin:8px 0; font:14px system-ui, sans-serif }}
input, select {{ font:inherit; padding:4px 8px; background:var(--card); color:var(--fg); border:1px solid var(--line); border-radius:4px }}
footer {{ margin-top:48px; font:13px system-ui, sans-serif; color:var(--muted) }}
</style></head><body><main>
<h1>The New York World's FUN crosswords, 1913–1917</h1>
<p class="lede">The first crossword ran in the New York World's Sunday FUN supplement on December 21, 1913, and a new one every Sunday after.
Other papers reprinted the section, so where the World's own pages are lost, a partner's copy is a second copy of the puzzle.
This page tracks the World's series by number, No. 1 to No. {len(status)}, and every copy of each puzzle we have found in a partner paper.</p>
<p>Puzzles with at least one copy: <b>{len(have)}</b> of {len(status)}, from <b>{len(printings)}</b> printings in {len({r['paper'] for r in printings})} papers. {numbering_note}</p>

<div class="rule"><b>The dating rule.</b> The World printed its series number in the grid (No. 7 on 1914-02-01, No. 8 on 1914-02-08, in the Minneapolis Journal).
That fits one puzzle every Sunday from No. 1 on 1913-12-21, so World No. <i>n</i> is expected on 1913-12-21 plus <i>n</i>−1 weeks.
<b>Every World date here is an inference from that count</b>, marked *. A copy's own date is a printing date, days to weeks after the World's;
the gap is shown as its lag. A copy with a printed number is tied to that World puzzle; a copy with none is tied by its first clue and grid,
and the record says how. A number that repeats or jumps within one paper's run is flagged: a skip, repeat or misprint, which is what this run is looking for.
A page missing from the scans is never counted as a skip.</div>

<h2 id="next">Next batch to find</h2>
{batch_table()}

<h2 id="missing">Missing puzzles to find</h2>
<p>Where a page's "last week's solution" is not the previous page's puzzle, a puzzle ran in between that we don't have: probe these dates.
Where it is the previous page's puzzle, nothing ran in between and the dates are settled as not carried.</p>
{gaps_table()}

<h2 id="papers">The papers and how far behind the World they ran</h2>
<p>Each paper's lag is its printing date minus the World date inferred from the number. A steady lag means the paper ran late;
a lag that grows means the World skipped weeks, or the paper did.</p>
{lag_table()}

<h2 id="flags">Flags</h2>
{flags_table()}

<h2>Progress by year of the World's series</h2>
{bars()}

<h2 id="unnumbered">Unnumbered puzzles matched across papers</h2>
<p>From late 1914 the grids carry no number, so a puzzle is known only by its copies. Copies of one puzzle share a key; the dates show how far apart the papers ran it.</p>
{groups_table()}

<h2 id="printings">Every printing</h2>
<div class="filters"><select id="pp"><option value="">All papers</option>{paper_options}</select></div>
<div class="scroll"><table id="pr"><thead><tr><th>Printed</th><th>Paper</th><th>Page</th><th>Grid No.</th><th>World puzzle*</th><th>Heading</th><th>Credit</th><th>Solution on page</th><th>Follows previous?</th><th>Copyright line</th><th>Notes</th></tr></thead><tbody>
{printings_table()}
</tbody></table></div>

<h2 id="coverage">Sundays searched without a page</h2>
{coverage()}

<h2>Every World puzzle</h2>
<div class="filters"><input id="q" type="search" placeholder="Search number, date, heading, credit…">
<select id="st"><option value="">All</option><option value="have">Have a copy</option><option value="wanted">Wanted</option></select>
<label><input type="checkbox" id="fl"> flagged only</label></div>
<div class="scroll"><table id="all"><thead><tr><th>World No.</th><th>World date*</th><th>Status</th><th>Copies</th><th>Heading</th><th>Credit</th><th>First clue (key)</th><th>Solution seen</th><th>Notes</th></tr></thead><tbody>
{status_table()}
</tbody></table></div>

<footer>Part of the <a href="https://github.com/EveryPuzzleProject">Every Puzzle Project</a>. Data: <a href="{REPO}">{REPO.split('github.com/')[1]}</a>
(status.tsv, printings.tsv, searches.tsv); what's known about the World's puzzles: the <a href="{CATALOG}">catalog entry</a>. Page images stay out of this repo.
Generated {dt.date.today().isoformat()}.</footer>
</main>
<script>
const q=document.getElementById('q'), st=document.getElementById('st'), fl=document.getElementById('fl'), rows=[...document.querySelectorAll('#all tbody tr')];
function f(){{const t=q.value.toLowerCase(), s=st.value, o=fl.checked; for(const r of rows) r.hidden=(s&&r.dataset.state!==s)||(o&&!r.classList.contains('flagged'))||(t&&!r.textContent.toLowerCase().includes(t));}}
q.addEventListener('input',f); st.addEventListener('change',f); fl.addEventListener('change',f);
const pp=document.getElementById('pp'), prs=[...document.querySelectorAll('#pr tbody tr')];
pp.addEventListener('change',()=>{{for(const r of prs) r.hidden=pp.value&&r.dataset.paper!==pp.value;}});
</script>
</body></html>
"""
    out = ROOT / "site"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"site/index.html: {len(have)}/{len(status)} numbers have a copy, {len(printings)} printings, {len(flagged)} flagged, batch {batch_no or '-'} with {len(queued)} to find")


if __name__ == "__main__":
    main()
