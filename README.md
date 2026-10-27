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

Every `world_no_expected` and every World date derived this way is an **inference**
from that count, and is shown as one (marked * on the status page). What the clipping
shows goes in `world_no_printed`. The two are compared on every write: a printed number
that differs from the expected one, repeats, or jumps against the previous numbered
clipping is flagged. That is a skip, a repeat or a misprint by the World, which is exactly
what this run is looking for. The Journal's own heading on 1914-02-01 said "No. 5"; it
was wrong and dropped the next week. The grid number is the one that counts.

A page missing from Newspapers.com is recorded as `missing-from-scans`, never as a skip
by the World. A Sunday when the paper ran no FUN puzzle is `not-carried`.

## What's here

| File | What it is |
|---|---|
| `status.tsv` | One row per Sunday, 1913-12-21 to 1917-12-30 (211 rows). Kept by `tools/record.py`. |
| `series.tsv` | The World's series and each paper whose copies we use, with dates and status. |
| `tools/record.py` | `init`, `new`, `set`, `queue`, `check`, `show`: the only way rows change. |
| `tools/render.py` | Builds the status page (`site/index.html`) from the TSVs; runs on every push. |
| `clippings/` | Page images saved from Newspapers.com. **Not in git** (see below). |

`status.tsv` columns: `sunday` (the World's date, inferred), `world_no_expected`,
`world_no_printed`, `source` (which paper's copy: `minneapolis-journal`,
`pittsburgh-press`, `tacoma-daily-ledger`), `copy_date` and `copy_page` (that paper's
issue and page, when they differ from the Sunday), `heading`, `clipping_url`, `file`
(the local page image), `solution_date`, `solution_page`, `solution_clipping_url`,
`solution_file`, `status`, `batch` (which day's batch it belongs to), `flag`
(computed), `notes`.

States: `to-clip`, `clipped`, `missing-from-scans`, `not-carried`,
`before-the-journal` (World Nos. 1–6, before the Journal's first reprint: another source
is needed for those).

## The daily loop

Newspapers.com allows about 30 high-resolution saves a day, so the run takes a week or
more. Each day:

1. **Clip** the Sundays listed under "Next batch to clip" on the status page. Save each
   page as *Entire page, JPG*, into `clippings/`, keeping the name Newspapers.com gives it:
   `The_Minneapolis_Journal_1914_02_15_45.jpg` (paper, date, page). The solution usually
   runs the next Sunday, often on the same page as the next puzzle, so one save may cover
   both.
2. **Intake.** `python tools/record.py new` lists the saved pages not yet recorded. Each
   is looked at only to index it: the grid's printed number and the heading. Clues and
   answers are not transcribed here; puzzle content comes later from the OCR pipeline
   (xword-ocr / blitz), so nothing typed by hand gets in silently. Then
   `python tools/record.py set 1914-02-15 status=clipped world_no_printed=9 heading="..." file=...`
   (and `solution_file=...` on the row whose solution the page carries).
3. **Check** `python tools/record.py check` lists the flags; `python tools/render.py`
   rebuilds the page. Commit, naming the dates covered.
4. **Queue** the next day: `python tools/record.py queue --n 30`, optionally with
   `--priority FROM TO` to put a date range first, or explicit Sundays.

Batch 1 is a spot check, about one Sunday every two months across 1914–1917, plus the
Sundays around the Globe's 1917-02-25 puzzle. It maps where the Journal carries FUN,
where the grid numbers stop and where the record may break, before the sequential fill
from 1914-02-15.

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

Page images from Newspapers.com stay out of this repo (`.gitignore`); `status.tsv`
records each clipping's URL and local file name. Whether 1914–1917 images are published
anywhere is a separate decision, not taken here.
