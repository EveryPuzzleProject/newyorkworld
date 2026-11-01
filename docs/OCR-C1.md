# OCR of chain C1 (the Journal's pages, 1914-02-15 to 08-09): coverage and exceptions

Run through xword-ocr (branch `claude/nyw-fun-c1`), 2026-11-01, as far as the pipeline and its
allowed interventions go: the harvest, hand-drawn grids where the detector reads a template at
the wrong size, the text step (Claude Sonnet) and the AI proof review (Claude Sonnet), triage.
Nothing typed in. The harvest is `xword-ocr/harvests/nyw-c1` (pubid `nyw`); the current run is
`c7` (`pipeline/triage/runs.json`); its proof packets are on the review site as batch
`nyw-1914-c1`; triage is `harvests/nyw-c1/triage/c7`. The fix file is `fixes/fixes.toml`: the
World's clue style (`[ocr] linked_ends`), pages read in tiles (`[ocr] tiles`), solutions in the
next issue (`[assembly] keys_next_issue`), each issue's World date (`tools/ocr_fixes.py`), and the
hand-drawn grids. The text step's conventions are `editorial.md`.

## Coverage

| | pages |
|---|---|
| Journal pages in C1 with an image | 24 (02-15 to 08-09; Nos. 7 and 8, 02-01 and 02-08, exist only as clips) |
| grid found at the right size (the detector, or a hand-drawn grid) | 22 (06-07 prints only a solution; 05-10's rules are too faint) |
| passes the harvest's own gate (clues line up) | 11 |
| assembled hands-off into a puzzle with clues | 8: Nos. 10, 11, 12, 13, 15, 19, 20, 22 (ids nyw1914-02-22, 03-01, 03-08, 03-15, 03-29, 04-26, 05-03, 05-17) |
| of those, with next week's key matched | 6 (No. 20's key, on the 05-10 page, and No. 22's, on 06-07, aren't found at the puzzle's size) |
| the World's number read from the centre block (Number header) | 5 (11, 12, 15, 19, 22); No. 10 and No. 13 print no number in the centre; No. 20 prints it in a box beside the grid (flagged) |
| triage | 2 ready for review (Nos. 11, 12), 6 needs work; 0 pass the ship check |
| the AI proof review | 8 of 8 Not ready, each with yes/no flags on the proof page (one edit made in all: a trailing noise trimmed on No. 10's A23) |

**What the pipeline gets right:** the templates' shapes (diamonds, the cross with corner
squares, the hourglass, the X), the shaded centre as the template's squares, the across clues
with their printed pairs, the key's letters where the capture is good, the World's number from
the centre block, the xd in gxd's form for nyw1913-12-28.

**What it gets wrong, every time, and the proof page shows as flags:** the slot a clue's text
is put on. The numbers are inferred from the clue list and the grid; one clue the OCR loses, or
one pair misread, and the words after it are one slot out of step until the next sure pair.
On 03-29 and 04-26 the Across texts run one slot ahead of the key from the middle of the list;
on every puzzle several Down texts sit on the wrong word. The key's letters are also unsure on
the 2650-px pages (NSWYORK for NEW YORK).

## What Alex must do by hand

1. **Re-download at the larger size** on Newspapers.com: every page from 04-05 on was saved at
   ~2650 px wide (the first seven are 3500). The clue type reads badly at that size, and the
   key's letters worse. Three pages read almost nothing even in tiles: **02-15 (No. 9), 06-28
   (No. 25), 07-05 (No. 26)**; 05-10 (No. 21) reads its pairs but its grid's rules are too faint.
   After a re-download, `harvest --reanalyze --only <issue>` reads the page again.
2. **On the proof page, batch nyw-1914-c1**, for each of the 8 puzzles: answer the AI reviewer's
   yes/no flags (a clue on the wrong word, a key square), and fix what the flags point at. Nos. 11
   and 12 are the nearest to done. Every value entered shows as the reviewer's, with its source.
3. **No. 10 (02-22) and No. 13 (03-15) print no number in the centre:** confirm "no number
   printed" or give it from the index (printings.tsv: 10 and 13) on the proof page.
4. **No. 29 (07-26)** is a puzzle in pieces (two staircases and three small squares, words 1 to
   104): the pipeline reads the pieces as separate grids. It stays an exception until pieces
   can be one puzzle, or it is transcribed by hand with its source.
5. **07-19 (No. 28, the "uncompleted" puzzle with no clue list)** and **Nos. 7 and 8** (clips only)
   stay exceptions.

## Exceptions, by kind

| kind | pages | diagnosis | state |
|---|---|---|---|
| capture too small for the clue type | 02-15, 06-28, 07-05 (0 to 24 pair lines read); 05-10 (faint rules) | the type is ~15 px tall at 2650 px | needs the larger download |
| clues read but too garbled to fit | 03-22, 04-05, 04-12 (EASTER), 04-19 (the cross), 05-24 (the X of bands, 06-14), 05-31 (06-21), 06-21 (FUN, 07-12), 07-12 (the W, 08-02) | with hand-drawn grids the shape is right; the pair list fills under half the grid's words (digits misread: "8-86", "$-4") | the same larger download would help; else a person's pass on the clue column |
| the puzzle in pieces | 07-26 (No. 29) | separate grids | exception |
| no clue list | 07-19 (No. 28) | printed as a puzzle to complete | exception |
| key read short | No. 20's key (05-10), No. 22's key (06-07), No. 10's key on 03-01 (hand-drawn, now matched) | apex squares' rules faint | hand-drawn key grids as for 03-01, after the re-download |
| no page image | 02-01 (No. 7), 02-08 (No. 8) | clips only | the Journal's full pages |

## Where to look

- the review site: batch `nyw-1914-c1`, e.g. https://blitz.xwordapp.com/review/?p=nyw1914-03-08-L000
- locally: the proof-proto launch config, `http://localhost:8790/blitz/src/blitz/proof.html?p=nyw1914-03-08-L000&base=/xword-ocr/harvests/nyw-c1/proof/c7/`; the list `harvests/nyw-c1/proof/c7/index.html`; triage `harvests/nyw-c1/triage/c7/summary.md`; the text step's changes with crops `harvests/nyw-c1/textstep/c7/index.html`.

## Decisions taken (in each puzzle's note)

- The grid is written as gxd writes nyw1913-12-28: `_` for the template's squares (the paper
  round the diamond and its shaded centre), clue lines as printed ("1-2. An insect. ~ BEE"), a
  `Numbering:` section saying where each number sits.
- The numbers are read off the clue list and the grid together: the across words take the
  list's first pairs in order, each down pair names the down word through a numbered square.
- The puzzle's date is the World's Sunday (printings.tsv); the Journal page is the Source.
- Hand-drawn grids (fix file `grids`, with `white` squares for the letters printed in No. 17's
  grid) are a person's statement of where the squares are, recorded with their source; the
  squares themselves are read from the page.
