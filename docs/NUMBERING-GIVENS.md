# How to write the World's numbering and givens in .xd

## Decision (Alex, 2026-11-17)

**Modern numbering, with the World's pair as clue metadata.** The proposal below (rules, a `## Labels`
section, `a-b` clue references) is superseded for all but three puzzles. Each clue is numbered as
any crossword is (`A4.`, `D21.`: a square that starts an across or down run of two or more takes
the next number in reading order; a given square is numbered like any other), and carries what the
World printed as clue metadata:

```
A6. A written acknowledgment. ~ RECEIPT
A6 ^Printed: 4-5
A16. What this puzzle is. ~ HARD
A16 ^Printed: 38-39
A16 ^Note: misprint: the pair that fits the grid is 18-19
A16 ^Fits: 18-19
```

- `^Printed:` is the pair as printed, misprints included; a `^Note:` names the pair that fits,
  and `^Fits:` gives it in a form tools read (2026-11-19: the review page labels each run's end
  squares from `^Fits:`, else `^Printed:`, so the blank grid shows the World's own numbers).
- A run with no clue line is a given word (FUN in No. 1) or, with an empty clue (`A4. ~ SALES`), a
  word the paper printed no clue for.
- A line the paper printed twice (No. 26's 27-34, No. 29's 77-79) is one clue; the other line is in
  its `^Note:`.
- Givens stay marked on their squares in the `## Design` section (`G { given: true }`), since some
  are single letters, not words (No. 13's centre E, No. 2's Y, A, R).
- A UI can show the World's numbering from `^Printed:`.
- **Titles and numbers (Alex, 2026-11-25, an editorial decision).** Every puzzle in the series has the same
  Title, `FUN's Cross-Word Puzzle`, and its `Number:` is its place in the series (1-33), printed or not (Nos.
  1-4, 29 and 31 print none). What each page actually printed as a heading is in its `## Printed` section.
  (Supersedes the earlier same-day rule of taking each puzzle's own heading as its Title.)
- **The four kinds of field (Alex, 2026-11-25; blitz `design/xd-fields.md`).** Every statement in the file is
  the puzzle as printed, the paper's other printed words (`## Printed`, `label: text`), EPP's own statements
  (named fields), or provenance (kept out of the xd). The catch-all `Notes:` is gone: our description is
  `Description:`, what's missing is `Incomplete:`, the scans are `Source:` / `Solution-Source:`. A probably wrong
  answer in the printed key stays in the grid, and each clue it spoils gets `^Answer-Correction:` (ROAB →
  `A14 ^Answer-Correction: MOAB`); where what was meant can't be named, a `^Note:` says so. A misprinted pair is
  `^Printed:` + `^Fits:` alone, without a prose note. No. 13's inner star is left out of the grid (in
  `Description:`, with `Incomplete:`).
- **Typos in the clue text (Alex, 2026-11-25).** The clue line keeps the text as printed, the
  paper's slips included; `^Correction:` gives the whole clue as it was meant, so a reader can show
  either. It fixes only typesetting slips (a dropped or wrong letter, a stray comma), never period
  spelling or style, and never what the clue means.
  ```
  D10. A place sheltered from strong lignt. ~ SHADE
  D10 ^Correction: A place sheltered from strong light.
  ```

Tested on all 33 hand-read files: 1,166 of 1,206 clued words fill a whole across or down run. The
other 40 are in three puzzles, which stay in the World's form below (`Numbering:` and `## Labels`)
with a note, to be treated as metas: **No. 13** (the inner star: words inside longer runs, three
meeting at the centre E), **No. 18** (four diagonal words) and **No. 27** (the given FUN runs on
into other words; in effect a bar between 1 Down and 10 Down, and xd has no bars yet).
`hand-read/modernize.py` did the conversion; `hand-read/worldxd.py check` checks both forms.

## The original proposal (superseded except for Nos. 13, 18 and 27)

For Alex. The 1913-14 World FUN puzzles (Nos. 1-33, `hand-read/`) don't number words the way every
other puzzle in gxd does, and some print letters in the grid. Today two gxd files
(`nyworld/1913/nyw1913-12-21.xd`, `-12-28.xd`) carry a `Numbering:` header and a character map
after the clues: Saul's form, used nowhere else, not in the spec (xdformat `doc/xd-format-v4.md`).
It runs out of characters past 61 (our files went on into symbols, Greek and Cyrillic), and its
map is already wrong in gxd's No. 1 (32 and 33 missing). This replaces it.

## What the World printed

- **End-square labels, not word numbers.** A number is printed in each square where a word ends,
  and a clue names its word by its two ends: "1-2. A barber's implement." The word runs in a
  straight line from the first to the second.
- **Any direction.** Across and down, and in No. 18 diagonally (1-3 GAMMA, 4-2 SNARE, 7-5 FRETS,
  6-8 SITES, from the corner squares in to the centre). The order of the pair is the reading order.
- **A printed letter can be an end.** Where a word starts or ends on a given letter, the clue
  names the letter: No. 2 "N-6. The German for north." and "W-7. A summons."; No. 9 "F-4", "P-23",
  "N-5", "S-24"; No. 13 "E-38" (the centre E).
- **Many labels.** Most diamonds run to 36; No. 20 to 76, No. 23 to 91, No. 29 to 104.
- **Misprinted pairs** are common: 18 recorded in the boxes files, and more in Nos. 1-3, whose
  readers kept the printed pair in the xd. The type is clear and the pair names the wrong square.

## Givens

Letters printed in the puzzle's own squares, for the solver to start from (from the scans, all 33
grids looked at, 2026-11-17):

