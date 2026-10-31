# Globe pages kept outside the Sunday series

Scans in `../newyorkworld-scans/`, not indexed in `printings.tsv`.

- `special/The_Boston_Globe_1924_05_25_82.jpg`: Sunday 1924-05-25, news page 8, "Cross-Word Puzzlers
  Hold First Convention". Prints the puzzle used in the championship speed contest (the first such
  contest): a small grid, about 15 wide, first clue "1 Across Baffle", no solution on the page. Not a
  Sunday-magazine puzzle and not part of any series; kept for the contest. The Sunday puzzle of the same
  date is `The_Boston_Globe_1924_05_25_95.jpg` (By E. R. M., Somerville).
- Weekday puzzles (indexed 2026-10-31, kept apart from the Sunday chain with their own paper ids, no World numbers):
  `boston-globe-saturday` (60 pages, 1923-05-26 to 1924-07-12; "The Globe's Saturday Cross Word Puzzle" from
  1923-06-09, solvers' "Cross Comment" column), `boston-globe-wednesday` (23 pages, 1924-02-06 to 1924-07-09),
  `boston-globe-other-days` (one-offs: Thanksgiving 1923-11-29, New Year's Day 1924-01-01, Friday 1924-02-22,
  Friday 1924-05-30). The pages sit in `pages/` with the Sundays. Within each of the Saturday and Wednesday series every
  page's solution answers the previous page's puzzle, except Saturday 1924-06-07 (its solution is for the Memorial
  Day special; a Marathon puzzle ran 05-31 with winners named 06-07 and 06-14). The one-offs' "gaps" rows in
  gaps.tsv are just that: unrelated pages.
  Convention: Saturday 1924-05-24 says the puzzlers' convention was held in New York the Sunday before (05-18).
