# Reading a 1913-14 World FUN crossword from the scan, with every text tied to its place on the page

The New York World's Sunday FUN section printed these puzzles; the Milwaukee Sentinel carried FUN
itself, on the World's own Sundays. The OCR pipeline finds the grids but can't read the clue lists
or the solution keys well enough, so Alex (the owner) has these read straight from the scan. Two
things matter equally: **the text is what is printed**, and **every piece of text is tied to its
place on the page image** (a box in the page file's own pixels), so a reviewer can check each one.

Never guess. What you can't read with confidence goes in your doubts file, not into the xd as if
it were certain.

## Files

- Page images: `C:\Users\adeja\Projects\newyorkworld-scans\pages\<file>` (read them with Read;
  zoom by cropping with Python/PIL into `hand-read\crops\`; the coordinates you record are always
  in the page file's own pixels, never a crop's: add the crop's offset back).
- OCR lines for each puzzle page: `hand-read\ocr\<page stem>.tsv`: `id x0 y0 x1 y1 score text`,
  sorted top to bottom. The text is often wrong; the boxes are where the pipeline saw text.
- The detector's grids on each page: `hand-read\ocr\<page stem>.grids.json` (rows, cols, corners
  TL TR BR BL). Often the wrong size, above all for solution grids: check and correct.
- The text step's attempt (a second opinion, often wrong): `textstep\s1\<pid>\text.md` and
  `answer.json`, where the pid is the xdid plus `-L000`/`-L001` (look in `textstep\s1\`).
- gxd's copies of Nos. 1 and 2 (for those two only): `C:\Users\adeja\Projects\gxd\nyworld\1913\`.
- The model of an xd: `C:\Users\adeja\Projects\gxd\nyworld\1913\nyw1913-12-28.xd` (read it).
- Run folder: `C:\Users\adeja\Projects\blitz-work\runs\nyw-s1\` (hand-read\ is in it).

## What to write (in hand-read\, with the Write tool; nothing in any git repo)

1. `<xdid>.xd`, gxd's format, as the model: headers, the grid from the printed solution (`_` for
   squares outside the template and for the shaded centre block; `#` only for a true black
   square), the clues in the order printed as `a-b. Clue text. ~ ANSWER`, and the Numbering section
   mapping the printed end-square numbers onto the grid (a letter for numbers above 9, as the model
   does). Headers: Title only if the puzzle prints its own name (not FUN's banner); Author only
   from a printed credit; Copyright: New York World; Date: the World date; Number: the printed
   number, if printed (heading, centre block or intro: say which in Notes); Notes: the design in a
   sentence, the credit line as printed, and last: "Read by hand from the Milwaukee Sentinel's page
   (<file>), solution from <file>, by Claude, 2026-11-16."
2. `<xdid>.boxes.json`, the tie between text and page:

```json
{"xdid": "nyw1914-06-14", "no": 23,
 "pages": {"puzzle": "Milwaukee_Sentinel_1914_06_14_87.png", "solution": "Milwaukee_Sentinel_1914_06_21_86.png"},
 "grid": {"page": "puzzle", "corners": [[450,117],[1077,98],[1077,926],[452,925]], "rows": 28, "cols": 21},
 "key":  {"page": "solution", "corners": [[..],[..],[..],[..]], "rows": 28, "cols": 21},
 "lines": [{"label": "heading", "text": "FUN'S CROSS-WORD PUZZLE No 23", "page": "puzzle", "ocr": ["o3","o5"]},
           {"label": "credit", "text": "This cross-word puzzle is furnished by H. J. Stack of Hartford, Conn.", "page": "puzzle", "box": [1095,170,1225,330]}],
 "clues": [{"pair": "2-3", "text": "Plural personal pronoun.", "answer": "WE", "page": "puzzle", "ocr": ["o101"], "how": "ocr-corrected"},
           {"pair": "4-5", "text": "Opposite of off.", "answer": "ON", "page": "puzzle", "box": [447,968,700,990], "how": "eye"}]}
```

   - `ocr`: the OCR line ids the text is printed in (one or more). The box is then their union
     (draw.py fills it in). `how`: "ocr-exact" (the OCR line's text is right as is),
     "ocr-corrected" (it's the right place, you corrected its text), "eye" (no OCR line covers it:
     give `box` yourself, `[x0, y0, x1, y1]` in page pixels, tight round the printed clue).
   - An OCR line that runs two clues or a clue and a joke together: cite it, and also give a tighter
     `box` round your clue's part (a given `box` wins).
   - `grid` and `key`: the lattice that puts every square in place. Corners are the outer corners
     of the whole rows x cols rectangle (squares outside the template included), TL TR BR BL. Start
     from grids.json; correct size and corners until draw.py's lattice lies on the printed rules.
   - `lines`: every printed line that belongs to the puzzle: heading, number, credit, intro,
     instructions (label each one so).
   - A page with no second page (the solution printed elsewhere, or none): leave that role out of
     "pages".
3. `doubts-<xdid>.md`: every square, word or clue you couldn't read with confidence; anything odd
   (a misprint you kept, a clue whose answer doesn't fit the key, a pair that names the wrong end
   squares, a given letter that disagrees with the solution); and for Nos. 1 and 2, every
   difference from gxd's copy (grid, numbers, clue text, punctuation, headers).

## Check before you finish

Run `python C:\Users\adeja\Projects\blitz-work\runs\nyw-s1\hand-read\draw.py <xdid>` (plain
Python, PIL). It fills in the boxes, lists problems (a clue with no box, an OCR id that doesn't
exist) and draws `overlays\<xdid>-puzzle.png` and `-solution.png`. Look at the overlays (crop with
`--crop puzzle x0 y0 x1 y1` to see one region at full size): every clue's box must sit on that
clue, the lattices on the printed squares. Fix and run again until it's clean. Then check the xd
yourself: every clue's answer runs between its two numbered end squares in the grid, letter for
letter with the solution.

## How the World printed these (from the earlier runs)

- A clue names its word by the numbers in its two end squares: "1-2 To unite in matrimony". There
  are no Across and Down lists; Across-like words come first, then Down-like, as printed.
- Every clue ends in a period; keep the printer's spelling and punctuation, misprints included
  (note them in doubts).
- The grid is a template (diamond, cross, hourglass, pyramid, X, W...). The shaded centre block
  often holds "No 11" or "FUN"; letters printed in squares as part of the design (FUN, EASTER,
  AMERICA) are squares of the puzzle, with their letters.
- The solution is in the next Sunday's FUN ("Solution to No 11 Puzzle"), sometimes on the same page
  as the next puzzle; some solution boxes hold two grids (another puzzle's): use the one that fits.
- A puzzle of several pieces (No. 13 two in one, No. 29 five in one): one xd, the pieces laid out in
  one grid as printed with `_` between them; say so in Notes.
- FUN's pages mix jokes and cartoons into the columns beside the clues: they are not clues.