| No. | givens | as words |
|---|---|---|
| 1 | F U N, row 2 | FUN: no clue; ends unnumbered |
| 2 | Y, N E W, A, R | NEW across row 2 and YEAR down the centre (sharing the E); two clues start on N and W |
| 9 | F U N, P U Z Z L E S | FUN and PUZZLES across; four clues start on F, P, N, S |
| 13 | E, the centre square | a letter, not a word: the eight three-letter words of the inner star all use it |
| 17 | E A S T E R, row 3 | EASTER, in black-letter; two clues start on its letters |
| 27 | F U N across and down, crossing at U | FUN twice; the down word 10-26 runs on to FUND, and has no clue |
| 28 | 38 letters, no numbers, no clues | the whole puzzle is "uncompleted": fill in the rest (two givens disagree with next week's solution: H/W at r7c1, N/R at r13c7) |
| 31 | A M E R I C A, middle row | AMERICA |

The other words with no printed clue are **not** givens (their squares are blank): No. 1 2-3
(SALES; the Sentinel dropped it, gxd's World copy has "What bargain hunters enjoy"), No. 17 1-2
and 33-34, No. 23 63-77, No. 24 11-19, No. 32 17-18. Probably the paper's omissions; each is in its
doubts file.

## The World numbered by rule, mostly (Alex, 2026-11-17)

Most of these puzzles number their end squares by one of a few rules, so a file can name the rule
instead of listing the squares. "End square": the first or last square of a run of two or more
squares across or down. "Reading order": row by row, left to right. A square holding a given
letter gets no number (its label is the letter), and the count goes on past it.

| rule | how | puzzles it fits exactly |
|---|---|---|
| `across-first` | each across word in reading order takes two numbers, its start then its end (1-2, 3-4, ...); then the end squares not numbered yet, in reading order | 16: Nos. 4-9, 11, 12, 15, 16, 19, 21, 22, 24, 32, 33 (and No. 3 by eye: no solution to test it) |
| `apex-first` | the top row's end squares first (a diamond's apex: 1), then as across-first | 2: Nos. 1 and 10 |
| `reading-order` | every end square in reading order | 3: Nos. 2, 17 and 23 |
| none | | 10: Nos. 13, 14, 18, 20, 25, 26, 27, 29, 30, 31 |

Tested on the hand-read files: each clue's pair and answer put its two numbers on the grid, and
each rule's numbering was compared square by square (xword-ocr `numbering.end_numbering`, which
already has these three as `across_first`, `apex_first`, `all_ends`). A fit is exact once the
misprinted pairs are set aside: Nos. 1 and 2 differ from their rule only at their misprints (3 and
5), No. 9 at one. The early ones match your reading: No. 1 apex first, No. 2 every end in reading
order (its apex Y is a given), No. 10 apex first again, and across-first from No. 4 on. Nos. 14, 25
and 26 are near misses (the centre column's ends numbered in another order); the rest are the odd
shapes (the X, the hourglass, the W, five in one, the inner star, the diagonals).

## The proposal

Use the v4 draft's headed sections (needed anyway for a Design section), and add one section the
v4 parser already ignores, so these files stay valid xd.

**1. A `Numbering:` metadata field names the rule.** `Numbering: across-first` (or `apex-first`,
`reading-order`). With the grid and the givens (rule 4), that places every printed number: nothing
else to write, and a checker can number the grid and test every clue's pair against it. This
takes over the field name from gxd's map, which it replaces.

**1b. When no rule fits, `Numbering: as-printed` and a `## Labels` section: one line per printed
label, with its square.**

```
## Labels
1 r3c5
2 r3c9
3 r5c3
...
29 r1c7
F r2c6
P r4c4
```

`r<row>c<col>`, 1-based, counted in the Grid section. A label is what's printed: a number, or a
given letter that a clue names as an end (only those). No alphabet to run out of, readable on its
own, and a diff shows a moved number as one line. The printed number's position inside the square
(corner, middle, on the rule) is not kept: the boxes files have it if anyone needs it. (A middle
way for the near misses, a rule plus a Labels section of only the squares that differ, is possible
but adds a third case; listing them all is simpler.)

**2. A clue reference `a-b` means: the word from label a to label b, in a straight line.**

```
1-2. A barber's implement. ~ RAZOR
F-4. To worry. ~ FAZE
4-2. A trap. ~ SNARE
```

The v4 spec already allows any reference text before the first '.', and its uniclue form drops
the A/D. A checker (xdlint) can test what our ad hoc scripts did this week: both labels exist, the
two squares are on one row, column or 45° diagonal, the answer's length is the number of squares,
and its letters are the grid's.

**3. A misprinted pair: the reference is the pair that fits, and the print is kept as metadata.**

```
3-4. Negative. ~ NO
3-4 ^Printed: 2-4
```

v4's clue metadata (`^Key: value`), no new syntax (No. 30's example). The boxes file keeps the same as `printed`.

