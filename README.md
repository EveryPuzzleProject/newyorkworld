# The New York World's FUN crosswords, 1913–1917

The first crossword ran in the New York World's Sunday supplement, FUN, on December 21,
1913, and a new one every Sunday after. The World's own FUN pages survive badly, but
other papers reprinted the section, crossword and all, almost from the start. This is the
Every Puzzle Project's record of the World's series, one row per Sunday, built from those
reprints: the Minneapolis Journal from February 1, 1914, and, where the Journal stops
carrying FUN, the Pittsburgh Press (from 1916-06-11) or the Tacoma Daily Ledger.

**Status page: https://everypuzzleproject.github.io/newyorkworld/** (every Sunday as
clipped / to clip / missing, mismatches flagged, and the next batch to clip).

What the run should settle: which World puzzle each Sunday's is; whether the World ever
skipped, repeated or renumbered; when the grid numbers stop; and which World puzzle the
Boston Globe printed on 1917-02-25 (and Tacoma on 1917-03-11, Pittsburgh later), matched
by number while there is one and by clues after that.

## The dating rule

The World printed its series number in the grid, in a shaded cross at the center of a
diamond template: No. 7 on 1914-02-01, No. 8 on 1914-02-08, rising one a week (seen in
the Minneapolis Journal). That fits one puzzle every Sunday from No. 1 on 1913-12-21:

> World No. *n* is expected on 1913-12-21 plus *n*−1 weeks, and the Journal ran each
> puzzle on the World's own date.

Every World date derived this way is an **inference** from that count, and is shown as
one (marked * on the status page). What a page shows goes in `world_no_printed`. A copy's
own date is a printing date, days to weeks after the World's; the difference is its lag.
Within one paper's run, a number that repeats or jumps against the previous numbered copy
is flagged. That is a skip, a repeat or a misprint by the World, or a week the paper
dropped, which is exactly what this run is looking for. The Journal's own heading on 1914-02-01 said "No. 5"; it
was wrong and dropped the next week. The grid number is the one that counts.

A page missing from Newspapers.com is recorded as `missing-from-scans`, never as a skip
by the World. A Sunday when the paper ran no FUN puzzle is `not-carried`.

## What's here

| File | What it is |
|---|---|
| `status.tsv` | One row per World puzzle, No. 1 to No. 211 (1913-12-21 to 1917-12-30), with its inferred date, whether we have a copy, and from where. Derived by `tools/record.py rebuild`; only `notes` is kept by hand. |
| `printings.tsv` | One row per copy we have a page for: paper, date, page, the number printed in the grid, heading, credit, copyright line, first-clue key, which solution the page carries, the Newspapers.com link, and the World number it is matched to (and how). Hand-indexed from the image. |
| `searches.tsv` | One row per paper and Sunday looked for: queued (which batch), found, no-hit, not-carried, missing-from-scans. The coverage log and the queue. |
| `links.tsv` | One row per checked link: which page's solution answers which page's puzzle, across papers, with the kind of evidence and who checked. |
| `chains.tsv`, `chain_breaks.tsv`, `chain_pages.tsv`, `reruns.tsv` | The unbroken chains of linked puzzles, the breaks between them, which chain each page sits in, and same-first-clue candidates for reprints. Derived by `rebuild`; see [docs/CHAINS.md](docs/CHAINS.md). |
| `papers.tsv` | The papers whose copies we use, with what each one's copy looks like. |
| `series.tsv` | The World's series and each paper's run, with dates and status. |
| `tools/record.py` | `new`, `add`, `link`, `search`, `queue`, `rebuild`, `show`: the only way the tables change. |
| `tools/render.py` | Builds the status page (`site/index.html`) from the tables; runs on every push. |

The Boston Globe printed each puzzle on the World's own date in 1917 (the World Magazine solutions box Tacoma reprinted on 1917-07-22 dates the chain), and not after: by 1919 it was out of step and by 1920 months behind (docs/CAMPBELL-CROSSCHECK.md). Its 1918 to 1924 pages are good copies without World numbers.

