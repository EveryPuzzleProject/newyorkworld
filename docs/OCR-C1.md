# OCR of chain C1 (the Journal's pages, 1914-02-15 to 08-09): coverage and exceptions

First run through xword-ocr (branch `claude/nyw-fun-c1`) on 2026-11-01, hands-off: the harvest,
the text step (Claude Sonnet, one pass) and triage, nothing typed in. The harvest is
`xword-ocr/harvests/nyw-c1` (pubid `nyw`); its page records are in `pipeline/scan/` here; the
proof packets are `harvests/nyw-c1/proof/c1` (not yet published to the review site); triage is
`harvests/nyw-c1/triage/c1`. The fix file is `fixes/fixes.toml`: the World's clue style
(`[ocr] linked_ends`), solutions in the next issue (`[assembly] keys_next_issue`), and each
issue's World date (`tools/ocr_fixes.py`, from printings.tsv), so a puzzle's id is nyw<World date>.

## Coverage

| | pages |
|---|---|
| Journal pages in C1 with an image | 24 (02-15 to 08-09; Nos. 7 and 8, 02-01 and 02-08, exist only as clips) |
| grid found | 23 (06-07 prints only a solution) |
| next week's key found at the puzzle's size | 16 |
| puzzle assembled with clues, hands-off | 4: 02-22 (No. 10), 03-01 (No. 11), 03-08 (No. 12), 03-15 (No. 13) |
| of those, with its key matched | 3 (02-22's key, on the 03-01 page, is read two rows short) |
| after the text step and triage | 3 ready for review, 1 needs work; 0 pass the ship check |

What the pipeline got right on the four: the diamond's shape, the shaded centre as the
template's squares, the across clues in order with their printed pairs, the key's letters
(BEE, MEALS, SETTLER, NETS, SAID, MANE ... for No. 12), the xd in gxd's form for
nyw1913-12-28. What it got wrong: the Down words' pairs are matched by inference from the
list and the grid, and the text step found several clue texts on the wrong Down slot in
each puzzle (its `unsure` and `findings` on the proof page); no title or byline (the Journal
prints a banner, "Cross-Word Puzzles / Can You Solve Them?", not a title); the printed
World number ("No 11" in the shaded centre) isn't OCR'd, so Number is wrong or empty.

## Exceptions, by kind

| kind | pages | diagnosis | what would fix it |
|---|---|---|---|
| OCR misreads the digits of the small clue type | 03-22, 03-29, 04-05, 04-26 (13-wide diamonds) | pairs read as "8-86", "$-4", "9-80"; the list's order repairs some, not enough for both directions | a person's pass on the proof page; or a clue-column re-read at a higher capture resolution |
| capture too small for the clue type | 02-15 (2660 px wide), 07-05 (2677 px), 06-28 | 0 to 7 pairs read on the page; the type is ~15 px tall | re-download these pages at Newspapers.com's larger size |
| letters printed in the grid | 04-12 (EASTER across the diamond), 07-12 (FUN), 07-19 (the "uncompleted" puzzle, no clue list) | a square with a big letter reads as a block; the clue pairs then don't fit; 07-19 has no clues at all | a rule for pre-printed letters (numbering.NONCELL has the hook: `letters`), or a hand box; 07-19 stays an exception |
| irregular template (not a diamond) | 04-19 (cross with corner squares), 05-03 (X, 21 wide), 05-31 (hourglass), 06-14 and 06-21 (lettered X), 07-26 (staircases + three small squares), 08-02 (zigzag W), 08-09 (cross with AMERICA) | the lattice found is the wrong size (27x16 for 06-14, 8x29 for 08-02): the detector's lattice growth and shape rule were made for one connected shape with four rules round each square | each is a one-off; not worth a detector (Alex, 2026-10-31). A hand-drawn grid (fix file `grids`) per page, or leave for the World's own pages |
| clue list not found beside the grid | 05-10 (No. 21, diamond 19 wide) | 5 pairs read, the list is elsewhere on the page or in another type | look at the page in the watch view |
| key read smaller than the puzzle | 03-01's key (02-22's page), 04-05, 04-12 | the apex squares' rules are faint: the lattice grows only where all four rules show | a near-miss key for a person (key-candidates) |
| no page image | 02-01 (No. 7), 02-08 (No. 8) | clips only in the index | the Journal's full pages |

## Where to look

- the proof page, locally: `xword-ocr` worktree, proof-proto launch config, then
  `http://localhost:8790/blitz/src/blitz/proof.html?p=nyw1914-03-08-L000&base=/xword-ocr/harvests/nyw-c1/proof/c1/`;
  the list: `harvests/nyw-c1/proof/c1/index.html`.
- triage: `harvests/nyw-c1/triage/c1/summary.md`.
- the text step's changes with their crops: `harvests/nyw-c1/textstep/c1/index.html`.

## Decisions taken (in each puzzle's note)

- The grid is written as gxd writes nyw1913-12-28: `_` for the template's squares (the paper
  round the diamond and its shaded centre), clue lines as printed ("1-2. An insect. ~ BEE"), a
  `Numbering:` section saying where each number sits.
- The numbers are read off the clue list and the grid together: the across words take the
  list's first pairs in order, each down pair names the down word through a numbered square.
- The puzzle's date is the World's Sunday (printings.tsv); the Journal page is the Source.
