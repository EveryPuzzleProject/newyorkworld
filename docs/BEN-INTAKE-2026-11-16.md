# Ben's research images, intake of 2026-11-16

Ben sent the rest of the images from his earlier research as a Google Drive export,
`The World syndicated crosswords-20261116T195426Z-1-001.zip`. Claude extracted it into a
fresh folder outside the repos, opened only the image files, and indexed the new ones
(number, heading, credit, first clue, solution label). Nothing was transcribed and no OCR
was run.

## What was in the zip

31 files, all images (8 PNG clippings, 23 JPG full pages), in one folder. No notes,
spreadsheets or URLs, so no `search` rows and no URLs were recorded.

| Group | Files | Result |
|---|---|---|
| Milwaukee Sentinel clippings, 1914-01-04 to 1914-02-01, named `Fun<n>[sol]-Milwaukee_Sentinel_<date>_<page>.png` | 8 | 5 byte-identical to the clippings filed earlier today; **3 new** |
| New Orleans States full pages, 1917-02-25 to 1917-09-23 | 20 | all byte-identical to pages already in `newyorkworld-scans/pages/` |
| Tacoma Daily Ledger full pages, 1917-08-19 to 1917-09-02 | 3 | all byte-identical to pages already held |

So: **31 images, 3 new, 28 exact duplicates (by content hash), 0 unidentified.** Ben's 1917
New Orleans and Tacoma pages were evidently the source of copies the project already had.

## Every image

Duplicates are listed under the file name they already have in the scans repo.

