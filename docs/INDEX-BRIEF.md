# Indexing brief: New York World FUN crossword reprints

You are indexing newspaper page images for a crossword research project. Each image is a full
newspaper page from 1914-1917 (Newspapers.com download), named paper_yyyy_mm_dd_page.jpg.
Each page should contain a reprint of the New York World's Sunday "FUN" crossword: in 1914-1916
a diamond-shaped grid with a shaded cross in the middle that prints a series number ("No. 16");
by 1917 grids may be other shapes and carry no number. Sometimes the previous week's SOLUTION
(a filled-in grid, often labelled "Solution to Cross-Word Puzzle No. N" or "Solution of last
week's puzzle") is on the same page, and sometimes there is more than one crossword.

RULE: index only. Do NOT transcribe clue lists or answers. Read only the fields below.

For each image:
1. Make a downsampled copy to find the puzzle (Python: PIL, e.g. thumbnail to 1400px tall) and
   Read it; then crop the grid region and any heading/credit text at full resolution and Read
   the crops. Crop the page's top banner too if there is a puzzle-page banner (PUZZLES / FUN)
   with a copyright line. Write temporary images under your group's folder.
2. Record, per crossword found on the page (usually one):
   - printed_no: the number printed in the grid, e.g. "16", or "none" if the grid has no number,
     or "unreadable". Look hard at the grid's center block; also note a number in the heading
     or intro text separately (heading_no) if there is one.
   - heading: the exact heading above the puzzle (e.g. "Can You Solve Them?", "Fun's Cross-Word
     Puzzle", "Cross-Word Puzzle").
   - credit: any constructor credit or "sent in by ..." line, verbatim; "" if none.
   - copyright_line: any copyright or syndicate line on the page near the puzzle or in the
     puzzle-page banner (e.g. "(Copyright, 1914, by the Du Puy Syndicate.)"), verbatim; "" if none.
   - fun_credit: does the page name FUN or the New York World anywhere around the puzzle?
     Quote it briefly, or "".
   - shape: "diamond", "square", "rectangle", "irregular" etc., and approximate size in squares
     across if easy to see (e.g. "diamond 13 wide").
   - fingerprint: the FIRST clue's label and its first three or four words only
     (e.g. "1-2 A child"), as a matching key. Nothing more from the clue list.
   - intro: one sentence of what the intro text says if it dates or numbers the puzzle
     (e.g. "the sixteenth in FUN's series", "solution next Sunday"); else "".
   - section/printed_page: the printed page number and section name from the page header
     (e.g. "Page Six, Foreign and Feature Section"); the paper's masthead date if visible.
   - solution: if a filled solution grid is on the page: its label verbatim (e.g. "Solution to
     Cross-Word Puzzle No. 15") and its shape; else "".
   - other_puzzles: brief note if the page has a second crossword or other grid puzzles.
   - confidence: high/medium/low for the printed_no reading, with a note if anything is odd
     (e.g. the number looks like 30 or 36).
3. If the page has no crossword at all, say so ("no crossword found") after checking the whole
   page at two scales.

Output: write ONE JSON file at the path you are given: a list of objects, one per image, with
the fields above plus "file". Then reply with a 2-3 line summary of anything surprising
(mismatched numbers, missing puzzles, unreadable numbers). Keep your final reply short; the
JSON is the deliverable.
