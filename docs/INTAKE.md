# Intake runbook: from page images to the record

The loop a Claude session runs when new page images arrive. It has run for 340 pages; follow
it exactly, and change the tools rather than improvising around them.

## 0. Where things are

- Images: `../newyorkworld-scans/pages/`, named as Newspapers.com downloads them:
  `The_Boston_Globe_1919_07_13_81.jpg` (paper, date, viewer page). A zip from a collaborator:
  unzip into a scratch folder first, then move only `*.jpg` page files into `pages/`; delete
  exact duplicates (names ending ` (1).jpg` whose bytes equal the original: `cmp`).
- The record: `printings.tsv` (one row per page, hand-indexed), `searches.tsv`, `status.tsv`
  (derived), `gaps.tsv` and `wanted.tsv` (derived), `papers.tsv`. Only `tools/record.py`
  writes them. `git pull --rebase` before starting: other sessions commit here too.

## 1. List the new pages

    python tools/new_with_prev.py > <scratch>/new_prev.txt

One line per unrecorded page with its previous found page of the same paper (shape, first
clue, world number) or "in this same batch". Pages whose name isn't in the
`Paper_YYYY_MM_DD_page` form are reported; fix the name or set `paper=` on `add`.

## 2. Index them with Sonnet agents

Spawn `general-purpose` agents on `model: sonnet`, about 10 pages each, **one paper per
agent** and the pages in date order (continuity is checked within a paper). Give each:

- the brief `docs/INDEX-BRIEF.md` (index only: number, heading, credit, copyright line,
  shape, first-clue fingerprint, solution label; never clues or answers), plus the extra
  field `continuity` (is the "last week's solution" on this page the previous found page's
  puzzle: exactly `yes` / `no` / `none` / `unclear`, with flat `evidence` and `confidence`);
- its lines from `new_prev.txt`; for the first page of a chunk whose previous page is in
  another chunk, name that page's file and tell the agent to open it only for grid shape and
  first clue;
- what the paper's copy looks like (the Globe: plain "Cross-Word Puzzle", hand-lettered
  numbers, no credit; FUN partners: "Fun's Cross-Word Puzzle", often a constructor credit);
- the exact output path `<scratch>/<group>.json`, a flat list of objects, and "final reply:
  3 lines".

About 100-140k Sonnet tokens per 10 pages. Agents drift in their JSON (nested `crosswords`,
`continuity_evidence`): the importers flatten both.

## 3. Import

    python tools/import_index.py <scratch>/<group>.json
    python tools/import_continuity.py <scratch>/<group>.json

Then by hand, with `python tools/record.py add <file> key=value ...`:
- a page with only a solution: `notes="no new puzzle on this page: ..."` (that phrase makes
  it solution-only for gaps and continuity);
- a copyright line that belongs to a story on the page, not the puzzle: `copyright_line=`;
- a misfiled paper (`Morning_Tribune` = `los-angeles-tribune`, `The_Times` =
  `shreveport-times`): `paper=<id>`;
- copies of one puzzle the first-clue grouping missed (spelling variants, "Meager"/"Meagre"):
  `puzzle_key=<shared key>` on each, with `match=` saying why.

## 4. World numbers

    python tools/world_dates_1917.py     # Globe/Journal date = World date; Tacoma minus two weeks (1917 on)
    python tools/world_dates_1916.py     # the Journal 1915-11-21 to 1917-01-28

Both are inferences and say so on every row; see their docstrings. The Globe rule is proven
through 1919 by the World Magazine solutions box (Tacoma 1917-07-22). For 1920 on, keep
applying it only while each Globe page answers the week before, and watch for the first
sign that the Globe's puzzle is no longer FUN's: a constructor credit of the Globe's own, a
changed heading, a break in continuity with nothing to explain it. The World's FUN ran no
new crosswords for about two months in early 1920 (Jerry King's puzzles replaced it in some
partners from March 1920). Record what the pages show; don't paper over it.

When a batch runs past the series table's end, raise `LAST_NO` in `tools/record.py` (one
constant, with the date in the comment).

## 5. Rebuild, render, commit, push

    python tools/record.py rebuild      # status, gaps, wanted, searches 'found', the scans repo's pages.tsv
    python tools/render.py
    git add -A && git commit -m "Intake: <paper> <first date> to <last date> (<n> pages)..." && git push
    cd ../newyorkworld-scans && git add -A && git commit -m "Pages: ..." && git push

`rebuild` prints the flags; look at any new one. Then queue the next batch if the open one
is done: `python tools/record.py queue --force --paper boston-globe --from <date> --n 30`.

## 6. Report

Three or four lines: pages in, the span now continuous, skips and missing puzzles found
(from `gaps.tsv` / `wanted.tsv`), anything odd an agent flagged (a reclued grid rerun counts
as a second puzzle; a World credit spelled in a grid is worth a note), and the queue.
