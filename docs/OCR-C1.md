# OCR of chain C1 (the Journal's pages, 1914-02-01 to 08-09): coverage and exceptions

Run through xword-ocr (branch `claude/nyw-fun-c1`), 2026-11-01, as far as the pipeline and its
allowed interventions go: the harvest, hand-fitted lattices where the detector reads a template at
the wrong size, the text step (Claude Sonnet) and the AI proof review (Claude Sonnet), triage.
Nothing typed in. The harvest is `xword-ocr/harvests/nyw-c1` (pubid `nyw`); the current run is
`c9` (`pipeline/triage/runs.json`); its proof packets are on the review site as batch
`nyw-1914-c1`; triage is `harvests/nyw-c1/triage/c9`. The fix file is `fixes/fixes.toml`: the
World's clue style (`[ocr] linked_ends`), pages read in tiles (`[ocr] tiles`), solutions in the
next issue (`[assembly] keys_next_issue`), each issue's World date (`tools/ocr_fixes.py`, plus
the key-only issue of 06-07 by hand), and the hand-fitted grids. The text step's conventions are
`editorial.md`.

## The pages: full pages and crops

Every page from 04-05 on was saved at about 2650 px wide, too small for the clue type, and
02-15, 06-28 and 07-05 read almost nothing. Alex saved Newspapers.com "Select portion" crops at
native resolution (about twice the per-letter detail): `_fun` (the puzzle with its heading and
clue columns) and `_key` (the "Solutions to Last Week's Puzzles" box) for most pages. They are
rows of `newyorkworld-scans/pages.tsv` with `crop_of` naming the page's own row; the harvest
reads a page with crops through its crops (each a leaf of the issue, with the page's link) and
never the page itself. 02-01 and 02-08 (Nos. 7 and 8) have no full page: their two crops are
two pages, and the file named `_fun` holds the solutions box, the one named `_key` the puzzle.
Run c9 reads 02-22 to 03-15, 03-29, 04-26, 05-03 and 07-19 on from the full pages; everything
else from crops.

## Coverage

| | |
|---|---|
| World issues in C1 with a page or crop | 27 (02-01 to 08-09; 05-24 prints no crossword; 05-17 and 06-07 print only a solution) |
| grid found at the right size (the detector, or a hand-fitted lattice) | 25 of 27 puzzle pages (05-10's key lattice is found but its squares don't classify; 07-26 is a puzzle in pieces) |
| assembled hands-off into a puzzle with clues | 22: Nos. 7–27 and 30 (ids nyw1914-02-01 … 06-21 and 07-12) |
| of those, with the next week's key matched | 16 |
| the World's number read from the centre block or the banner (Number header) | 11 (Nos. 7, 8, 9, 11, 12, 15, 16, 17, 19, 22, 24); the rest print none in the centre (Nos. 10, 13, 25), or the crop cut the box (No. 20, 23, 26, 27, 30), or the list has no number crop (14, 18, 21) |
| keys recorded without a puzzle page | No. 6 (the 02-01 solutions box) |
| triage | 3 ready for review (Nos. 7, 11, 12), 19 needs work; 0 pass the ship check |
| the AI proof review | 22 of 22 Not ready, each with yes/no flags on the proof page (one small edit on No. 12; everything else flagged, never moved): clue texts on the wrong word where a pair was lost or misread, key squares, missing numbers. No. 12's clues all match their crops now; its flags are two unread key letters |

**What the pipeline gets right now:** the templates' shapes at native resolution (the diamonds,
the even diamond with EASTER, the cross with corner squares, the hourglass, the X of bands, the
W), the clue pairs as printed on most crops, the key's letters, the World's number, the xd in
gxd's form for nyw1913-12-28.

**What it still gets wrong, and the proof page shows as flags:** the word a clue's text is put
on. The numbers are inferred from the clue list and the grid; a pair the OCR garbles beyond
repair ("8-86", "$-4") leaves its squares unnumbered, and the Down pairs that pass through
them can't be placed or land on a near match. Run c9 places more of them (a pair garbled in
one digit is kept for its word, pairs of new numbers go to words in number order, a lost word
keeps its numbers when the next pair confirms them): on No. 12 every clue read is on its word.
The gates were lowered to a quarter of the words so these puzzles come through for review at
all: the words no pair reached show as missing.