| File as filed | Paper | Date | What it is | World No. and how known |
|---|---|---|---|---|
| `Milwaukee_Sentinel_1914_01_04_81_key.png` (**new**; Ben's `Fun2sol-…`) | Milwaukee Sentinel | 1914-01-04 | solution only: "the solution to the New Year cross-word puzzle", with FUN'S Weekly Riddle; says another puzzle of the same kind is given today | solution to **No. 2**: last week's puzzle in a paper carrying FUN on the World's dates, and the grid matches gxd `nyw1913-12-28` square for square |
| `Milwaukee_Sentinel_1914_01_04_80_fun.png` (dup) | Milwaukee Sentinel | 1914-01-04 | puzzle, "Find the Missing Cross Words", 1-2 Used on washday | No. 3 (already recorded) |
| `Milwaukee_Sentinel_1914_01_18_83_key.png` (**new**; Ben's `Fun4sol-…`) | Milwaukee Sentinel | 1914-01-18 | solution only: "the solution to last week's cross word puzzle"; says another cross-word puzzle is on page 6 | solution to **No. 4**: last week's puzzle; its top word answers No. 4's first clue "1-2 To help" |
| `Milwaukee_Sentinel_1914_01_18_81_fun.png` (dup) | Milwaukee Sentinel | 1914-01-18 | puzzle, "FUN'S CROSS-WORD PUZZLE, NO. 5" | No. 5, printed (already recorded) |
| `Milwaukee_Sentinel_1914_01_25_67_fun.png` (dup) | Milwaukee Sentinel | 1914-01-25 | puzzle, No 6 in the grid | No. 6, printed (already recorded) |
| `Milwaukee_Sentinel_1914_01_25_68_key.png` (dup) | Milwaukee Sentinel | 1914-01-25 | solution to No. 5 | label (already recorded and linked) |
| `Milwaukee_Sentinel_1914_02_01_66_fun.png` (**new**; Ben's `Fun7-…`) | Milwaukee Sentinel | 1914-02-01 | puzzle, "FUN'S CROSS-WORD PUZZLES: Can You Solve Them?", diamond, first clue "1-2 United in Matrimony"; "Today the seventh puzzle in the series"; solution to last week's on page 15 | **No. 7**, printed ("No 7" in the shaded centre cross) |
| `Milwaukee_Sentinel_1914_02_01_67_key.png` (dup) | Milwaukee Sentinel | 1914-02-01 | solution to No. 6 | label (already recorded and linked) |
| `New_Orleans_States_1917_02_25_42.jpg` … `_1917_09_23_39.jpg` (20 dups) | New Orleans States | 1917-02-25, 03-25 (×2), 04-01, 04-15, 04-22, 05-06, 05-13, 05-20, 06-10, 06-24, 07-01, 07-15, 07-22, 08-12, 08-19, 09-02, 09-09, 09-23 (×2) | already held | already recorded |
| `The_Tacoma_Daily_Ledger_1917_08_19_38.jpg`, `_08_26_10.jpg`, `_09_02_38.jpg` (3 dups) | Tacoma Daily Ledger | 1917-08-19, 08-26, 09-02 | already held | already recorded |

Where Ben's file names and the pages agree: all three new names were right (paper, date,
viewer page, and which puzzle). The page numbers the clippings print ("page 6", "page 15")
are FUN's own section pages, not the Newspapers.com viewer pages in the file names.

## What changed in the record

- **No puzzle went from wanted to have.** No. 2 is still wanted as a page; it now has a
  **solution** (`solution_seen: milwaukee-sentinel 1914-01-04`), which agrees with the gxd
  copy taken from T Campbell's reprint of the World page, an independent check of
  `nyw1913-12-28`.
- **No. 7 gained a second copy**, and a better one in one respect: the Sentinel prints it
  with the grid's own number and no wrong heading (the Minneapolis Journal's same-day copy is
  headed "No. 5"). It is a clipping at Ben's resolution; whether it reads better than the
  Journal crop is for the OCR step to show.
- **No. 4 is now complete**: puzzle (the World clip, The Farmers Mail and Breeze of
  1914-02-14, Capper's Weekly) plus its solution (Sentinel 1914-01-18).
- Complete (puzzle and solution both held) among Nos. 1-7: **Nos. 4, 5, 6**. No. 3's
  solution would be in the Sentinel of 1914-01-11; No. 7's in the Sentinel of 1914-02-08;
  neither is saved yet.
- No `link` rows were added: none of the new solution boxes carries a printed number, and
  the puzzles they answer are not Sentinel pages we hold, so there is no label-to-label link
  to record. (No. 4's solution could be linked to the Kansas Farmer page with `kind=grid`
  after a grid check; not done here.)

## The Milwaukee Sentinel's run, as now known

- **Held:** 1914-01-04, 01-18, 01-25, 02-01 (four Sundays, each with that week's puzzle and
  the previous week's solution): puzzles Nos. 3, 5, 6, 7 and solutions to Nos. 2, 4, 5, 6.
- **Implied:** 1913-12-28 (the 01-04 box solves "last week's" New Year puzzle, No. 2) and
  1914-01-11 (the 01-18 box solves last week's, No. 4). Both issues should hold puzzles:
  No. 2 on 12-28 and No. 4 on 01-11.
- **Gaps:** 1914-01-11 not saved; nothing before 1914-01-04 saved; nothing after 1914-02-01.
- **Nos. 1-2:** not covered by a held page. The Sentinel ran FUN's crossword by 1913-12-28,
  so its 12-28 issue (No. 2, and No. 1's solution) and its 12-21 issue (No. 1) are the
  first things to look for.
- **Nos. 7-30:** only No. 7. The zip has nothing from 1914-02-08 on, so whether the Sentinel
  kept carrying FUN through July 1914, where the Journal reads badly, is still open.

## Other papers in the zip

New Orleans States (20 pages, 1917-02-25 to 1917-09-23) and Tacoma Daily Ledger (3 pages,
1917-08-19 to 09-02): all already in the scans repo and the record. Nothing new.

## Nothing surprising

No paper's own numbering, no puzzle out of the World's sequence, no unidentifiable image.
The one small finding: No. 2 was a New Year puzzle (NEW / YEAR shaded at the top of the
diamond), and the Sentinel's solution box calls it that rather than by number.

## Which source to read each of Nos. 1-30 from

| No. | Read from | Why |
|---|---|---|
| 1 | gxd `nyw1913-12-21` (Campbell's World page); Pittsburgh Press 1918-12-01 as a check | no 1913 partner page held |
| 2 | gxd `nyw1913-12-28`; check against the Sentinel 1914-01-04 solution | no page held; the solution now confirms the grid |
| 3 | Milwaukee Sentinel 1914-01-04 | only copy |
| 4 | Kansas Farmer and Mail and Breeze 1914-02-14 (full page), Sentinel 1914-01-18 for the solution | cleanest full page; now complete |
| 5, 6 | Milwaukee Sentinel | only copies, solutions held |
| 7 | Milwaukee Sentinel 1914-02-01, the Journal crop as a second read | correct heading; two copies to compare |
| 8-30 | Minneapolis Journal crops, until Sentinel pages for 1914-02-08 on turn up | only copies held |

## What to ask Ben for next

1. The Milwaukee Sentinel's FUN pages for **1913-12-21, 1913-12-28 and 1914-01-11** (Nos. 1,
   2 and 4 as puzzles, and the solutions to Nos. 1 and 3).
2. Whether the Sentinel kept carrying FUN after 1914-02-01, and if so its crossword page
   and solution box for **1914-02-08 through July 1914** (Nos. 8-30), where the Journal
   reads badly; Newspapers.com links (clipping URLs) for all his Sentinel clippings.
3. Any search notes he kept (Sundays he looked at and found nothing), so they can go in
   `searches.tsv`.
