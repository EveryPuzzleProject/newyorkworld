# Batch nyw-1914-c1, retired (2026-11-16)

The first review batch: Nos. 7-30 read from the Minneapolis Journal's pages (`docs/OCR-C1.md`).
Alex retired it on 2026-11-16 in favour of a batch read from the Milwaukee Sentinel's cleaner
pages (`docs/SENTINEL-BATCH.md`). Two reasons:

- Its ids for Nos. 22-30 carry dates from the weekly count, two or three weeks early (No. 22 is
  `nyw1914-05-17-L001`; the World printed it on 1914-05-31).
- Its ledger is keyed by those ids. A Sentinel harvest gives some of the same ids to other
  puzzles (`nyw1914-06-21-L001` is No. 27 here and No. 24 in the Sentinel), so its edits would
  land on the wrong puzzle.

What is here, moved out of the live files so no harvest or ship applies it again:

| file | was | what |
|---|---|---|
| `decisions.jsonl` | `fixes/decisions.jsonl` | proof verdicts, byline gaps, settles and restarts (200 rows) |
| `corrections.jsonl` | `fixes/corrections.jsonl` | the review site's edits (464 rows) |
| `tool-notes.jsonl` | `fixes/tool-notes.jsonl` | why each edit was made (426 rows) |
| `ids.tsv` | `pipeline/ids.tsv` | the registry's 28 ids for the Journal's pages |
| `puzzles/` | `pipeline/puzzles/1914/` | the assembly packets |
| `by-number.tsv` | new | each c1 id with its World number, its count date and its World date, to look up c1's notes for a puzzle by number |

Left where they were:

- `pipeline/ship/nyw-1914-c1.json` and `as-shipped/`: the record of what c1 shipped and held.
- Nos. 11 and 12 (`xd/nyw1914-03-01.xd`, `xd/nyw1914-03-08.xd`): shipped, with their rows in
  `provenance.jsonl` and `fixes/xdids.tsv`. The Sentinel batch checks them.
- The Journal's hand-fitted grids in `fixes/fixes.toml` (`[page."minneapolis-journal-…"]`): keyed
  by the Journal's pages, so they touch nothing else, and they are needed if those pages are ever
  read again.
- `pipeline/scan/minneapolis-journal-*.json`: page records, not puzzles.

Use: for each puzzle in the Sentinel batch, the reviewer gets c1's corrections and notes for the
same World number (`by-number.tsv` → pid → the rows here) as things to check. None is applied.
