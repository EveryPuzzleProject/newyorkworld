# Checking brief: does this printed solution answer that puzzle?

You are checking links in a chain of newspaper crosswords for a research project. Each image is a
full newspaper page from 1914-1924 (Newspapers.com download). For each pair you are given two
pages: a PUZZLE page and a SOLUTION page, which may be the same paper or two different papers.
The question is always the same: **does a filled solution grid printed on the SOLUTION page answer
the empty puzzle grid on the PUZZLE page?** Some pairs add a narrower question (which of two
solutions on the page, for instance); answer that too.

RULE: index only. You may read clues and answers on the images in order to compare them, but do
NOT write any clue or answer word in your output. Report the verdict and what kind of agreement you
saw, in words like "same shape, black squares match, first three across answers fit their clues".
Never type a clue, an answer or a grid.

For each pair:
1. Make a downsampled copy of each page to find the grids (Python: PIL, e.g. thumbnail to 1400px
   tall) and Read it; then crop the puzzle grid, its first clues, and the solution grid at full
   resolution and Read the crops. Write temporary images under the folder you are given.
2. Compare:
   - shape: same overall outline and same black-square pattern? (A printing may be redrawn or
     slightly different in width; that alone is not a mismatch.)
   - fit: do at least three answers in the solution grid fit their clues on the puzzle page at
     the right numbered squares? Check across and down, away from the top row too.
3. Decide:
   - yes: shape agrees and at least three answers fit.
   - no: the shape differs or the answers do not fit. Say what it looks like instead.
   - unclear: the print is too dark, cut off or broken to tell; say why.
   If a page has no solution grid or no puzzle grid at all, say so in the note and give "unclear".

Output: write ONE JSON file at the path you are given, a list with one object per pair:
`{"id", "puzzle_page", "solution_page", "verdict", "shape": "same/different/unreadable",
"answers_checked": <number that fit>, "confidence": "high/medium/low", "note"}`, with the note in
one sentence and free of clue and answer words. Then reply in 2-3 lines with anything surprising.
Keep your reply short; the JSON is the deliverable.
