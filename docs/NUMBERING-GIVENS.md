# How to write the World's numbering and givens in .xd: a proposal (2026-11-17)

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
| 28 | 50 letters, no numbers, no clues | the whole puzzle is "uncompleted": fill in the rest (two givens disagree with next week's solution: H/W at r7c1, N/R at r13c7) |
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

**5. A word with no printed clue still gets a clue line, with an empty body and a reason.**

```
F-N. ~ FUN
F-N ^Given: yes

11-19. ~ LET
11-19 ^Note: no clue printed
```

So every word of the grid is an entry (searches and answer counts see FUN and AMERICA), and the
metadata says why the clue is empty. A fully given word's labels are its printed end letters (F
and N above), listed in `## Labels` like any other end.

**6. No. 28 (letters given, no clues, no numbers):** the Grid holds next week's solution, the
Design marks the 50 given squares, `Numbering: none`, and there are no clue lines and no Labels. Its two clashes
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
rabidrat/gxd, replacing both files, the `Numbering:` header and map dropped in favour of Labels.
One thing to carry over, not replace: gxd's No. 1 comes from the World's own page (via Campbell),
the Sentinel is a reprint. Where the reprint drops something (No. 1's 2-3 clue), the World's text
stands; where they differ in wording ("Sunk in mud." / "To sink in mud."), the Notes say both and
the World's wins. The Sentinel's corrections stand where the World's image is the poorer witness
(gxd's No. 1 Numbering, No. 2's clue-final periods). The xdformat spec could take the Labels
section and the `given` property later, as a documented extension, if Saul likes them.

## Decide

1. `Numbering:` naming the rule (`across-first`, `apex-first`, `reading-order`), and `as-printed`
   with a `## Labels` list of `r<row>c<col>` lines for the ten that fit none; `a-b` references
   (rules 1, 1b, 2). The rule names are mine: rename freely.
2. Misprints as `^Printed:` (rule 3).
3. Givens as a Design property, or a metadata field (rule 4).
4. Empty-body clue lines for given and unclued words (rule 5).
5. Nos. 13, 22, 17 and 29 (above).