A grid printed again on a later Sunday with new clues counts as a second puzzle (the paper ran it as that week's puzzle); the notes on both rows say it is a rerun of the grid (decided 2026-10-30, Globe 1918-06-23 and 07-07).

Printings and puzzles are kept apart: a Boston Globe date is a printing of a World puzzle,
not a Globe puzzle. A printing with a number in the grid is tied to that World number; one
without is tied by its first clue and grid shape against another copy, and `match` says how.
Each printing's lag (its date minus the inferred World date) is computed, so each paper's
delay behind the World shows on the status page.

The Globe's own run (which Sundays exist, the Sundays it skipped, its Saturday and Wednesday series from 1923 and 1924) is accounted for in the [bostonglobe repo](https://github.com/EveryPuzzleProject/bostonglobe) and its [status page](https://everypuzzleproject.github.io/bostonglobe/); its page images are in `bostonglobe-scans/print/`. Here the `boston-globe*` rows in `printings.tsv` stay as the identity link: which Globe printing is which World puzzle (the 1917 anchor rests on them).

## The daily loop

Newspapers.com allows about 30 high-resolution downloads a day, so the run takes a week or
more. Each day:

1. **Find** the Sundays listed under "Next batch to find" on the status page. Download each
   page as *Entire page, JPG* into `../newyorkworld-scans/pages/` (the private twin repo),
   keeping the name Newspapers.com gives it: `The_Minneapolis_Journal_1914_02_15_34.jpg`.
   If several papers carry the puzzle that day, every distinct paper's copy is welcome.
2. **Intake.** `python tools/record.py new` lists the saved pages not yet recorded. Each is
   looked at only to index it: the grid's printed number, heading, credit, copyright line,
   the first clue as a matching key, and which solution the page carries. Clues and answers
   are not transcribed here; puzzle content comes later from the OCR pipeline (xword-ocr /
   blitz), so nothing typed by hand gets in silently. Then
   `python tools/record.py add <file> world_no_printed=9 heading="..." ...`.
   A Sunday with no page: `python tools/record.py search <paper> <date> no-hit` (or
   `not-carried`, `missing-from-scans`), with a note.
3. **Rebuild and commit.** `python tools/record.py rebuild` recomputes status.tsv, the flags
   and the scans repo's `pages.tsv`; `python tools/render.py` rebuilds the page. Commit both
   repos, naming the dates covered.
4. **Queue** the next day: `python tools/record.py queue --n 30` (sequential Minneapolis
   Journal Sundays from 1914-02-15 that have neither a page nor a search result), or explicit
   dates.

Batch 1 was a spot check, about one Sunday every two months across 1914–1917, plus the
Sundays around the Globe's 1917-02-25 puzzle, to map where the Journal carries FUN, where
the grid numbers stop and where the record breaks, before the sequential fill.

## How you can help

If you have access to Newspapers.com or another scan of the Minneapolis Journal, the
Pittsburgh Press, the Tacoma Daily Ledger or, best of all, the World's own FUN section
(especially December 1913 to January 1914, World Nos. 1–6), see the status page for the
Sundays wanted and open an issue with the date and a clipping link. Please don't upload
page images: issues are public. What's known about the World's puzzles and its partner
papers, with sources, is in the catalog:
[new-york-world.md](https://github.com/EveryPuzzleProject/catalog/blob/main/publications/new-york-world.md)
and [first-runs.md](https://github.com/EveryPuzzleProject/catalog/blob/main/first-runs.md).

## Images

Page images from Newspapers.com never go in this repo. They live in the private twin
`newyorkworld-scans` (`pages/`, with a `pages.tsv` in xword-ocr's folder-source format so the
OCR pipeline can harvest it directly); `status.tsv` records each page's file name and
Newspapers.com URL. Whether 1914–1917 images are published anywhere is a separate decision,
not taken here.
