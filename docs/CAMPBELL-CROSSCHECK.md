# Cross-check against Campbell, Popik and Crossword Craze (2026-10-31)

Read in full: T Campbell's [Arthur Wynne](https://tcampbell.substack.com/p/arthur-wynne) post, his
"Year in Crosswords" posts for 1914 to 1929 and his
[corrections](https://tcampbell.substack.com/p/year-in-corrections); Ben Zimmer's
[Crossword Craze](https://crosswordcraze.today/) (25 posts, nearly all 1924, text only). Campbell's
text was read in full, but only about 12 of his images were looked at. "Reported" below means
Campbell says so and it has not been checked against a page.

## 1. For anyone indexing now: Globe date is not World date after about 1918

The rule "Globe date = World date" (`world_dates_1917.py`, `LAGS` in `tools/record.py`, the status
page, README) was established for 1917. It does not hold later.

**Proved from our own table.** Campbell dates a puzzle to 1919-10-12: the 9-wide, 22-tall grid
whose intro claims the longest word in the English language. That is our Globe 1920-05-02 (same
shape, same intro, "1-9 A skin used for writing"), **29 weeks later**, tagged World No. 333.

**Likely, not proved.** Campbell's Journal puzzle of 1919-08-17 (Capt. F.W. Steffen, five long
words) looks like our Globe 1919-12-14 ("1-13 An embodiment"), 17 weeks later. The match rests on
the first clue fitting the top-row answer in Campbell's image. Our index gives that Globe grid as
about 13 wide, and Campbell's is 15, so check the shape.

**Reported by Campbell.**
- 1919: the Globe starts the year a couple of weeks behind the Pittsburg Press and falls further
  out of step, until FUN designs appear in it months apart from other papers. In 1917 the Globe
  ran ahead of Pittsburgh, so the relationship had already reversed by January 1919.
- Early 1920: the World and its partners ran no new crosswords for about two months, resuming in
  late February. The Globe kept printing, which our table confirms (a puzzle every Sunday,
  1920-01-04 to 02-29, each with a World number).
- February 1922: the Globe prints puzzles not seen in the World or Jerry King that month. He can't
  say whether they are its own or reprints from earlier years.
- 1923-03-18: the Globe is "still recycling" World puzzles from two years earlier.
- The World also ran other puzzles in place of the crossword at least twice in 1918, and a maze
  from 1919-01-12 in syndicated papers. So a plain weekly count overstates the World's numbers.

**What is affected.**
- Treat `world_no` on Globe rows as a date-derived label, not an identification, from about 1918
  to 1923-04-29, where the numbers already stop. The printings themselves are good copies.
- `LAGS["boston-globe"] = (0, 0, ...)` and the candidate dates built from it. Other papers' lags
  were measured against the Globe's date, so check those too for 1918 on.
- `wanted.tsv` and `gaps.tsv` rows for Globe gaps (1918-09-08, 1919-01-05, 1919-07-13, 07-20). A
  Globe skip may have delayed the queue, not dropped a World puzzle: 1918-09-15's solution is
  labelled for the Sept 1 puzzle.
- Lines claiming the Globe ran on the World's date: `tools/render.py`, README, and the `match`
  text on rows after 1917. Scope them to 1917.

**What is not yet known.** When the drift starts (solidly on the World's date in 1917, off it by
January 1919), and how much of 1920 to 1923 is delay and how much reuse.

**How to date it.** Get dated non-Globe copies across 1918 to 1923 and match them to Globe rows by
first clue and shape: the Pittsburg Press (searches stop in 1917), the Journal (below), the LA
Evening Express, the Buffalo Courier Express. A few pages per quarter should plot the drift. Until
then, keep indexing as normal, since page facts are unaffected, but don't derive new conclusions
from Globe `world_no`. Same first clue seen twice in the Globe so far, both unchecked: "To catch
sight of" (1917-08-05, 1919-03-30); "A beverage" (1919-06-08, 1922-06-04).

## 2. Corrections to our notes

- **The Journal did not leave FUN for good on 1917-01-28.** Campbell quotes Journal puzzle intros
  of 1919-08-03 and 1919-08-17 and has it taking Jerry King from March 1920. Our evidence for the
  end is February and March 1917 only, plus text-search misses. The Journal apparently returned;
  when is open. RESEARCH item 2's "last FUN puzzle" needs that scope.
- **No. 4 exists in print.** Campbell's 1914 post reproduces it complete ("The fourth in FUN'S
  series", first clue "1-2 To help"). `status.tsv` lists it as wanted, and the source of his copy
  isn't stated.
- **The weekly count has dated support.** [Popik](https://barrypopik.com/blog/crossword_puzzle)
  cites the World of 1914-01-11, Fun p. 12, for that same line, and 1914-01-04, p. 8, for "Find the
  Missing Cross Words" (read through a summary; check the page). No. 10 (Washington) matches our
  unnumbered 1914-02-22. The Journal's "fifth" on 1914-02-01 is its own miscount.
- **First reader credit.** Campbell has Mrs. M.B. Wood one installment after No. 7, so apparently
  No. 8 (1914-02-08), before Katherine Reilly (1914-04-05). Our No. 8 is a clipping, not a full page.
- **The 13-year-old of 1916-04-02** is Benjamin R. Scott of Shrewsbury, N.J.: Campbell's copy has
  nearly the same blurb, with the name.
- **F, U, N.** Campbell places them in January 1915, which fits Nos. 55 to 57 on the World's dates
  and the Journal's 01-24 to 02-07 as about three weeks late. He quotes the line "That spells FUN",
  which may settle what those puzzles were; he says nothing about solutions.
- **Thomas C. Kelly's circular puzzle** is in Campbell's 1914 post, undated, and not in
  `printings.tsv`. E.H. Sheppard of Somerville, N.J. (the multi-cross grid there) isn't either.
- **Globe Saturdays began 1923-05-26** as we have it. Campbell's May 27 is a Sunday.

## 3. New sources

- **LA Evening Express**: reported from 1918-06-09, with a February 1919 testimonials promo.
- **Buffalo Courier Express**: reported running the World's puzzle in 1919 to 1922, with intros;
  dropped it for Jerry King in 1923.
- **Pittsburg Press** and **Minneapolis Journal** in 1918 to 1920: no searches here yet.

Dated World features, useful as anchors: 1915-03-07 "twenty-five cross-words every day" (we hold a
Journal page of that date), 1919-01-26 "Combination Cross-Word/Word Square", 1919-11-09 "96-word"
interlock intro, February 1922 Valentine heart (Robert Hamilton).

Style dates that matter for parsing: vertical clues moving to numerical order during 1922; modern
numbering (no end numbers) in the World from 1923-07-22.

## 4. Who may hold World pages

- Will Shortz: Parker Higgins of Crossword Craze got a scan from his collection.
- Natan Last quotes the World's 1914 note; his book is *Across the Universe* (Pantheon, 2025).
- Barry Popik cites World pages with page numbers; Ben Zimmer may know how.
- T Campbell: his scans of Nos. 4, 7, 8 and 10; ask where they come from.

## 5. For the catalog (not this repo)

- `first-runs.md` says syndicates join from October 1924. Crossword Craze has Bell Syndicate in the
  Indianapolis Star from February 1924 and the Burlington Free Press from 1924-03-13.
- Add: Washington Evening Star (February 1924, front-page promotion); Lloydminster Times (by
  1923-07-01, first known modern numbering); New York Tribune and Herald Tribune.
- The Globe's Wednesday and Saturday series, "probably own": the Cross Comment posts name local
  makers (Marion Mellus of Newton for the Wednesday 1924-04-23 puzzle; Chet Bent; L.C. Hall), and
  Campbell quotes 1923 rejection notes.
- Madeleine Marshall, Stern (the Herald Tribune spells it Stearn) and the convention: May 18, not
  the May 23 in one Crossword Craze post.
- `first-runs.md`'s list of Campbell posts not yet read can be closed through 1929.
