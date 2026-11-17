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
| `draw.py` | draws a boxes file on its pages, to check it (`python draw.py <xdid>`) |
| `build_packets.py` | the review packets: in the scans repo, `packets/nyw-1914-s1/` (each puzzle's scan with its boxes, the clue list beside it, the key's letters drawn in its squares) |
| `run-pages.tsv` | the run's folder source (the batch's 69 rows of `pages.tsv`) |

The run itself (harvest, text step) is `blitz-work/runs/nyw-s1`.

**Checked (Claude, 2026-11-16):** every boxes file passes `draw.py` with no problems; in every
puzzle with a solution, every clue's answer is a straight run of squares in the grid, except three
of No. 13's diagonal words (below). No. 3 has no solution anywhere: shape and clues only.

## Open decisions (Alex)

1. **Misprinted clue pairs.** Some files write the pair the grid needs and keep the printed one in
   the boxes file (`printed`); others (Nos. 1-3 and a few more) keep the printed pair in the xd.
   gxd's No. 2 uses the pairs that fit. One rule for all.
2. **Numbering for numbers above 35.** A-Z for 36-61 is shared, but above 61 the files use ASCII
   symbols (Nos. 20, 27), Greek (Nos. 22, 23) or Greek and Cyrillic (No. 29), and No. 13 skips E.
   Each file's `Numbering:` header states its scheme. One scheme (or another way to write numbers).
3. **Titles.** About half the files take FUN's heading ("FUN'S Cross-Word Puzzles") as the Title;
   READING.md said not to. Real titles: No. 3 "Find the Missing Cross Words", No. 10 "A George
   Washington Cross-Word Puzzle", No. 17 the Easter puzzle, No. 25 the July 4 puzzle, No. 31
   "Some Geography!"?
4. **Misprinted key letters.** Kept as printed in the grid: No. 4 ROAB (MOAB), No. 10 OSEL, No. 11
   WELD/DOW (MELD/DOM), No. 21 RABIT, No. 23 CRATES (GRATES), No. 25 EARNS (ERNES). blitz's ship
   rule corrects a misprinted key letter with an "Answer key corrected:" note.
5. **Shapes xd can't hold.** No. 13's four diagonal words print their middle letters between
   squares; No. 18 has four diagonal words; No. 29's small pieces sit half a square off. Shaded
   interior squares: `#` or `_` (No. 22's hourglass, No. 17's ornament square).
6. **Words with no printed clue** (answer in the grid only): No. 1 2-3, No. 17 1-2 and 33-34, No. 23
   63-77, No. 24 11-19, No. 27 10-26, No. 32 17-18.
7. **gxd and shipped copies.** No. 1: same grid as gxd, but gxd's Numbering leaves out 32 and 33,
   its heading and one clue differ, and the Sentinel prints no clue for 2-3. No. 2: five clue
   numbers misprinted in the Sentinel, gxd drops the clues' periods. No. 12: the Sentinel credits
   Evangeline Kearney, which `xd/nyw1914-03-08.xd` lacks; No. 11: same grid and clues as shipped.