**4. Givens in the Design section: a given square is styled `given`.**

```
## Design
G { given: true }

.............
.....GGG.....
.............
...GGGGGGG...
```

The letter stays in the Grid (it is the solution's); the Design says it was printed, and the numbering rules
skip it (a given square takes no number). This is one
new property for the Design section, which is otherwise visual (circle, shaded, bars, images). A
given is between the two: the cell is drawn with its letter. If Saul would rather keep Design
purely visual, the fallback is a `Givens: r2c6 r2c7 r2c8 ...` metadata field.

**4b. Why spell the givens out, not infer them (tested 2026-11-17).** The rule "a word of the
grid with no clue line is a given" finds the givens exactly in Nos. 1, 2, 9 and 31 (FUN, NEW and
YEAR, FUN and PUZZLES, AMERICA). It fails on the rest: No. 13's given is one letter, not a word;
No. 17 would add the DS run beside EASTER (two words' ends side by side); No. 18 would add SREM (an
unclued column of crossing letters); No. 27's given FUN runs into the unclued FUND; and No. 28's
givens are scattered letters, two of them different from the solution. Writing them costs a Design
block in 8 files of 33, and the numbering rules need them.

**5. A word with no printed clue (and not a given) gets a clue line with an empty body and a reason.**

```
11-19. ~ LET
11-19 ^Note: no clue printed
```

So every word of the grid is an entry, and the metadata says why its clue is empty. A word printed
whole as a given (FUN, AMERICA) gets no clue line: no clue was printed for it, the Design says it
is given, and its end letters would make poor references (AMERICA would be "A-A", and No. 27's FUN
runs both ways from one F).

**5b. A word the grid can't hold** keeps its clue line and says so: `E-38 ^Offgrid: its middle
letter is printed on the corner between two squares` (No. 13's inner star).

**6. No. 28 (letters given, no clues, no numbers):** the Grid holds next week's solution, the
Design marks the 38 given squares, `Numbering: none`, and there are no clue lines and no Labels. Its two clashes
stay in Notes.

### Not covered: shapes for you to look at

- **No. 13** (two in one): the four diagonal words of the inner star (CUE, RUE, EEN, ELM) print
  their middle letters on the corners between squares, so the grid has no square for them. Grid
  and clues can't agree there; the clue lines are right, the grid holds the two end letters.
  Packet: scans repo `packets/nyw-1914-s1/nyw1914-03-15/`.
- **No. 18**'s diagonal words: covered by rule 2.
- **No. 29** (five in one): three small pieces sit half a square off the main lattice; laid out at
  the nearest square. Cosmetic (the boxes file has their true place). `.../nyw1914-07-26/`.
- **No. 22**'s stippled squares inside the hourglass and **No. 17**'s ornament square: `#` blocks,
  or Design `shaded` on a `_`?

## Replacing gxd's Nos. 1 and 2

With the new versions, once the form above is settled: one MR from the fork (alexdej1/gxd) into
rabidrat/gxd, replacing both files, the `Numbering:` map dropped for the rule name.
One thing to carry over, not replace: gxd's No. 1 comes from the World's own page (via Campbell),
the Sentinel is a reprint. Where the reprint drops something (No. 1's 2-3 clue), the World's text
stands; where they differ in wording ("Sunk in mud." / "To sink in mud."), the Notes say both and
the World's wins. The Sentinel's corrections stand where the World's image is the poorer witness
(gxd's No. 1 Numbering, No. 2's clue-final periods). The xdformat spec could take the Labels
section and the `given` property later, as a documented extension, if Saul likes them.

## Done (2026-11-17, Alex: "do what you think works best")

All 33 hand-read files are in this form (`hand-read/convert.py` did it, once), and
`python hand-read/worldxd.py check` passes on every one: each clue's pair names two squares on one
line under the file's rule or Labels, and its answer runs between them in the grid; every word of
the grid has a clue line or is given whole. The conversion changed exactly the known misprints (No. 1:
3, No. 2: 5, No. 3: 2, No. 9: 1, each with `^Printed:`) and added the six unclued words. No. 1's 2-3
notes the World's own clue for it. The boxes files' pairs follow the xd, with the print in `printed`.

What's still yours:

1. The rule names (`across-first`, `apex-first`, `reading-order`, `as-printed`, `none`).
2. Givens as a Design property, or a metadata field, if Saul wants Design kept visual.
3. Nos. 13, 22, 17 and 29 (above).
