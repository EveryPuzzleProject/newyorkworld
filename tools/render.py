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
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/EveryPuzzleProject/newyorkworld"
CENSUS = "https://github.com/EveryPuzzleProject/census/blob/main/publications/new-york-world.md"
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


# How far along each World puzzle is, best first. The page leads with this.
STAGES = [
    ("gxd", "In gxd", "transcribed and in the gxd corpus"),
    ("shipped", "Transcribed", "transcribed and reviewed: an .xd in this repo's xd/ folder"),
    ("review", "In review", "read by OCR, on the review site, not yet passed"),
    ("have", "Page found", "a copy is held, not yet read"),
    ("wanted", "Wanted", "no copy found yet"),
    ("unused", "No such puzzle", "the World skipped this number"),
]
STAGE_LABEL = {k: label for k, label, _ in STAGES}
SERIES_END = 211  # the run this page is about: No. 211 is 1917-12-30; later rows are the Globe's, kept for research
REVIEW = "https://blitz.xwordapp.com/review/?p={pid}"
GXD_NOTE = re.compile(r"in gxd as (nyw\d{4}-\d\d-\d\d)")  # status notes record a puzzle already in gxd from elsewhere
UNUSED_NOTE = re.compile(r"never used")  # status notes record a number the World skipped


def stages(status: list[dict]) -> dict[str, dict]:
    """World No. -> {stage, why, link}: from status (have / wanted, and two notes phrases), the
    pipeline's ship record (pipeline/ship/*.json: OCR'd, in review, shipped) and xd/. The pipeline
    names puzzles by the inferred World date, so its rows are matched to numbers by that date."""
    no_by_date = {r["sunday_inferred"]: r["world_no"] for r in status}
    ship = {}
    for f in sorted((ROOT / "pipeline" / "ship").glob("*.json")):
        for p in json.loads(f.read_text(encoding="utf-8")).get("puzzles", []):
            n = no_by_date.get(p.get("date", ""))
            if n:
                ship[n] = p
    xd = {no_by_date.get(p.stem[3:13]) for p in (ROOT / "xd").glob("nyw*.xd")}
    out = {}
    for r in status:
        n, notes = r["world_no"], r["notes"]
        p = ship.get(n)
        m = GXD_NOTE.search(notes)
        if m:
            out[n] = {"stage": "gxd", "why": f"in gxd as {m.group(1)}", "link": ""}
        elif n in xd or (p and p.get("status") == "shipped"):
            out[n] = {"stage": "shipped", "why": "shipped from batch " + (p and p.get("pid", "") or ""), "link": REVIEW.format(pid=p["pid"]) if p else ""}
        elif p:
            out[n] = {"stage": "review", "why": f"held: {p.get('why') or p.get('reason', '')}", "link": REVIEW.format(pid=p["pid"])}
        elif r["status"] == "have":
            out[n] = {"stage": "have", "why": "", "link": ""}
        elif UNUSED_NOTE.search(notes):
            out[n] = {"stage": "unused", "why": notes, "link": ""}
        else:
            out[n] = {"stage": "wanted", "why": "", "link": ""}
    return out


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

    def wanted_by_paper() -> str:
        wanted = read("wanted.tsv")
        open_rows = [w for w in wanted if w["status"] in ("", "found", "queued")]
        done = [w for w in wanted if w["status"] in ("no-hit", "not-carried", "missing-from-scans")]
        if not wanted:
            return "<p>Nothing missing that a known partner could supply.</p>"
        by_paper = collections.defaultdict(list)
        for w in open_rows:
            by_paper[w["paper"]].append(w)
        out = []
        for pid, ws in sorted(by_paper.items(), key=lambda kv: -len(kv[1])):
            lis = "".join(f"<li><b>{e(w['date'])}</b> for {e(w['puzzle'])} <span class=muted>({e(w['why'])})</span> · {date_links({'paper': pid, 'date': w['date']})}</li>"
                          for w in sorted(ws, key=lambda w: w["date"]))
            out.append(f"<details open><summary><b>{e(pname(pid))}</b> · {len(ws)} date{'s' * (len(ws) != 1)} to try</summary><ul>{lis}</ul></details>")
        puzzles_open = sorted({w["puzzle"] for w in open_rows}, key=lambda p: (p.startswith("J"), p))
        head = f"<p>{len(puzzles_open)} missing puzzles with somewhere left to look; {len(done)} candidate dates already reported as dead ends.</p>"
        closed = sorted({w["puzzle"] for w in wanted} - set(puzzles_open))
        tail = (f"<p class=muted>No partner left to try for: {', '.join(e(c) for c in closed)}.</p>" if closed else "")
        return head + "\n".join(out) + tail

    def chains_section() -> str:
        chains, breaks = read("chains.tsv"), read("chain_breaks.tsv")
        if not chains:
            return "<p>Not computed yet.</p>"
        short = lambda s: s.replace("nyw", "").replace("minneapolis-journal ", "Journal ").replace("boston-globe ", "Globe ")
        t0, t1 = dt.date(1914, 2, 1), dt.date(1924, 10, 12)
        at = lambda d: 100 * (dt.date.fromisoformat(d) - t0).days / (t1 - t0).days
        cls = lambda c: ("fl" if c["anchor"].startswith("floating") else "an") + (" te" if c["standing"] == "tentative" else "")
        segs = "".join(f'<a class="cs {cls(c)}" href="#{e(c["chain"])}" style="left:{at(c["first_date"]):.2f}%;width:max(3px,{at(c["last_date"]) - at(c["first_date"]):.2f}%)" title="{e(c["chain"])}: {e(short(c["first"]))} to {e(short(c["last"]))}, {e(c["puzzles"])} puzzles"></a>' for c in chains)
        years = "".join(f'<span class="cy" style="left:{at(f"{y}-01-01") if y > 1914 else 0:.2f}%">{y}</span>' for y in range(1914, 1925))
        strip = f'<div class="ct">{segs}</div><div class="cyr">{years}</div>'
        after = {b["after"]: b for b in breaks}
        rows = []
        for c in chains:
            size = f'{e(c["puzzles"])} puzzle{"s" * (c["puzzles"] != "1")}, {e(c["verified_links"])} verified link{"s" * (c["verified_links"] != "1")}'
            if c["standing"] == "tentative":
                size += f'<br><span class=warn>tentative: {e(c["tentative_links"])} more link{"s" * (c["tentative_links"] != "1")} by series, no solution</span>'
            empty = f'<br><span class=muted>weeks with no puzzle in any paper, passed by a link: {e(short(c["empty_slots"]))}</span>' if c["empty_slots"] else ""
            rows.append(f'<tr id="{e(c["chain"])}"><td><b>{e(c["chain"])}</b></td><td>{e(short(c["first"]))} to {e(short(c["last"]))}{empty}</td>'
                        f'<td>{size}</td><td>{e(c["anchor"])}</td></tr>')
            b = after.get(c["last"])
            if b:
                w = f'{link_date(b)}' if b["want_paper"] else f'<span class=muted>{e(b["want_why"] or "nothing known to try")}</span>'
                rows.append(f'<tr class="brk"><td class=warn>break</td><td colspan=2><b>{e(b["reason"])}</b> <span class=muted>{e(short(b["detail"]))}</span></td><td>{w}</td></tr>')
        verified, tentative = (sum(int(c[k]) for c in chains) for k in ("verified_links", "tentative_links"))
        counts = f"<p>{len(chains)} chains, {len(breaks)} breaks: <b>{verified}</b> verified links, <b>{tentative}</b> tentative.</p>"
        return f'{strip}{counts}<div class="scroll"><table><thead><tr><th>Chain</th><th>Span</th><th>Size</th><th>Anchored by / page that joins the break</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

    def link_date(b: dict) -> str:
        return f'{e(pname(b["want_paper"]))} <b>{e(b["want_date"])}</b> · {date_links({"paper": b["want_paper"], "date": b["want_date"]})}'

    def reruns_table() -> str:
        rows = read("reruns.tsv")
        body = "".join(f'<tr><td>{e(pname(r["later_paper"]))} {e(r["later_date"])}</td><td>{e(pname(r["first_paper"]))} {e(r["first_date"])}</td><td>{e(r["weeks"])}</td><td class=muted>{e(r["later_shape"])} / {e(r["first_shape"])}</td></tr>' for r in rows)
        return (f'<details><summary>{len(rows)} printings with the first clue of a puzzle printed at least six months earlier</summary><div class="scroll"><table><thead><tr><th>Later printing</th>'
                f'<th>Earlier printing</th><th>Weeks apart</th><th>Shapes, later / earlier</th></tr></thead><tbody>{body}</tbody></table></div></details>')

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
            body = "".join(f"<tr><td>{e(pname(g['paper']))}</td><td>{e(g['before'])}</td><td>{e(g['after'])}</td><td>{e(g['kind'])}</td><td class=muted>{e(g['evidence'])}</td></tr>" for g in myst)
            out.append('<h3>Mysteries and rechecks</h3><p>Consecutive pages whose solution is not the previous puzzle (mystery), or a verdict made against a page that a newer page has since displaced (recheck).</p>'
                       f'<div class="scroll"><table><thead><tr><th>Paper</th><th>Page</th><th>Previous page</th><th>Kind</th><th>Evidence</th></tr></thead><tbody>{body}</tbody></table></div>')
        if skips:
            body = "".join(f"<tr><td>{e(pname(g['paper']))}</td><td>{e(g['sundays'].replace(' ', ', '))}</td><td>{e(g['after'])} to {e(g['before'])}</td><td class=muted>{e(g['evidence'])}</td></tr>" for g in skips)
            out.append("<h3>Skips confirmed</h3><p>Nothing ran on these Sundays: the later page's solution answers the earlier page's puzzle.</p>"
                       f'<div class="scroll"><table><thead><tr><th>Paper</th><th>Skipped</th><th>Between</th><th>Evidence</th></tr></thead><tbody>{body}</tbody></table></div>')
        return "\n".join(out)

    def coverage_grid() -> str:
        """One row per paper per year, one cell per Sunday: a copy we hold (links to the page on
        Newspapers.com), a Sunday searched and not carried, searched with no hit, or nothing yet.
        The top row is any copy at all for that Sunday."""
        pr_by = {}
        for r in printings:
            if r["file"].startswith("clip:") and not r["url"]:
                continue
            pr_by.setdefault((r["paper"], r["date"]), []).append(r)
        se_by = {(x["paper"], x["date"]): x for x in searches}
        papers_seen = sorted({r["paper"] for r in printings} | {x["paper"] for x in searches}, key=lambda p: (p != "minneapolis-journal", pname(p)))
        out = []
        for y in ("1913", "1914", "1915", "1916", "1917"):
            d = dt.date(int(y), 1, 1)
            d += dt.timedelta(days=(6 - d.weekday()) % 7)
            sundays = []
            while d.year == int(y):
                if dt.date(1913, 12, 21) <= d <= dt.date(1917, 12, 30):
                    sundays.append(d.isoformat())
                d += dt.timedelta(days=7)
            if not sundays:
                continue
            rows_html = []
            # top row: any copy
            cells = []
            for sd in sundays:
                have = [r for (p, dd), rs in pr_by.items() if dd == sd for r in rs]
                if have:
                    cells.append(f'<span class="c have" title="{e(sd)}: {", ".join(dict.fromkeys(pname(r["paper"]) for r in have))}"></span>')
                else:
                    cells.append(f'<span class="c none" title="{e(sd)}: no copy yet"></span>')
            rows_html.append(f'<div class="cr"><span class="cl"><b>any copy</b></span>{"".join(cells)}</div>')
            for p in papers_seen:
                cells = []
                any_this_year = False
                for sd in sundays:
                    rs = pr_by.get((p, sd))
                    x = se_by.get((p, sd))
                    if rs:
                        any_this_year = True
                        r0 = rs[0]
                        label = f"{pname(p)} {sd}" + (f": No. {r0['world_no_printed']}" if r0["world_no_printed"] else "") + (f" · {r0['heading']}" if r0["heading"] else "")
                        if r0["url"]:
                            cells.append(f'<a class="c have" href="{e(r0["url"])}" title="{e(label)}"></a>')
                        else:
                            cells.append(f'<span class="c have" title="{e(label)} (no link)"></span>')
                    elif x and x["result"] == "not-carried":
                        any_this_year = True
                        cells.append(f'<span class="c nc" title="{e(pname(p))} {e(sd)}: not carried. {e(x["note"])}"></span>')
                    elif x and x["result"] in ("no-hit", "missing-from-scans"):
                        any_this_year = True
                        cells.append(f'<span class="c nh" title="{e(pname(p))} {e(sd)}: {e(x["result"])}. {e(x["note"])}"></span>')
                    elif x and x["result"] == "queued":
                        any_this_year = True
                        cells.append(f'<span class="c q" title="{e(pname(p))} {e(sd)}: queued (batch {e(x["batch"])})"></span>')
                    else:
                        cells.append('<span class="c none"></span>')
                if any_this_year:
                    rows_html.append(f'<div class="cr"><span class="cl">{e(pname(p))}</span>{"".join(cells)}</div>')
            months = ""
            for sd in sundays:
                m = dt.date.fromisoformat(sd)
                months += f'<span class="c mo">{m.strftime("%b")[0] if m.day <= 7 else ""}</span>'
            out.append(f'<h3>{y}</h3><div class="cg"><div class="cr"><span class="cl"></span>{months}</div>{"".join(rows_html)}</div>')
        legend = ('<div class="legend"><span class=key><span class="c have"></span>copy held (click: the page on Newspapers.com)</span>'
                  '<span class=key><span class="c nc"></span>searched: not carried</span><span class=key><span class="c nh"></span>searched: no hit</span>'
                  '<span class=key><span class="c q"></span>queued</span><span class=key><span class="c none"></span>not looked for</span></div>')
        return legend + "\n".join(out)

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

    def bars_held() -> str:
        """Distinct puzzles held per year of first printing, against that year's Sundays."""
        seen = set(); per = collections.Counter()
        for r in sorted(printings, key=lambda r: r["date"]):
            if r["notes"].lower().startswith(("no new puzzle", "no crossword")):
                continue
            k = ("no", r["world_no"]) if r["world_no"] else (("key", r["puzzle_key"]) if r["puzzle_key"] else ("file", r["file"]))
            if k in seen:
                continue
            seen.add(k); per[r["date"][:4]] += 1
        out = []
        for y in sorted(per):
            d = dt.date(int(y), 1, 1); d += dt.timedelta(days=(6 - d.weekday()) % 7)
            sundays = 0
            while d.year == int(y):
                sundays += 1; d += dt.timedelta(days=7)
            have = min(per[y], sundays)
            out.append(f'<div class=bar><span class=yr>{y}</span><span class=track><span class="seg have" style="flex:{have}"></span>'
                       f'<span class="seg wanted" style="flex:{sundays - have}"></span></span><span class=n>{per[y]}/{sundays}</span></div>')
        return "\n".join(out)

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

    st = stages(status)
    series = [r for r in status if r["world_no"].isdigit() and int(r["world_no"]) <= SERIES_END]
    counts = collections.Counter(st[r["world_no"]]["stage"] for r in series)
    puzzle_copies = collections.defaultdict(list)   # World No. -> printings of its puzzle
    solution_copies = collections.defaultdict(list)  # World No. -> printings of its solution
    for r in printings:
        if r["world_no"] and not r["notes"].lower().startswith(("no new puzzle", "no crossword")):
            puzzle_copies[r["world_no"]].append(r)
        if r["solution_of"].isdigit():
            solution_copies[r["solution_of"]].append(r)

    def copy_links(rs: list[dict]) -> str:
        rs = sorted(rs, key=lambda r: (r["date"], r["paper"]))
        return "; ".join(link(r["url"], f"{pname(r['paper'])} {r['date']}") for r in rs)

    def tip(r: dict) -> str:
        n, s = r["world_no"], st[r["world_no"]]
        parts = [f"No. {n}", f"{r['sunday_inferred']}*", STAGE_LABEL[s["stage"]]]
        if puzzle_copies[n]:
            parts.append("copies: " + ", ".join(f"{pname(x['paper'])} {x['date']}" for x in sorted(puzzle_copies[n], key=lambda x: x["date"])))
        if solution_copies[n]:
            parts.append("solution: " + ", ".join(f"{pname(x['paper'])} {x['date']}" for x in sorted(solution_copies[n], key=lambda x: x["date"])))
        if s["why"]:
            parts.append(s["why"])
        return " · ".join(parts)

    def overview() -> str:
        legend = "".join(f'<span class=key><span class="sq {k}"></span><b>{label}</b> <span class=muted>{counts[k]}</span></span>'
                         for k, label, _ in STAGES if counts[k] or k in ("gxd", "shipped", "review", "have", "wanted"))
        years = []
        for y in ("1913", "1914", "1915", "1916", "1917"):
            cells = "".join(
                f'<a class="sq {st[r["world_no"]]["stage"]}{" sol" if solution_copies[r["world_no"]] else ""}" href="#n{e(r["world_no"])}" title="{e(tip(r))}">{e(r["world_no"])}</a>'
                for r in series if r["sunday_inferred"][:4] == y)
            years.append(f'<div class=yrow><span class=ylab>{y}</span><div class=cells>{cells}</div></div>')
        return (f'<div class=legend>{legend}</div>'
                f'<p class=muted>One square per World puzzle, No. 1 to No. {SERIES_END}, in order. Hover for the copies held; click for its row below. '
                'A dot means its solution is held too. Squares are placed by number, not by date: the World skipped some Sundays, so the dates drift from the count.</p>'
                + "".join(years))

    def needed() -> str:
        wanted_nos = [r for r in series if st[r["world_no"]]["stage"] == "wanted"]
        runs, cur = [], []
        for r in wanted_nos:
            if cur and int(r["world_no"]) != int(cur[-1]["world_no"]) + 1:
                runs.append(cur); cur = []
            cur.append(r)
        if cur:
            runs.append(cur)
        lis = []
        for run in runs:
            a, b = run[0], run[-1]
            nos = f"No. {a['world_no']}" if a is b else f"Nos. {a['world_no']}–{b['world_no']}"
            dates = a["sunday_inferred"] if a is b else f"{a['sunday_inferred']} to {b['sunday_inferred']}"
            why = "; ".join(dict.fromkeys(x["notes"] for x in run if x["notes"]))
            lis.append(f"<li><b>{nos}</b> <span class=muted>({e(dates)}*)</span>{' · ' + e(why[:260]) + ('…' if len(why) > 260 else '') if why else ''}</li>")
        review = [r for r in series if st[r["world_no"]]["stage"] == "review"]
        have = [r for r in series if st[r["world_no"]]["stage"] == "have"]
        out = [f"<h3>Puzzles with no copy yet ({len(wanted_nos)})</h3><ul>{''.join(lis)}</ul>"]
        if review:
            out.append(f"<h3>Read but not yet passed review ({len(review)})</h3><p>Nos. {', '.join(r['world_no'] for r in review)}: "
                       f'open one from the table below, or the <a href="https://blitz.xwordapp.com/review/">review site</a>.</p>')
        if have:
            out.append(f"<h3>Copies held, not yet read ({len(have)})</h3><p class=muted>Waiting for the OCR pipeline (xword-ocr, then review on blitz).</p>")
        out.append('<p>If you can reach one of the missing pages, please <a href="' + REPO + '/issues/new">open an issue</a> with the date and where you found it '
                   "(a clipping link is enough; please don't upload page images).</p>")
        return "\n".join(out)

    def puzzle_table() -> str:
        out = []
        for r in series:
            n, s = r["world_no"], st[r["world_no"]]
            label = STAGE_LABEL[s["stage"]]
            stage = f'<span class="pill {s["stage"]}">{link(s["link"], label) if s["link"] else e(label)}</span>'
            if s["stage"] == "review" and s["why"]:
                stage += f'<br><span class=muted>{e(s["why"][:120])}</span>'
            flag = f"<b class=warn>{e(r['flag'])}</b> " if r["flag"] else ""
            notes = r["notes"]
            notes_html = (f"<details><summary>{e(notes[:90])}…</summary>{e(notes)}</details>" if len(notes) > 110 else e(notes))
            out.append(f'<tr id="n{e(n)}" data-stage="{e(s["stage"])}"><td><b>{e(n)}</b></td><td>{e(r["sunday_inferred"])}<span class=muted>*</span></td>'
                       f'<td>{stage}</td><td>{copy_links(puzzle_copies[n]) or "<span class=muted>none</span>"}</td>'
                       f'<td>{copy_links(solution_copies[n]) or ""}</td><td>{e(r["heading"])}<br><span class=muted>{e(r["fingerprint"])}</span></td>'
                       f'<td>{flag}{notes_html}</td></tr>')
        opts = "".join(f'<option value="{k}">{label} ({counts[k]})</option>' for k, label, _ in STAGES if counts[k])
        return (f'<div class="filters"><select id="sg"><option value="">All {len(series)} puzzles</option>{opts}</select>'
                '<input id="q" type="search" placeholder="Search number, date, paper, heading…"></div>'
                '<div class="scroll"><table id="all"><thead><tr><th>No.</th><th>World date*</th><th>Stage</th><th>Puzzle copies</th><th>Solution copies</th>'
                f'<th>Heading / first clue</th><th>Notes</th></tr></thead><tbody>{"".join(out)}</tbody></table></div>')

    later = [r for r in status if r["world_no"].isdigit() and int(r["world_no"]) > SERIES_END]
    later_pr = [r for r in printings if r["date"] > "1917-12-30"]

    numbering_note = ""
    if last_numbered:
        numbering_note += f"The latest copy with a printed number is {pname(last_numbered['paper'])} {last_numbered['date']} (No. {last_numbered['world_no_printed']}). "
    if first_unnumbered:
        numbering_note += f"The earliest copy with no number is {pname(first_unnumbered['paper'])} {first_unnumbered['date']}. "
    paper_options = "".join(f'<option value="{e(pid)}">{e(pname(pid))}</option>' for pid in sorted({r["paper"] for r in printings}, key=pname))

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The World's FUN Crosswords</title>
<link rel="stylesheet" href="https://everypuzzleproject.org/site.css">
<style>
h1, h2 {{ font-family:inherit; font-weight:bold; line-height:inherit }} .epp-header .wrap {{ max-width:1100px }}
:root {{ --pg-bg:#fbfaf7; --fg:#1d1d1b; --pg-muted:#6b6a65; --pg-line:#e3e0d8; --card:#ffffff; --pg-accent:#1c4f8a; --warn:#a33a1c;
  --s-have:#2f6f4f; --s-wanted:#d9d5cc; --st-gxd:#1f5c3f; --st-shipped:#3d8a63; --st-review:#3b6ea8; --st-have:#e2c98a; --st-wanted:#e6e2d9; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --pg-bg:#161614; --fg:#ecebe6; --pg-muted:#a3a19a; --pg-line:#34332f; --card:#1f1f1c; --pg-accent:#7aaee0; --warn:#e0794f;
  --s-have:#5fae86; --s-wanted:#3b3a36; --st-gxd:#3f9a6c; --st-shipped:#5fae86; --st-review:#5b8fd0; --st-have:#8a7340; --st-wanted:#2c2b28; }} }}
:root[data-theme="dark"] {{ --pg-bg:#161614; --fg:#ecebe6; --pg-muted:#a3a19a; --pg-line:#34332f; --card:#1f1f1c; --pg-accent:#7aaee0; --warn:#e0794f;
  --s-have:#5fae86; --s-wanted:#3b3a36; --st-gxd:#3f9a6c; --st-shipped:#5fae86; --st-review:#5b8fd0; --st-have:#8a7340; --st-wanted:#2c2b28; }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--pg-bg); color:var(--fg); font:16px/1.55 Georgia, "Times New Roman", serif }}
main {{ max-width:1100px; margin:0 auto; padding:32px 16px 64px }}
h1 {{ font-size:2rem; margin:0 0 4px }} h2 {{ margin:40px 0 8px; font-size:1.35rem; border-bottom:2px solid var(--fg); padding-bottom:4px }}
a {{ color:var(--pg-accent) }} .muted {{ color:var(--pg-muted) }} .lede {{ font-size:1.1rem }} code {{ font-size:0.9em }}
.rule {{ background:var(--card); border:1px solid var(--pg-line); border-left:4px solid var(--pg-accent); padding:12px 20px; margin:16px 0; font-size:0.95rem }}
table {{ width:100%; border-collapse:collapse; font:14px/1.4 system-ui, sans-serif }}
th, td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--pg-line); vertical-align:top }}
th {{ font-weight:600 }} .scroll {{ overflow-x:auto }} td:first-child {{ white-space:nowrap }}
#pr {{ table-layout:fixed }} #pr td, #all td {{ white-space:normal; overflow-wrap:anywhere }} #pr td:first-child, #all td:first-child {{ white-space:normal }}
#pr th:nth-child(1) {{ width:7% }} #pr th:nth-child(2) {{ width:8% }} #pr th:nth-child(3) {{ width:4% }} #pr th:nth-child(4) {{ width:5% }} #pr th:nth-child(5) {{ width:8% }}
#pr th:nth-child(6) {{ width:11% }} #pr th:nth-child(7) {{ width:9% }} #pr th:nth-child(8) {{ width:13% }} #pr th:nth-child(9) {{ width:7% }} #pr th:nth-child(10) {{ width:7% }}
tr.flagged td {{ background:color-mix(in srgb, var(--warn) 10%, transparent) }}
.bar {{ display:flex; align-items:center; gap:8px; font:12px system-ui, sans-serif; margin:2px 0 }}
.yr {{ width:3em; color:var(--pg-muted) }} .n {{ width:4.5em; text-align:right; color:var(--pg-muted) }}
.track {{ flex:1; display:flex; height:12px; border-radius:2px; overflow:hidden; background:var(--s-wanted) }}
.seg.have {{ background:var(--s-have) }} .seg.wanted {{ background:var(--s-wanted) }}
.warn {{ color:var(--warn) }} .have {{ color:var(--s-have) }}
.ct {{ position:relative; height:18px; background:var(--s-wanted); border-radius:2px; margin:12px 0 2px; overflow:hidden }} .cs {{ position:absolute; top:0; bottom:0; border-right:1px solid var(--pg-bg) }}
.cs.an {{ background:var(--s-have) }} .cs.fl {{ background:var(--pg-accent) }} .cs.te {{ opacity:.55 }} .cyr {{ position:relative; height:16px; font:11px system-ui, sans-serif; color:var(--pg-muted); margin-bottom:10px }} .cy {{ position:absolute }}
tr.brk td {{ background:color-mix(in srgb, var(--warn) 7%, transparent) }}
.cg {{ font:11px system-ui, sans-serif; overflow-x:auto; margin:4px 0 12px }} .cr {{ display:flex; align-items:center; gap:2px; margin:2px 0 }}
.cl {{ width:11em; flex:none; color:var(--pg-muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis }}
.c {{ width:13px; height:13px; flex:none; border-radius:2px; display:inline-block; background:var(--s-wanted) }}
.c.have {{ background:var(--s-have) }} a.c.have:hover {{ outline:2px solid var(--pg-accent) }} .c.nc {{ background:var(--pg-line); border:1px solid var(--pg-muted); box-sizing:border-box }}
.c.nh {{ background:color-mix(in srgb, var(--warn) 45%, var(--pg-bg)) }} .c.q {{ background:color-mix(in srgb, var(--pg-accent) 40%, var(--pg-bg)) }} .c.none {{ background:var(--s-wanted); opacity:.45 }}
.c.mo {{ background:none; color:var(--pg-muted); font-size:10px; text-align:center; line-height:13px }} h3 {{ margin:14px 0 2px; font-size:1rem }}
.pill {{ font-size:12px; padding:1px 7px; border-radius:9px; white-space:nowrap }}
.filters {{ display:flex; flex-wrap:wrap; gap:8px; margin:8px 0; font:14px system-ui, sans-serif }}
input, select {{ font:inherit; padding:4px 8px; background:var(--card); color:var(--fg); border:1px solid var(--pg-line); border-radius:4px }}
.stats {{ display:flex; flex-wrap:wrap; gap:12px; margin:20px 0 8px }} .stats div {{ background:var(--card); border:1px solid var(--pg-line); border-radius:6px; padding:10px 16px; min-width:9em; font:14px system-ui, sans-serif }}
.stats b {{ display:block; font:bold 1.8rem Georgia, serif }} .stats span {{ color:var(--pg-muted) }}
.legend {{ display:flex; flex-wrap:wrap; gap:6px 16px; margin:8px 0; font:13px system-ui, sans-serif }} .key {{ display:inline-flex; align-items:center; gap:6px }}
.yrow {{ display:flex; gap:10px; align-items:flex-start; margin:6px 0 }} .ylab {{ width:3em; flex:none; font:13px system-ui, sans-serif; color:var(--pg-muted); padding-top:6px }}
.cells {{ display:flex; flex-wrap:wrap; gap:3px }}
.sq {{ position:relative; display:inline-flex; align-items:center; justify-content:center; width:30px; height:26px; border-radius:3px; font:11px system-ui, sans-serif; text-decoration:none; color:var(--fg); background:var(--st-wanted) }}
.legend .sq {{ width:14px; height:14px }} a.sq:hover {{ outline:2px solid var(--pg-accent) }}
.sq.gxd, .pill.gxd {{ background:var(--st-gxd); color:#fff }} .sq.shipped, .pill.shipped {{ background:var(--st-shipped); color:#fff }} .sq.review, .pill.review {{ background:var(--st-review); color:#fff }}
.sq.have, .pill.have {{ background:var(--st-have); color:var(--fg) }} .sq.wanted, .pill.wanted {{ background:var(--st-wanted); color:var(--pg-muted) }}
.sq.unused, .pill.unused {{ background:repeating-linear-gradient(45deg, transparent 0 4px, var(--pg-line) 4px 6px); color:var(--pg-muted); border:1px dashed var(--pg-muted) }}
.sq.sol::after {{ content:""; position:absolute; top:3px; right:3px; width:5px; height:5px; border-radius:50%; background:currentColor; opacity:.8 }}
.pill a {{ color:inherit }} details {{ margin:6px 0; border-top:1px solid var(--pg-line); padding:6px 0 }} details > summary {{ cursor:pointer }}
details details {{ border:0; padding:0; margin:0 }} #all td {{ font-size:13px }} #all td:nth-child(2) {{ white-space:nowrap }}
footer {{ margin-top:48px; font:13px system-ui, sans-serif; color:var(--pg-muted) }}
</style></head><body>
<header class="epp-header"><div class="wrap">
  <a href="https://everypuzzleproject.org/">Every Puzzle Project</a>
  <span class="epp-page">New York World</span>
  <nav><a href="https://github.com/EveryPuzzleProject/newyorkworld">Repo</a></nav>
</div></header>
<main>
<h1>The New York World's FUN crosswords, 1913–1917</h1>
<p class="lede">The first crossword ran in the New York World's Sunday FUN supplement on December 21, 1913, and a new one most Sundays after.
The World's own pages survive badly, but other papers reprinted FUN, crossword and all. The Every Puzzle Project is recovering the whole series,
No. 1 to No. {SERIES_END}, from those reprints, and transcribing each puzzle into the gxd crossword corpus.</p>

<div class="stats">
<div><b>{counts['gxd'] + counts['shipped']}</b><span>transcribed</span></div>
<div><b>{counts['review']}</b><span>in review</span></div>
<div><b>{counts['have']}</b><span>page found, not read</span></div>
<div><b>{counts['wanted']}</b><span>still wanted</span></div>
</div>

<h2 id="progress">Every puzzle at a glance</h2>
{overview()}

<h2 id="needed">What's needed</h2>
{needed()}

<h2 id="puzzles">Every puzzle</h2>
<p class=muted>* The World date is inferred from the number: No. <i>n</i> on 1913-12-21 plus <i>n</i>−1 weeks. In 1914 the World skipped some Sundays,
so from No. 22 on the real dates run two or three weeks later than shown (<a href="{REPO}/blob/main/docs/BEN-INTAKE-2026-11-16.md">details</a>).
Links go to the page on Newspapers.com where we have one.</p>
{puzzle_table()}
<p class=muted>The record runs on past 1917 ({len(later)} numbers to {later[-1]['sunday_inferred'] if later else ''}) for the Boston Globe's pages, {len(later_pr)} of them,
held without World numbers because the Globe fell out of step with the World after 1917. They are in the research detail below.</p>

<h2 id="research">Research detail</h2>
<p>How the record is built: every page found, every search, how copies are matched and linked, and what is still open.
Tasks where finding is the work: <a href="{REPO}/blob/main/RESEARCH.md">RESEARCH.md</a>. The intake loop: <a href="{REPO}/blob/main/README.md">README</a>.</p>

<details><summary><b>The dating rule</b></summary>
<div class="rule">The World printed its series number in the grid (No. 7 on 1914-02-01, No. 8 on 1914-02-08). One puzzle every Sunday from No. 1 on 1913-12-21
gives World No. <i>n</i> on 1913-12-21 plus <i>n</i>−1 weeks, and <b>every World date on this page is that inference</b>, marked *. A copy's own date is its printing date;
the difference is shown as its lag. A copy with a printed number is tied to that puzzle; a copy with none is tied by its first clue and grid, and the record says how.
A number that repeats or jumps within one paper's run is flagged. A page missing from the scans is never counted as a skip.
The Milwaukee Sentinel's copies (2026-11-16) show the count drifting in 1914: FUN ran no new crossword on 1914-05-17, 05-24 and 06-07, and never used the number 34,
so the papers' "lag" from May 1914 on is mostly the count's error.</div>
</details>

<details><summary><b>Next batch to find</b></summary>
{batch_table()}
</details>

<details><summary><b>Missing puzzles: where else to look</b></summary>
<p>One line per missing puzzle and the paper and date where its copy should be, worked out from each paper's known delay behind the
World in 1917 (the Globe ran on the World's date that year, and not after; Pittsburgh one to two weeks later, Tacoma and Shreveport two, New Orleans two to three,
Salt Lake three, the LA Tribune three to eight; in 1915-16 the delays are counted from the Journal). A date searched and not found is recorded as a dead end
(<code>record.py search &lt;paper&gt; &lt;date&gt; no-hit</code>) and drops out of the list.</p>
{wanted_by_paper()}
<h3>Gaps by paper</h3>
{gaps_table()}
</details>

<details><summary><b>Chains: which solution answers which puzzle</b></summary>
<p>A link says that a page's printed solution answers an earlier puzzle, checked on the scans. A chain is an unbroken run of links:
each puzzle's successor is proved, not inferred from a date. Green chains reach a fixed point (a printed grid number, or the World Magazine's dated solutions box of July 1917);
blue chains float. A chain resting on a tentative link is drawn paler. Method: <a href="{REPO}/blob/main/docs/CHAINS.md">docs/CHAINS.md</a>.</p>
{chains_section()}
<p>The same first clue can come back years later: the Globe seems to have reprinted much of 1916 in 1918 and 1919. Nothing here treats these as the same puzzle; they are for checking.</p>
{reruns_table()}
</details>

<details><summary><b>Coverage by week and paper</b></summary>
<p>Every Sunday of the run, one column each; one row per paper. A filled cell is a page we hold, and links to it on Newspapers.com.
The top row of each year shows whether any paper's copy of that Sunday is in.</p>
{coverage_grid()}
</details>

<details><summary><b>The papers and their lag behind the count</b></summary>
<p>Each paper's lag is its printing date minus the World date inferred from the number. Where two papers show the same lag on the same puzzles, the count is
probably wrong rather than both papers late.</p>
{lag_table()}
</details>

<details><summary><b>Flags</b> ({len(flagged)})</summary>
{flags_table()}
</details>

<details><summary><b>Progress by year</b></summary>
<p><b>Puzzles held, by the year they were printed.</b> Every distinct puzzle we have a page for, counted once, against the Sundays of that year.</p>
{bars_held()}
<p><b>World numbers with a copy</b>, by inferred year.</p>
{bars()}
</details>

<details><summary><b>Unnumbered puzzles matched across papers</b></summary>
<p>From late 1914 the grids carry no number, so a puzzle is known only by its copies. Copies of one puzzle share a key.</p>
{groups_table()}
</details>

<details><summary><b>Every printing</b> ({len(printings)} pages from {len({r['paper'] for r in printings})} papers)</summary>
<p class=muted>{numbering_note}</p>
<div class="filters"><select id="pp"><option value="">All papers</option>{paper_options}</select></div>
<div class="scroll"><table id="pr"><thead><tr><th>Printed</th><th>Paper</th><th>Page</th><th>Grid No.</th><th>World puzzle*</th><th>Heading</th><th>Credit</th><th>Solution on page</th><th>Follows previous?</th><th>Copyright line</th><th>Notes</th></tr></thead><tbody>
{printings_table()}
</tbody></table></div>
</details>

<details><summary><b>Sundays searched without a page</b></summary>
{coverage()}
</details>

<footer>Part of the <a href="https://github.com/EveryPuzzleProject">Every Puzzle Project</a>. Data: <a href="{REPO}">{REPO.split('github.com/')[1]}</a>
(status.tsv, printings.tsv, searches.tsv, links.tsv, chains.tsv, pipeline/ship); what's known about the World's puzzles: the <a href="{CENSUS}">census entry</a>. Page images stay out of this repo.
Generated {dt.date.today().isoformat()}.</footer>
</main>
<script>
const q=document.getElementById('q'), sg=document.getElementById('sg'), rows=[...document.querySelectorAll('#all tbody tr')];
function f(){{const t=q.value.toLowerCase(), s=sg.value; for(const r of rows) r.hidden=(s&&r.dataset.stage!==s)||(t&&!r.textContent.toLowerCase().includes(t));}}
q.addEventListener('input',f); sg.addEventListener('change',f);
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
