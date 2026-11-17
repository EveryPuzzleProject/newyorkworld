# Nos. 1-33 from the Milwaukee Sentinel: sources, dates and ids, harvest plan (2026-11-16)

A plan for the review batch of the World's FUN crosswords Nos. 1-33, read from the Milwaukee
Sentinel's FUN pages instead of the Minneapolis Journal's.

**Decided (Alex, 2026-11-16):** the date table in section 2, and retiring batch c1. Both are done
in the record (this PR). Still open: URLs for the Sentinel's 1913-14 rows (section 3), and running
the harvest. Nothing has been harvested or published.

The data comes from PR #28 (`nyw/queue-sentinel`: `printings.tsv`, `links.tsv`,
`docs/SENTINEL-WANTED.md`) and scans PR #5 (the page images and `pages.tsv`). Both are still open
and are needed before the harvest.

## 1. The source map

The Sentinel carried FUN itself, on the World's own Sundays, so a Sentinel page's date is the
World date. Files are in `newyorkworld-scans/pages/`, named `Milwaukee_Sentinel_<date>_<page>.png`;
the table drops the `Milwaukee_Sentinel_` prefix. The page in brackets is FUN's own page number.
"Count date" is what the weekly count gives where it is wrong (section 2).

| No. | World date | count date | puzzle | solution |
|---|---|---|---|---|
| 1 | 1913-12-21 | | 1913_12_21_68 (FUN 14) | 1913_12_28_78 (FUN 15), printed upside down |
| 2 | 1913-12-28 | | 1913_12_28_77 (FUN 14) | 1914_01_04_81_key (Ben's clipping) |
| 3 | 1914-01-04 | | 1914_01_04_80_fun (Ben's clipping) | **none found in any paper** |
| 4 | 1914-01-11 | | **no Sentinel page**: fallbacks below | 1914_01_18_83_key (Ben's clipping) |
| 5 | 1914-01-18 | | 1914_01_18_81_fun (Ben's clipping) | 1914_01_25_68_key (Ben's clipping) |
| 6 | 1914-01-25 | | 1914_01_25_67_fun (Ben's clipping) | 1914_02_01_67_key (Ben's clipping) |
| 7 | 1914-02-01 | | 1914_02_01_66_fun (Ben's clipping) | 1914_02_08_82 (FUN 15) |
| 8 | 1914-02-08 | | 1914_02_08_80 (FUN 13) | 1914_02_15_84 (FUN 15) |
| 9 | 1914-02-15 | | 1914_02_15_83 (FUN 14) | 1914_02_22_83 (FUN 15) |
| 10 | 1914-02-22 | | 1914_02_22_80 (FUN 12) | 1914_03_01_85 (FUN 15) |
| 11 | 1914-03-01 | | 1914_03_01_82 (FUN 12) | 1914_03_08_85 (FUN 15) |
| 12 | 1914-03-08 | | 1914_03_08_82 (FUN 12) | 1914_03_15_86 (FUN 15) |
| 13 | 1914-03-15 | | 1914_03_15_85 (FUN 14) | 1914_03_22_85 (FUN 15) |
| 14 | 1914-03-22 | | 1914_03_22_84 (FUN 14) | 1914_03_29_87 (FUN 15) |
| 15 | 1914-03-29 | | 1914_03_29_86 (FUN 14) | 1914_04_05_90 (FUN 15) |
| 16 | 1914-04-05 | | 1914_04_05_89 (FUN 14) | 1914_04_12_89 (FUN 15) |
| 17 | 1914-04-12 | | 1914_04_12_88 (FUN 14) | 1914_04_19_95 (FUN 15) |
| 18 | 1914-04-19 | | 1914_04_19_94 (FUN 14) | 1914_04_26_91 (FUN 15) |
| 19 | 1914-04-26 | | 1914_04_26_90 (FUN 14) | 1914_05_03_97 (FUN 15) |
| 20 | 1914-05-03 | | 1914_05_03_95 (FUN 13) | 1914_05_10_90 |
| 21 | 1914-05-10 | | 1914_05_10_89 (FUN 14) | 1914_05_17_89 (FUN 15), a solutions-only Sunday |
| 22 | 1914-05-31 | 05-17 | 1914_05_31_90 (FUN 15) | 1914_06_07_85 (FUN 15), a solutions-only Sunday |
| 23 | 1914-06-14 | 05-24 | 1914_06_14_87 (FUN 13) | 1914_06_21_86 (FUN 14) |
| 24 | 1914-06-21 | 05-31 | 1914_06_21_87 (FUN 15) | 1914_06_28_74 (FUN 4) |
| 25 | 1914-06-28 | 06-07 | 1914_06_28_84 (FUN 14) | 1914_07_05_81 (FUN 15) |
| 26 | 1914-07-05 | 06-14 | 1914_07_05_81 (FUN 15) | 1914_07_12_80 (FUN 14) |
| 27 | 1914-07-12 | 06-21 | 1914_07_12_79 (FUN 13) | 1914_07_19_79 (FUN 15) |
| 28 | 1914-07-19 | 06-28 | 1914_07_19_79 (FUN 15) | 1914_07_26_76 (FUN 10) |
| 29 | 1914-07-26 | 07-05 | 1914_07_26_81 (FUN 15) | 1914_08_02_68 (FUN 14) |
| 30 | 1914-08-02 | 07-12 | 1914_08_02_69 (FUN 15) | 1914_08_09_75 |
| 31 | 1914-08-09 | 07-19 | 1914_08_09_83 (FUN 15) | 1914_08_16_82 (FUN 15) |
| 32 | 1914-08-16 | 07-26 | 1914_08_16_82 (FUN 15) | 1914_08_23_76 (FUN 7) |
| 33 | 1914-08-23 | 08-02 | 1914_08_23_85 (FUN 15) | 1914_08_30_84 (FUN 4) |

That makes 32 puzzle pages and 32 solution pages from the Sentinel, on 61 files.

**Pages with two items.** 1914_07_05_81 has No. 26 and No. 25's solution; 1914_07_19_79 has
No. 28 and No. 27's solution; 1914_08_16_82 has No. 32 and No. 31's solution. 1914_05_31_90 has
No. 22 and a solutions box for the Mexico map puzzle, which is not a crossword.

**Facing pages of one issue.** 1913-12-28 pp. 77/78 (No. 2, No. 1's solution); 1914-01-04
pp. 80/81 (No. 3, No. 2's solution); 1914-02-01 pp. 66/67 (No. 7, No. 6's solution); and from
02-08 on, nearly every Sunday has the puzzle and last week's solution two or three pages apart.
`pages.tsv` should list each issue's pages in printed order (it does), so the harvest sees them as
neighbouring leaves.

**Fallbacks** (the Sentinel lacks only these two):

- **No. 4's puzzle.** Read `pages/Kansas_Farmer_and_Mail_and_Breeze_1914_02_14_16.jpg` (Farmers
  Mail and Breeze, 1914-02-14 p. 16, the full page Alex saved; the record calls it "the page to
  read for No. 4"). Check the reading against Campbell's image of the World's own page
  (`other/New_York_World_1914_01_11_FUN_No4_Campbell.webp`) and Capper's Weekly 1914-04-18. Its
  solution is the Sentinel's 01-18 box. The xd keeps the World's date, 1914-01-11.
- **No. 3's solution.** No paper has it: the Sentinel's 1914-01-11 page was searched and not
  found, and no other partner copy of January 1914 is known. No. 3 goes to review **without a
  key**, read from the puzzle alone. The record already says it needs the World's own FUN
  section (Shortz, NYPL microfilm, Campbell).

**Nos. 1 and 2** are in gxd (`nyworld/1913/nyw1913-12-21.xd`, `nyw1913-12-28.xd`, from Campbell's
reprint of the World page). The Sentinel copies are read only to check those: differences are
listed for Alex, nothing replaces them. One is already known: gxd's No. 1 clue list starts at 2-3,
the Sentinel's at 4-5.

**Nos. 11 and 12** are already shipped to this repo's `xd/` from the Journal (not yet in gxd). They
are in the same position as Nos. 1 and 2: the Sentinel reading checks them, and a difference
becomes a correction through the ship records, not a new file.

**Gaps in the links** (`links.tsv`, PR #28): No. 27's puzzle → solution (1914_07_12_79 →
1914_07_19_79) is in `printings.tsv` but has no row in `links.tsv`. No. 4's Kansas Farmer page has
no link to its 01-18 solution. Both should be added before the harvest pins keys from the links.

## 2. Dates and ids

### What's wrong

`tools/record.py` dates every number by the weekly count (`sunday_of(n)` = 1913-12-21 + n−1
weeks). That is right to No. 21 and wrong after it. FUN ran no new crossword on 1914-05-17 (only
No. 21's solution), 05-24 (the Mexico map puzzle) or 06-07 (only No. 22's solution), and it never
used No. 34. Everything else flows from that function: `printings.tsv` `sunday_inferred` and
`lag_weeks`, `status.tsv`, `tools/ocr_fixes.py` (which re-dates the Journal's issues to the count
date in `fixes/fixes.toml`), and from there the harvest's ids. That is why batch `nyw-1914-c1`
has No. 22 as `nyw1914-05-17`, and why the record shows the Sentinel and the Journal running
"2-3 weeks late" when both ran on the World's day.

### World date = the Sentinel's date (decided; done)

`sunday_of(n)` now gives the dates the Sentinel prints:

| Nos. | World date | how it differs from the count |
|---|---|---|
| 1-21 | 1913-12-21 … 1914-05-10 | the same |
| 22 | 1914-05-31 | +2 weeks |
| 23-33 | 1914-06-14 … 08-23 | +3 weeks |
| 34 | none: never used | |
| 35-54 | 1914-08-30 … 1915-01-10 | +2 weeks (the Sentinel prints Nos. 47-54 week by week, No. 54 on 1915-01-10) |
| 55, 56 | none: the count's numbers for 1915-01-03 and 01-10, which carry printed Nos. 53 and 54 | |
| 57 on | the count, as now | `world_dates_1915.py` already numbers 1915 by date |

This reaches past No. 33 (to No. 54), because it is the same fault and one function. After it:

- `status.tsv` dates Nos. 22-54 correctly, and the lags in `printings.tsv` for the Sentinel and
  the Journal in 1914 become 0.
- `status.tsv` notes 1914-05-17, 05-24 and 06-07 as Sundays with no new crossword.
- `tools/ocr_fixes.py` stops re-dating the 1914 Sentinel and Journal issues, so a puzzle's
  harvest id is its own page's date (`nyw1914-05-31-L000` for No. 22).
- xdids are `nyw<World date>`, as gxd's `nyw1913-12-21`: No. 22 is `nyw1914-05-31`, No. 33
  `nyw1914-08-23`.

Where one World Sunday has more than one grid (the Journal's registry has two ids at Nos. 22, 23
and 24 and three at No. 29, the five-in-one; No. 13 is printed as a two-in-one), `assign-ids`
gives the second `b`, and the gxd export maps it to gxd's `a` (blitz `design/judge-postmortem.md`).
Whether a two-in-one is one xd or two is for Alex at review, puzzle by puzzle.

### Batch `nyw-1914-c1` is retired (decided; done)

c1 is 22 puzzles from the Journal: 2 shipped (Nos. 11, 12), 20 held (17 needs-work, 1 each
edits-unapplied, proof-stale, incomplete). Its ids for Nos. 22-30 use count dates. Reusing it
alongside a Sentinel batch is not safe, because the same names would mean different things:

- **Corrections are keyed by pid.** `fixes/corrections.jsonl` has 28 corrections for
  `nyw1914-06-21-L001`, which in c1 is No. 27. In a Sentinel harvest, `nyw1914-06-21-L001` is
  No. 24 (06-21 p. 87, after p. 86). Those 28 edits would land on the wrong puzzle. Seven more
  pids (02-22, 03-01, 03-08, 03-15, 03-29, 04-26, 05-03 `-L000`) are the same name and the same
  number in both, but the edits are keyed to the Journal's reading (clue slots, key squares) and
  can mis-apply to a different reading.
- **Review-site packets are stored by pid** (`nyw/<pid>/`). Publishing a Sentinel batch would
  overwrite c1's packets for those eight pids under c1's batch page.
- **`pipeline/ids.tsv`** holds 27 registry ids for the Journal's pages, with count dates in the
  ids (`nyw-1914-05-17-1` is No. 22). Registry ids never change, so the Sentinel's No. 24 on
  1914-06-21 would get the next free number after c1's `nyw-1914-06-21-*` (No. 27).

Proposal:

1. **Retire c1.** Done: its `decisions.jsonl`, `corrections.jsonl` and `tool-notes.jsonl` rows,
   its `pipeline/ids.tsv` rows and its assembly packets are in `fixes/retired/nyw-1914-c1/`
   (README there). The Journal's hand-fitted grids stay in `fixes/fixes.toml`: they are keyed by the
   Journal's pages and touch nothing else. `pipeline/ship/nyw-1914-c1.json` stays as the record.
2. **Keep Nos. 11 and 12 as shipped.** Their `xd/`, `provenance.jsonl` and `fixes/xdids.tsv` rows
   stay. The Sentinel reading is compared against them. `fixes/xdids.tsv` pins `nyw1914-03-01` and
   `03-08` to the Journal's pages; a pinned id follows other scans of the same issue only, and the
   Sentinel is another issue key, so `assign-ids` would give its copies `nyw1914-03-01b`. After the
   harvest, pin the Sentinel's pages to the same two ids (or keep those two out of `assign-ids`).
3. **Carry over the reviewers' work as evidence, not edits.** For each of Nos. 7-30, the proof
   reviewer gets c1's corrections and the owner's notes for that number (`by-number.tsv` in the
   retired folder maps each c1 id to its number) as a list of known trouble spots to check. Nothing
   from c1 applies automatically.
4. **Take c1 off the review site** before the new batch is published (needs Alex's say-so: the
   site is public).

## 3. Harvest and review plan

### Before the harvest

1. Merge PR #28 and scans PR #5 (Alex).
2. In the record (this repo; done in this PR): the date change in section 2, rebuilt, the two
   missing links, `tools/ocr_fixes.py` re-run (the 1914 Journal issues are no longer re-dated), c1
   retired.
3. In `newyorkworld-scans/pages.tsv` (the scans PR; `pages.tsv` is written by `tools/record.py
   rebuild`, so the changes are in `sync_pages_tsv`, here, and the scans PR is its output):
   - **Fix `crop_of` on the January clippings** (done). Today 01-18's and 01-25's solution clippings are
     marked as crops of the puzzle clippings, and 02-01's puzzle clipping as a crop of its solution
     clipping. The harvest reads a page that has crops only through its crops, so as it stands it
     would never read Nos. 5 and 6 or No. 6's solution. Ben's clippings are separate pages (the
     puzzle and solution are on different printed pages), so: either clear `crop_of` and list the
     clippings as pages, or add the full pages (01-04 pp. 80/81, 01-18 pp. 81/83, 01-25 pp. 67/68,
     already in `pages/`) as rows and make each clipping a crop of its own page. The second is the
     documented form, and it gives the proof page the whole page to look at. The clippings are
     sharper than the full pages (about 1300 px across one column against 1600 for the whole page),
     so they stay what is read. Done the second way: the six full pages are listed, each clipping is a
     crop of its own page, and 02-01's two clippings (no full page held) stand as pages.
   - **Add an `answers` column** from `links.tsv` (done, for every paper; 77 rows, 32 of them the
     Sentinel's 1913-14 solutions): each solution row names the puzzle row it
     answers. That pins all 32 keys rather than leaving the harvest to match black squares across
     weeks.
   - **URLs.** None of the 1913-14 Sentinel rows has a `url` (the 1915 GenealogyBank rows do).
     Without one a page is named `scan:<issue>/<leaf>` on the proof page and in the xd's
     provenance, which isn't a link. **Alex:** add the Newspapers.com image links, or ship with
     scan names.
4. **Resolution.** The Sentinel pages are 1600 px wide, against the Journal's 2650, but FUN's
   page is tabloid-sized: on 06-14 p. 87 the clue type is clean even at half size. Run without
   `[ocr] tiles` first and compare on a few pages.

### The harvest

In an `xword-ocr` worktree on its own branch, a new harvest folder, so c1's state stays as it was:

```
uv run xword-ocr harvest --folder ../newyorkworld-scans --pubid nyw \
  --fixes ../newyorkworld/fixes/fixes.toml --out harvests/nyw-s1 \
  --only milwaukee-sentinel-1913-12-21 milwaukee-sentinel-1913-12-28 … milwaukee-sentinel-1914-08-30 \
         kansas-farmer-and-mail-and-breeze-1914-02-14
```

That is the Sentinel's 35 issues from 1913-12-21 to 1914-08-30 (08-30 for No. 33's solution only;
its No. 35 page is outside this batch) and the Kansas Farmer page for No. 4. Then the same stages
as c1 (`docs/OCR-C1.md`): `stage adopt`, relink, the text step and the AI proof review (Sonnet;
`editorial.md`), triage. Fixes that carry over unchanged: `[ocr] linked_ends`, `[assembly]
keys_next_issue` (still right: the key is in the next issue, and pinned by `answers` anyway). The
`[publication] untitled` rule names chain C1 and the Journal's column headings; the Sentinel prints
its headings ("FUN'S CROSS-WORD PUZZLE No 23"), so that rule needs another look before triage.
Hand-fitted grids are drawn again from the Sentinel's pages where the detector misses, as in c1.

Expected: 33 puzzles (Nos. 1-33), 32 with a pinned key (all but No. 3, and No. 4's key is from a
different paper than its puzzle). Nos. 1, 2, 11 and 12 are check-only.

### Review

- Batch name `nyw-1914-s1`. Packets built, **not** published until Alex says so.
- Owner review first (Alex), as for c1. The c1 trouble-spot lists go with each puzzle (section 2).
- The ship check runs against the World dates and xdids above. Nothing ships with a count date,
  and nothing goes to gxd without Alex's say-so. gxd branches go to Alex's fork.

## 4. The run (2026-11-16)

PRs #28, #29 and scans #5, #6 merged (Alex). The run is `blitz-work/runs/nyw-s1` (outside the repos,
as xword-ocr requires), read from its own `source/pages.tsv`: the 69 rows of `pages.tsv` for the
batch's 36 issues, with absolute paths. xword-ocr branch `claude/nyw-s1` (no code changes).

**Harvest.** 30 of the 33 puzzles assemble, plus No. 35 from the 08-30 page (left out of the
batch). Eight pages needed a grid hint (`fixes/fixes.toml`, "The Milwaukee Sentinel's pages"): the
World prints its end-square numbers large, the detector reads them as letters and takes the puzzle
for a solution grid; `puzzle = true` on the detector's own corners fixed Nos. 3, 4, 5 and 27, and
No. 23's X of bands needed its corners widened to 28 x 21. Not assembled: No. 2, No. 28 (letters
given in the grid, no clue list) and No. 31 (the geography puzzle).

**Alex's rule for this batch (2026-11-16):** use what the OCR library gets, and don't extend it for
the early puzzles' odd designs. Where it can't, read the scan directly, and record the reading as
made by hand from the scan. So Nos. 28 and 31 are read from the page (xd files in the run's
`hand-read/`, with a doubts list), and No. 2 is compared with gxd's copy. The same goes for any
odd design the text step and review can't bring right (likely Nos. 23, 27, 29 and 30).

**Text step.** 30 puzzles in 8 batches of 4 (Sonnet agents, as c1), run `textstep/s1`. It could not
bring them right: 29 of 30 asked for a clue list to be read again, and the keys came out garbled or
unread on most (only Nos. 11-13 got usable key fixes).

**Read from the scans instead (Alex, 2026-11-16).** All 33 were read by hand from the page images
(Claude agents, Opus), with every clue and printed line tied to its box on the page: the result and
its open decisions are in [`hand-read/`](../hand-read/README.md); the review packets (each scan with
its boxes beside the text) are in the scans repo, `packets/nyw-1914-s1/`. Nothing is shipped or
published.

## Still open for Alex

1. URLs for the 1913-14 Sentinel rows, or go without.
2. Taking c1 off the review site (it is public).
3. Go-ahead to run the harvest as `nyw-s1` once PRs #28, scans #5 and these two are merged.
