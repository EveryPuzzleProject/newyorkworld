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

## Addendum: the Sentinel of 1914-08-09 (Alex, looking for No. 34)

Alex saved the Sentinel's FUN page of 1914-08-09 (`Milwaukee_Sentinel_1914_08_09_83.png`,
FUN p. 15), the World's date for No. 34. It has no number and is not a new puzzle. It is
"SOME GEOGRAPHY!", the AMERICA puzzle contributed by E. W. Fuller of New York, with the
same grid and first clue ("1 to 2 A city in Persia") as the Minneapolis Journal's page of
the **same day**. The record already places that puzzle at No. 31, by its position between
the Journal's numbered Nos. 30 and 32, so the Sentinel copy is recorded as a second copy of
No. 31, and No. 34 stays wanted.

That leaves one question open. The Sentinel was on the World's dates in January 1914. If it
still was in August, the AMERICA puzzle is No. 34. On that reading the Journal printed it on
its World date and dropped No. 31, and that would explain the Journal's jump from No. 33 to
No. 35 (it had already run No. 34). If the Sentinel had drifted three weeks behind like the
Journal, both papers were following the same syndicated schedule and the AMERICA puzzle is
No. 31. One numbered Sentinel page decides it: **1914-08-02** (No. 33 if on date, No. 30 if
behind) or **1914-08-16** (No. 35 or No. 32; its solution box should also be the AMERICA
puzzle's).

## Addendum: the Sentinel of November and December 1914 (Alex)

Alex saved four more Sentinel FUN pages. Each has the same puzzle as the Minneapolis
Journal's page of the same day:

| File | Date | Puzzle | Number | Solution box |
|---|---|---|---|---|
| `Milwaukee_Sentinel_1914_11_22_77.png` | 1914-11-22 | FUN'S THANKSGIVING CROSS-WORD PUZZLE, 2-3 A rodent | **No 47, printed** | last week's: No. 46 (no held copy) |
| `Milwaukee_Sentinel_1914_11_29_79.png` | 1914-11-29 | FUN'S CROSS-WORD PUZZLE, double diamond by B. A. Havens, 1-10 To fall behind | **No 48, printed** | No. 47 (linked, `kind=grid`) |
| `Milwaukee_Sentinel_1914_12_20_66.png` | 1914-12-20 | FUN'S CHRISTMAS CROSS-WORD PUZZLE, half-filled, no clues | none; No. 51 by sequence | No. 50 |
| `Milwaukee_Sentinel_1914_12_27_59.png` | 1914-12-27 | FUN'S NEW YEAR CROSS-WORD PUZZLE, 2-3 Away from | none; No. 52 by sequence | No. 51 (linked, `kind=grid`) |

**The Journal's late-1914 numbers were one too low, and are corrected.** The record had
numbered the Journal's unnumbered puzzles from 1914-11-22 by sequence, assuming the dropped
week came later: Thanksgiving 46, then 47 to 52. The Sentinel prints 47 and 48 on the same
puzzles. The Journal's seven rows from 1914-11-22 to 1915-01-03 are renumbered 47 to 53,
and each says why in `match`. The Journal never ran **No. 46**: its 11-15 page has only
No. 45's solution. No. 46 is now wanted. Only its solution is held, in the Sentinel box of
11-22. **No. 53** (Journal 1915-01-03) goes from wanted to have, and the Journal's printed
No. 54 on 01-17 now follows without a gap. The Journal's flag "No. 45 to No. 54 in 10
weeks: -1" still stands, and it is correct: the Journal did drop one puzzle, No. 46.

**The World's own dates.** The holiday puzzles were written for the day they appeared:
Thanksgiving on 11-22 (Thanksgiving was 11-26), Christmas on 12-20, and New Year on 12-27,
whose clues say New Year's Day "arrives next Friday" and give "Jan. 1, 1915". So in late
1914 both papers ran FUN's puzzles on FUN's own Sundays, and FUN's numbering ran **two weeks
behind the README's weekly count** (No. 47 on 11-22, where the count puts it on 11-08). The
"lag 2w" that `status.tsv` now shows for both papers is the count's error, not delay by the
papers. The README's dating rule ("No. *n* on 1913-12-21 plus *n*−1 weeks") is therefore
wrong by late 1914. This intake does not change it; that is for Alex to decide.

**What this means for August and No. 34.** If the papers were also on FUN's dates in
August, as they were in January and in November and December, then the AMERICA puzzle of
1914-08-09 is FUN's puzzle of that day. Its place in the sequence is No. 31 (between the
Journal's printed 30 and 32), the same as before. The jump from No. 33 (08-23) to No. 35
(08-30) would then be **the World skipping the number 34**, not the Journal dropping a
week. That fits the offset: three weeks behind the count in August and two weeks behind in
November. The Sentinel of **1914-08-30** (No. 35 with "Solution to No. 33"?) or of
**08-23** would show whether the Sentinel also goes from 33 to 35. If it does, No. 34 never
existed. The offset grew from zero (No. 7 on 1914-02-01) to three by August, mostly in
May–June, where the Journal's flags for Nos. 22 and 23 sit. Sentinel pages for
**1914-05-17, 05-24 and 06-07** would show whether FUN skipped those Sundays.

## Addendum: the Sentinel of May and June 1914 (Alex, by search; pages not yet saved)

Alex reports finding the Sentinel's No. 20 on 1914-05-03 and No. 21 on 05-10, and on 06-07
"the solution to cross-word puzzle No. 22, given in last week's Fun" (an hourglass grid, the
same shape as the Journal's No. 22). His searches found nothing on 05-17, 05-24 and 05-31.
The 06-07 page means No. 22 was in the Sentinel's FUN of 05-31, so that no-hit is a search
miss. The three no-hits are recorded in `searches.tsv`; the found pages wait until they are
saved.

The Sentinel's run matches the Journal's week for week: No. 21 on 05-10, only its solution on
05-17, a map-of-Mexico game and no crossword on 05-24, No. 22 on 05-31, only No. 22's
solution on 06-07, and No. 23 on 06-14. Two papers that copy the same weeks in step point to
**FUN itself running no new crossword on three Sundays: 1914-05-17, 05-24 and 06-07**, rather
than to delay by the papers. That accounts for the whole three-week offset from the weekly
count by June. With the World's 33-to-35 jump in August (offset three to two), and the
November and December holiday puzzles on their own dates, a consistent account of 1914 is:

- Nos. 1-21: the count holds (No. *n* on 1913-12-21 plus *n*−1 weeks).
- FUN runs no new crossword on 05-17, 05-24 and 06-07.
- Nos. 22-33: the count plus three weeks (No. 22 on 05-31, No. 33 on 08-23).
- No. 34 is never used.
- Nos. 35-54 and on: the count plus two weeks (No. 35 on 08-30, No. 47 on 11-22, No. 52 on 12-27).

On this account the Minneapolis Journal ran FUN on its own dates throughout 1914. Its "lag"
on the status page is the count's error, and the record's flags at Nos. 22, 23 and 35 are
the World's own skips. The README's dating rule and `status.tsv`'s inferred dates are left
as they are for Alex to decide. Still to check: whether the Sentinel also goes from No. 33
to No. 35 (1914-08-23 and 08-30), and No. 46 (Sentinel 1914-11-15).

## Addendum: the Sentinel of 1914-08-23 and 08-30 (Alex): no No. 34

| File | Date | Puzzle |
|---|---|---|
| `Milwaukee_Sentinel_1914_08_23_85.png` | 1914-08-23 | **No. 33, printed**, by Harold Smith of Waterford, N. Y.; 1-2 Part of a fish |
| `Milwaukee_Sentinel_1914_08_30_85.png` | 1914-08-30 | **No. 35, printed**, by S. Worcester of Biddle street, Milwaukee; 1-2 A dress of state |

Both are the Journal's puzzles of the same days. The Sentinel goes from No. 33 to No. 35 in
one week, as the Journal does, whose 08-30 page labels its solution "No 33". Two papers
carrying FUN on the same Sundays skip the same number. So the World's FUN never numbered
a puzzle 34, and the 33-to-35 jump is the World's. `status.tsv` keeps No. 34 as
wanted, because only the tool can change that, with a note that it was probably never used.
This settles the August question in the first addendum: the AMERICA puzzle of 08-09 is
No. 31 on FUN's own date, not No. 34. The account of 1914 set out above (the count holds to
No. 21, three weeks behind from No. 22, two weeks behind from No. 35) now has printed
evidence at each step except the three weeks without a crossword in May and June, and for
those both papers agree.

Neither page has a solution box, so the Sentinel's solutions for this stretch are on other
pages of FUN.

## Addendum: the Sentinel of 1914-05-03 (Alex)

| File | Date | What it is |
|---|---|---|
| `Milwaukee_Sentinel_1914_05_03_95.png` | 1914-05-03, FUN p. 13 | **No. 20, printed**, "the twentieth in FUN'S series", by Miss Elizabeth M. Butzinger of New York; X-shaped; 1-2 A young hawk |
| `Milwaukee_Sentinel_1914_05_03_97.png` | 1914-05-03, FUN p. 15 | solution only: "SOLUTION TO No 19", with the Tango puzzle's solution |

These are the Journal's puzzle and solution of the same day. The Sentinel's No. 20 is the
better copy to read: the Journal's page shows the clue list only from 63-64, and this one
has it in full from 1-2. No. 19's solution is linked to the Journal's No. 19 (04-26) by its
printed label. Alex also reported the Sentinel's No. 21 on 05-10, but that page has not been
saved yet.

## Addendum: the Sentinel of 1914-05-10 and 06-07 (Alex)

| File | Date | What it is |
|---|---|---|
| `Milwaukee_Sentinel_1914_05_10_89.png` | 1914-05-10, FUN p. 14 | **No. 21, printed**, Miss Butzinger's second puzzle; 1-2 A conveyance |
| `Milwaukee_Sentinel_1914_05_10_90.png` | 1914-05-10 | solution only: "SOLUTION TO No 20" (linked to No. 20 of 05-03 by label) |
| `Milwaukee_Sentinel_1914_06_07_85.png` | 1914-06-07, FUN p. 15 | solution only: "the solution to cross-word puzzle No. 22, given in last week's Fun" (linked to the Journal's No. 22 of 05-31 by label); no new crossword |

Every Sentinel page from May 1914 matches the Journal's of the same day. The Sentinel now
holds both puzzle and solution for No. 20, and the solutions to Nos. 19 and 22. Its 06-07
page confirms that No. 22 ran on 05-31 and that 06-07 had no new crossword.