**Reviewing these on the proof page (since run c9):** each clue row shows the pair as printed
("33-34. Flesh for food."), the same label as on the scan, and the blank grid shows the
numbers printed in the squares, so a text on the wrong word can be checked against the two
end squares it names. The xd writes the clues with their pairs ("1-2. An insect. ~ BEE") and a
Numbering section, as gxd writes nyw1913-12-28; a clue whose pair wasn't read keeps its slot
label (A4). The page change is on the blitz branch `claude/nyw-linked-proof`; until it is
deployed, the live site shows the standard numbers.

## What Alex must do by hand

1. **On the proof page, batch nyw-1914-c1**, for each of the 22 puzzles: answer the AI reviewer's
   yes/no flags (a clue on the wrong word, a key square), and fix what the flags point at. No. 12
   is nearest to done (two key letters), then Nos. 7 and 11. Every value entered shows as the
   reviewer's, with its source. Merge and deploy blitz `claude/nyw-linked-proof` first, so the
   page shows the printed pairs and the squares' numbers.
2. **No. 10 (02-22) and No. 13 (03-15) print no number in the centre:** confirm "no number
   printed" or give it from the index on the proof page. No. 7's shaded centre says No. 7 while
   the Journal's own heading says No. 5 (its fifth): the number is the World's.
3. **Keys that did not match** (the proof page shows the grid blank): Nos. 14, 16, 21, 24, 25,
   30, see below. Each key is on its crop; a person can confirm the key on the proof page.
4. **No. 29 (07-26)** is a puzzle in pieces (two staircases and three small squares, words 1 to
   104); **No. 28 (07-19)** has no clue list; **Nos. 31–33** have no page image. They stay
   exceptions.

## Exceptions, by kind

| kind | puzzles | diagnosis | state |
|---|---|---|---|
| clue list too garbled to pair | No. 8 (15 of 34 pairs read even from the crop; the Down column is tiny), No. 18 (the Across texts can't be placed) | the crop's type is still small, digits misread | a person's pass on the clue column from the proof page |
| key found, not matched: the grid read with an extra row | No. 16 (04-05, read 14 x 13; key 13 x 13), No. 24 (06-21, 14 x 13; key 13 x 13) | the apex squares above and below the diamond read as a row of their own | a hand lattice of 13 rows if the apex squares aren't letter squares; else the key is right to differ |
| key found, its lattice doesn't classify | No. 21 (the 05-17 key crop: 20 x 19 found, every square reads white) | the key's letters and thick rules at native size | a person confirms the key on the proof page |
| key found at the wrong size | No. 14 (03-29 page: the puzzle's own squares misclassified), No. 25 (the 07-05 crop reads its key 11 x 13 of 13), No. 30 (08-09 prints the W's key in two pieces) | detector | exception until a hand lattice is fitted |
| the puzzle in pieces | No. 29 (07-26) | separate grids | exception |
| no clue list | No. 28 (07-19) | printed as a puzzle to complete | exception |
| no page image | Nos. 31–33 | not downloaded | the Journal's pages of 08-16 on |

## Where to look

- the review site: batch `nyw-1914-c1`, e.g. https://blitz.xwordapp.com/review/?p=nyw1914-03-08-L000
- locally: the proof-proto launch config, `http://localhost:8790/blitz/src/blitz/proof.html?p=nyw1914-03-08-L000&base=/xword-ocr/harvests/nyw-c1/proof/c9/`; the list `harvests/nyw-c1/proof/c9/index.html`; triage `harvests/nyw-c1/triage/c9/summary.md`; the text step's changes with crops `harvests/nyw-c1/textstep/c9/index.html`.

## Decisions taken (in each puzzle's note)

- The grid is written as gxd writes nyw1913-12-28: `_` for the template's squares (the paper
  round the diamond and its shaded centre), clue lines as printed ("1-2. An insect. ~ BEE"), a
  `Numbering:` section saying where each number sits.
- The numbers are read off the clue list and the grid together: the across words take the
  list's first pairs in order, each down pair names the down word through a numbered square.
- The puzzle's date is the World's Sunday (printings.tsv); the Journal page is the Source.
- Hand-fitted grids (fix file `grids`, with `white` squares for the letters printed in Nos. 9
  and 17, `puzzle = true` for the X whose numbers read as letters) are a person's statement of
  where the squares are, recorded with their source; the squares themselves are read from the page.
- A solutions box is always last week's puzzle's: an issue's own keys are never taken
  (`keys_next_issue`), and the key-only issue of 06-07 is dated the World's 05-24, whose
  solution it carries.
