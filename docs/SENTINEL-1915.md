# The Milwaukee Sentinel's 1915 FUN pages (intake of 2026-11-16)

Alex DeJarnatt found the Milwaukee Sentinel's 1915 FUN pages on **GenealogyBank** (a new
source for this project: a search for "cross-word" in 1915) and saved 34 full pages covering
26 Sundays, 1915-01-03 to 09-12. They are PNGs, 1600 px wide, filed in
`newyorkworld-scans/pages/` as `Milwaukee_Sentinel_1915_MM_DD_<page>.png`, and each row in
`printings.tsv` carries its GenealogyBank page link. Sonnet agents indexed them (number,
heading, first clue, solution label; nothing transcribed) and checked every solution box against
its puzzle per [CHAIN-BRIEF.md](CHAIN-BRIEF.md): 19 links yes, 1 no.

## What they show

**1. The Sentinel is still FUN itself in 1915.** Every page is headed "FUN." with FUN's own page
number; puzzles are "FUN'S CROSS-WORD PUZZLE". Its grids carry FUN's numbers through 1915-01-10
(No. 54, with the solution to No. 53, the Paul West puzzle of 01-03), one a week since No. 47 on
1914-11-22. The solution printed on 02-21 is a valentine, so a 02-14 puzzle.

**2. The Journal was on the same Sundays, not weeks behind.** At all thirteen Sundays held from
both papers between 1915-01-24 and 07-25, they printed the same puzzle on the same day (first
clue and shape). The only slip is No. 54, which the Journal printed a week late on 01-17 after
skipping 01-10. The record had read the Journal as three to six weeks behind the World in 1915.
That gap came from the weekly count (the World skipped weeks in 1914), not from the Journal.

**3. So 1915 has World dates.** `tools/world_dates_1915.py` gives every 1915 Sentinel and Journal
puzzle the World number of its own date (inferred, marked on each row's `match`): 33 Sentinel and
20 Journal printings. Numbers with a copy went from 158 to 188.

**4. Ten puzzles no other paper held:** 02-21 (the "Pentacle Puzzle", which FUN calls "a new kind of
cross-word puzzle": five words around a star), 02-28, 06-13, 06-20, 08-01, 08-08, 08-15, 08-22,
08-29, 09-05, plus the solution to 09-05 (on 09-12). The Journal carried no FUN puzzle from
August to mid-November 1915; the Sentinel fills six of those weeks.

## The 1915 chains now

| Chain | Span | Puzzles | Was |
|---|---|---|---|
| C3 | 1914-11-08 (No. 47) to 1915-02-07 (N) | 11 | same, now dated |
| C4 | 1915-02-21 (Pentacle) | 1 | new |
| C5 | 1915-02-28 to 04-04 | 6 | 03-07 to 04-04, floating |
| C6 | 1915-04-11 to 05-23 | 6 | same, now dated |
| C7 | 1915-06-06 to 06-13 | 2 | 06-06 alone |
| C8 | 1915-06-20 to 09-05 | 12 | 06-27 to 07-25, floating |

All are still "floating" in `chains.tsv` (the dates are inferred, not proved by a dated
solution). One run of Sentinel pages from 09-12 to 11-21 would join C8 to the chain that runs
to the 1917 solutions box, and prove the Sentinel's dates at both ends.

## Sentinel pages to look for next

In order of value (the status page's "Missing puzzles" list now names these too):

1. **1915-09-19 to 11-21** (ten Sundays): joins 1915 to 1916-17.
2. **1915-02-14** (the valentine puzzle) and the page after 02-21's Pentacle (its solution, on
   02-28): closes N / 02-21 / 02-28.
3. **1915-05-30** (and 05-09, 05-16, 05-23, 06-06): closes 05-23 / 06-06.
4. **1915-06-20's other FUN page** (the solution to 06-13's swastika-shaped puzzle), and
   **1915-04-04 / 04-11** (the Journal holds only a clip of 04-04).
5. **1915-01-17 and 01-31**: whether the World ran a puzzle on 01-17 (the Journal printed No. 54
   that day), and the U of F-U-N, which would turn its two tentative links into checked ones.
6. The clue-list continuations: 01-03 says "Continued on Next Page" (p. 61 not saved), as does
   05-02's pinwheel.
7. Back into 1914 and to December 1913: Nos. 1, 2, 4 and the solutions the 1914 intake asked for.

Not recorded as searches: the Sundays between the saved ones. Whether GenealogyBank's search
missed them or they weren't saved isn't known, so they stay unsearched rather than `no-hit`.
