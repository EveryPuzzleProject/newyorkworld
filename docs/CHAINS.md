# Chains: which puzzle follows which, proved page by page

A World date on the status page is an inference from a weekly count. A chain doesn't depend on
the count. Each link says that a page's printed solution answers an earlier puzzle, so the order of
the puzzles rests on what was printed. This file gives the method and the result as of 2026-10-31.
The live tables are `chains.tsv`, `chain_breaks.tsv` and `chain_pages.tsv`, drawn on the
[status page](https://everypuzzleproject.github.io/newyorkworld/#chains).

## What a link is

**Verified link:** the solution grid printed on page B has the same shape as the puzzle grid on
page A, and its answers fit A's numbering, checked by eye on the scans. A and B may be different
papers: Tacoma's solution of 1917-01-28 proves the puzzle Los Angeles printed six weeks later.
The puzzle after the link is B's own, or, if B has only a solution, the same paper's next puzzle
within two weeks. If a link's own solution says otherwise, `next_page` in `links.tsv` names it.

The evidence, strongest first:

| Kind | What it is | Where it's recorded |
|---|---|---|
| dated | a printed date: the World Magazine box ("June 17"), the Globe's "Solution of Puzzle Sept 9" | `links.tsv` |
| label | a printed "Solution to No. 16" | `solution_of` |
| grid | shape and answers compared by eye | `continuity`, `links.tsv` |
| printed numbers | two consecutive numbers printed by the World, up to 1915-01-17 | `world_no_printed` |
| series | **tentative, not verified**: no solution ties the puzzles, but they plainly belong together | `links.tsv`, verdict `tentative` |

A verdict in `links.tsv` overrides `continuity`. Only verdicts go in. Nobody types clues or answers
into the tables. Checks follow [CHAIN-BRIEF.md](CHAIN-BRIEF.md) and go through `tools/import_links.py`.

**A chain** is a maximal run of adjacent puzzles, every pair linked. The series is dated, so a
puzzle goes by its inferred World Sunday in gxd's form, `nyw1914-02-01`. Its number follows in
brackets: a property of the puzzle through 1915-01-17, a convenience index after that, never the
identity. A puzzle with no World date yet (the Journal's pages of 1915, the Globe from 1918) goes
by its page. The puzzles stand in this order: 1914-02-01 to 1914-12-27, the Journal's pages of
1915, 1915-11-21 to 1917-12-30, the Globe's Sundays from 1918. A chain is **anchored** if it holds
a printed number or the 1917 solutions-box dates, otherwise **floating**: its order is proved, but
where it sits on the calendar isn't.

A chain that rests on a tentative link is marked tentative in `chains.tsv` and on the page, and
counts of verified and tentative links are kept apart. There are two: F to U and U to N, the
letter-shaped puzzles of 1915-01-24 to 02-07, plainly a sequence spelling FUN (Alex DeJarnatt,
2026-10-31). They ran without solutions, so no solution can prove them.

**An empty week** is a World Sunday no paper has a puzzle for, passed over by a link. From 1915
such a link doesn't break the chain, because the week exists only in the count. Before that it
does, because the World printed the numbers on either side, so that puzzle exists.

## Result

10 chains, 9 breaks, 2 of the links tentative. All 828 pages are accounted for in `chain_pages.tsv`: 699 sit in exactly
one chain, 117 are the Globe's own weekday series, 11 hold no puzzle, and one, the World's
1914-01-11 (No. 4), comes before the chains start on 1914-02-01 (No. 7).

| Chain | Span | Puzzles | Anchor |
|---|---|---|---|
| C1 | 1914-02-01 (No. 7) to 1914-08-02 (No. 33) | 27 | printed numbers |
| C2 | 1914-08-16 (No. 35) to 1914-11-08 (No. 47) | 13 | printed numbers |
| C3 | 1914-11-15 (No. 48) to 1914-12-13 (No. 52) | 5 | floating |
| C4 | 1914-12-27 (No. 54) to the Journal's 1915-02-07 (F, U, N) | 4 | printed number; **tentative**, 2 of its 3 links |
| C5 | the Journal's 1915-03-07 to 04-04 | 5 | floating |
| C6 | the Journal's 1915-04-11 to 05-23 | 6 | floating |
| C7 | the Journal's 1915-06-06 | 1 | floating |
| C8 | the Journal's 1915-06-27 to 07-25 | 5 | floating |
| **C9** | **1915-11-21 (No. 101) to 1917-12-30 (No. 211)** | 107 | solutions box |
| **C10** | **the Globe, 1918-01-06 to 1924-10-12** | 353 | floating |

## The breaks, and the page that closes each

| Break | Why | Page to find |
|---|---|---|
| 1914-08-02 / 08-16 | the Journal never ran 08-09 (No. 34); its page answers No. 33 | the World's own page |
| 1914-11-08 / 11-15 | the Journal's 12-06 solution is too small to read; shape agrees, answers can't be checked | the World's own page, or a better scan of the Journal's |
| 1914-12-13 / 12-27 | 12-20 (No. 53) lost; the Journal's 1915-01-17 page answers its 01-03 | the World's own page |
| N / 1915-03-07 | the Journal's 02-14, 02-21 and 02-28 have no puzzle, at least in the scans Newspapers.com holds (Alex DeJarnatt, browsed, 2026-10-31); its 03-07 page prints no previous solution, which fits | another paper's copy; no partner known in 1915 |
| 1915-04-04 / 04-11 | the 04-04 puzzle is held only as a clip with no clue list; the 04-11 solution has its grid, but the answers can't be checked, and 03-28 has the same grid | **the Journal's full 1915-04-04 page** (Alex has found it) |
| 1915-05-23 / 06-06 | no solution held for 05-23; the Journal's 05-30 has no puzzle (Alex DeJarnatt, page by page, 2026-10-31) | another paper's copy; no partner known in 1915 |
| 1915-06-06 / 06-27 | 06-27's solution answers a puzzle between them | the Journal's 1915-06-20: Alex found only an answer key in the issue, so another paper's copy |
| 1915-07-25 / 11-21 | no partner known, August to mid-November 1915 | any partner paper; the Journal's own 1915-08-01 |
| 1917-12-30 / the Globe | not a broken link: the Globe's solutions go on, but its order stops being the World's | dated copies from another paper, 1918 on |

**The join.** 1917-02-11 / 02-18 was the last break before the solutions box. Alex found the
Pittsburgh Press of 1917-03-04 (clip, 2026-10-31): the same puzzle as Shreveport's that day, 1917-02-18
(No. 166). Pittsburgh's 02-25 page has no puzzle and prints the 02-11 solution, so 03-04's is the next
puzzle in its run. That closes the link, and 107 puzzles, November 1915 to December 1917, now reach
the box. The week with no puzzle is also where Pittsburgh's lag goes from one week to two. The full
page adds a good copy; the link doesn't wait for it. Alex looked through the 03-04 issue and it has
no solutions anywhere, which fits: no new puzzle ran the week before. The puzzle's own solution is
already held, on Shreveport 1917-03-11, so 02-18 links forward to 02-25 without Pittsburgh.

## What the chains corrected

- **Nine World dates were wrong and are fixed.** The Journal's pages of 1916-11-05 to 11-26 move
  back one week: it printed one puzzle twice (10-29, 11-05), ran a week late, and dropped a puzzle
  to catch up. Fort Wayne printed the Journal's 11-26 puzzle a week earlier, on 11-19, so the
  Journal was late. Tacoma's January 1917 rows were a week off (its lag was one week until 02-04),
  as was Shreveport 02-11. Los Angeles 1917-01-14 carried a stale No. 279, from the withdrawn Globe
  numbers, and is 1916-12-03 (No. 155).
- **1916-08-13, 09-10 and 1917-02-18 are no longer wanted,** and 1916-11-26 and 1917-01-14 now have
  their true copies: they were held in partner papers without a date. Another 114 copies took dates,
  nearly all from the same first clue as a dated copy, the README's rule. `tools/world_dates_copies.py`
  holds the rules.
- **Los Angeles 1916-10-22 is 1916-07-16 (No. 135) again,** the same grid 14 weeks later.
- **Journal 1915-04-04 exists.** The "not carried" was derived from a shape-only "yes". Checking
  answers showed that "yes" was wrong, and Alex then found the page. Its clipped solution answers
  03-28. It reruns the 03-28 grid with a different solution, so by the README's rule it's a second
  puzzle. Of the 16 shape-only links rechecked, 14 held, this one failed, and one (1914-11-08 /
  11-15) can't be read.
- **Empty weeks.** 1916-10-01, 10-15, 1917-05-20 and 06-24 are in no paper. The World Magazine box
  goes June 17 to July 1, so 06-24 is confirmed: the World ran no puzzle that Sunday. The rest are
  held up by links only. 1916-10-08 (the Journal's date) might be 10-15: Tacoma's run could allow either.

## Open questions

**Did the World itself skip weeks in 1914?** The holiday puzzles fit the Journal's date, not the
World date the count gives:

| Puzzle | Journal | Count says | Theme |
|---|---|---|---|
| No. 25 | 1914-06-28 | 06-07 | "Fourth of July flavor" |
| No. 46 | 1914-11-22 | 11-01 | Thanksgiving |
| No. 50 | 1914-12-20 | 11-29 | Christmas |
| No. 51 | 1914-12-27 | 12-06 | the New Year is near |

A paper wouldn't run a holiday puzzle a month early. So the Journal may not have been behind at all:
the World may have skipped weeks in May and June 1914, and the count may put its dates up to three
weeks too early from there on. That would change this file's 1914 dates, which is one reason the
printed numbers stay beside them. It needs a dated World page from the second half of 1914. Nothing
in the tables has been changed for it. Nos. 46-52 also carry a caution: the puzzle lost between
No. 45 and No. 54 could sit anywhere in that run, so those numbers may be one too low.

**Did the Globe drift, or reprint?** `reruns.tsv` lists printings with the first clue of a puzzle
at least six months older. Seventeen of them are Globe Sundays from 1918-10 to 1919-06, mostly
1916 puzzles, out of order. If they are reprints, the Globe wasn't late in those months, it
was using old stock. It also happens in 1917: the puzzles of 08-05, 09-16, 09-30 and 10-21 have the
first clues of 1916-11-19, 06-11, 07-09 and 07-02, and the 08-05 one is in four papers, so the World
or its syndicate reran it. These are first-clue matches only, and shapes often read differently, so
they are **candidates**, not the same puzzle; that's Alex's call, and nothing was changed for them.

## Keeping it current

`python tools/record.py rebuild` recomputes everything. After an intake, run
`tools/world_dates_1917.py`, then `tools/world_dates_copies.py`. A cross-paper check goes in with
`record.py link PUZZLE_FILE SOLUTION_FILE kind=grid verdict=yes checked_by=…`.
