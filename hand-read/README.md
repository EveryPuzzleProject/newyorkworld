# Nos. 1-33 read by hand from the scans (batch nyw-1914-s1, 2026-11-16)

The OCR pipeline (xword-ocr) found these grids but not their clue lists or keys: FUN's pages run
jokes and cartoons into the clue columns, and the keys came out garbled. Alex's rule for this batch:
use what the OCR gets, don't extend it for the early puzzles' odd designs, and read the scans
directly where it can't, recording the reading as made by hand. So all 33 were read from the page
images by Claude agents (Opus), following [READING.md](READING.md), with every piece of text tied to
its place on the page.

| file | what |
|---|---|
| `<xdid>.xd` | the puzzle, gxd's form; Notes ends with the pages it was read from |
| `<xdid>.boxes.json` | where each clue and printed line is on the page (pixel box in the page file, and the OCR line ids it came from, `how`: ocr-exact / ocr-corrected / eye), the grid's and key's lattices (corners and size), printed pairs where the xd corrects a misprint (`printed`) |
| `doubts-<xdid>.md` | everything not read with confidence, misprints, and for Nos. 1, 2, 11 and 12 the differences from gxd's / this repo's shipped copy |
| `no2-check.md` | the first check of No. 2 against gxd |
| `puzzles.tsv` | each puzzle's puzzle page and solution page (`newyorkworld-scans/pages/`) |
| `ocr/` | the pipeline's OCR lines and detected grids for each page, the ids the boxes cite (`ocr_lines.py` wrote them) |
| `worldxd.py` | the form's numbering rules, parser and checker: `python worldxd.py check` (docs/NUMBERING-GIVENS.md) |
| `modernize.py` | the one-off renumbering to the modern form, the World's pairs kept as `^Printed:` (2026-11-17; Nos. 13, 18 and 27 kept in the World's form) |
| `convert.py` | the one-off conversion from Saul's `Numbering:` map to that form (2026-11-17) |
| `draw.py` | draws a boxes file on its pages, to check it (`python draw.py <xdid>`) |
| `build_packets.py` | the review packets: in the scans repo, `packets/nyw-1914-s1/` (each puzzle's scan with its boxes, the clue list beside it, the key's letters drawn in its squares) |
| `run-pages.tsv` | the run's folder source (the batch's 69 rows of `pages.tsv`) |

The run itself (harvest, text step) is `blitz-work/runs/nyw-s1`.

**Checked (Claude, 2026-11-16):** every boxes file passes `draw.py` with no problems; in every
puzzle with a solution, every clue's answer is a straight run of squares in the grid, except three
of No. 13's diagonal words (below). No. 3 has no solution anywhere: shape and clues only.

## Open decisions (Alex)

**Numbering settled (Alex, 2026-11-17):** modern A/D numbering, each clue's printed pair as
`^Printed:`, givens on their squares in Design ([docs/NUMBERING-GIVENS.md](../docs/NUMBERING-GIVENS.md),
"Decision"). Nos. 13, 18 and 27 stay in the World's own form, as metas, with a note. Still open:

1. **Titles.** About half the files take FUN's heading ("FUN'S Cross-Word Puzzles") as the Title;
   READING.md said not to. Real titles: No. 3 "Find the Missing Cross Words", No. 10 "A George
   Washington Cross-Word Puzzle", No. 17 the Easter puzzle, No. 25 the July 4 puzzle, No. 31
   "Some Geography!"?
2. **Misprinted key letters.** Kept as printed in the grid: No. 4 ROAB (MOAB), No. 10 OSEL, No. 11
   WELD/DOW (MELD/DOM), No. 21 RABIT, No. 23 CRATES (GRATES), No. 25 EARNS (ERNES). blitz's ship
   rule corrects a misprinted key letter with an "Answer key corrected:" note.
3. **Shapes.** No. 13's inner star (`^Offgrid`), No. 29's offset pieces, No. 22's stippled squares
   and No. 17's ornament square (docs/NUMBERING-GIVENS.md).
4. **gxd and shipped copies.** No. 1: same grid as gxd, but gxd's Numbering leaves out 32 and 33,
   its heading and one clue differ, and the Sentinel prints no clue for 2-3. No. 2: five clue
   numbers misprinted in the Sentinel, gxd drops the clues' periods. No. 12: the Sentinel credits
   Evangeline Kearney, which `xd/nyw1914-03-08.xd` lacks; No. 11: same grid and clues as shipped.
