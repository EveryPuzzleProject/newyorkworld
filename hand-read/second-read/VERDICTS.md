# The blind second reading, settled against the scans (2026-11-25)

Eight Sonnet agents read the clue lists of Nos. 1-33 again from crops of the scans, never seeing
the xd (`second-read/nyw*.txt`). `second_read.py` compared the two readings. Before the fixes below,
1,232 printed lines, of which 1,188 agree (1,168 word for word, 6 once the reader's
own doubts are set aside, 14 differing only in punctuation or a word broken at a line end). Claude
(Opus) then looked at each of the other 44 lines on a close crop of the scan. `REPORT.md` is the comparison rerun after the fixes.

## The xd was right (13 text lines)
The blind reader tidied the paper's own errors; the xd keeps them as printed, which is the rule:
"Same,as air." · "Foolis' talk." · "implemeut" · "lignt" · "arount" · "Qpality" · "with s grip" ·
"To-fortify." · "Seed-vessel" · "go to he ball game" · "Water in a solid mass." · "A unit." ·
No. 22's "5864" (the paper dropped the hyphen; the pair is 58-64).

## The xd was wrong: misprinted pairs, now recorded (14)
The first reading had noticed 12 of these (they are in the boxes files), but the renumbering of
2026-11-17 (`modernize.py`) took the World's pair from the xd, where they hadn't been written, and
so recorded the pair that fits instead of the one printed. Two (No. 23's 59-72, No. 27's 25-61)
are new. Each now has `^Printed:` (the print), a misprint `^Note:` and `^Fits:` (the pair that fits).

| No. | xdid | clue | printed | fits |
|---|---|---|---|---|
| 5 | nyw1914-01-18 | D13 | 14-32 | 14-22 |
| 6 | nyw1914-01-25 | A14 | 16-16 | 15-16 |
| 6 | nyw1914-01-25 | A25 | 21-32 | 31-32 |
| 6 | nyw1914-01-25 | D18 | 11-30 | 21-30 |
| 14 | nyw1914-03-22 | D3 | 2-28 | 2-38 |
| 15 | nyw1914-03-29 | A2 | 1-1 | 1-2 |
| 15 | nyw1914-03-29 | A25 | 31-33 | 31-32 |
| 15 | nyw1914-03-29 | D2 | 1-6 | 1-8 |
| 15 | nyw1914-03-29 | D13 | 14-23 | 14-22 |
| 23 | nyw1914-06-14 | D33 | 59-72 | 59-73 |
| 27 | nyw1914-07-12 | 25-64 | 25-61 | 25-64 |
| 31 | nyw1914-08-02 | A5 | 2-4 | 3-4 |
| 32 | nyw1914-08-16 | A8 | 7-2 | 7-8 |
| 32 | nyw1914-08-16 | A25 | 31-22 | 31-32 |

## Can't be told from this scan (left as the pair that fits)
The print is too heavy or broken to tell 3 from 8, 5 from 6, or 2 from 3. The xd keeps the pair
that fits the grid and claims no misprint:
- No. 5 (01-18) A6 "6- 6" or 5-6; No. 7 (02-01) D23 "25 36" or 35-36 (the first reading had
  taken both as misprints; the boxes files still say so).
- No. 17 (04-12) D3 3-10 or 8-10, D18 23-32 or 28-32; No. 21 (05-10) D35 43-52 or 48-52.
- No. 22 (05-31): nine pairs (A30, D12, D17, D32, D35, D41, D42, D45, and D7 above).
- No. 29 (07-26): A5 73-75 or 78-75, D41 22-34 or 22-54, D45 24-32 or 24-82, D49 26-30 or 26-80.

## Corrections (`^Correction:`, Alex, 2026-11-25)
The xd keeps each typo as printed and gives the clue as meant in `^Correction:`. A Sonnet agent went
through all 1,230 clue lines for typesetting slips; since both readings agree on these lines, the
print is confirmed. 21 clues now carry a correction (the 9 typos above, and "Assembled,",
"make by striking", "the first man.", "flag around a staff,", "blook", "Used to billiards.",
"Ahe steel beak", "Heoric", "Blockthorn", "crytogamous", "fo rhealing", "A summed month.").
Left alone as period style: "Non success.", "Die past participle.", "Wing Shaped.".

## For Alex
- **No. 20 (05-03) A32, 37-38** ([review page](https://blitz.xwordapp.com/review/?p=nyw1914-05-03)): settled (Alex, 2026-11-25). The "dash" is the heavy serifed foot of an A whose upper part didn't print, so the line is "A little stream." as the xd has it.
- **No. 17 (04-12) A15, 19-20** ([review page](https://blitz.xwordapp.com/review/?p=nyw1914-04-12)): "In hac salus." or "In hae salus."? The print is too heavy to
  tell c from e; the xd says hac.
