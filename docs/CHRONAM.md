# Chronicling America and the World's FUN crossword

Searched 2026-10-31 through the loc.gov JSON API. Short answer: **Chronicling America holds none of the known FUN partner papers, and a search of its OCR for 1914-1923 turns up no FUN grid puzzle.** What it does hold that bears on the series is advertising for the Sunday World in The Evening World (below). Tool: `tools/chronam.py`.

## The API (current, 2026)

- Everything lives at loc.gov. The old `chroniclingamerica.loc.gov/search/pages/results/?...&format=json` and `/lccn/<lccn>.json` answer **308** and redirect to `www.loc.gov/chroniclingamerica/...`; use the collection endpoint instead.
- **Search pages by OCR phrase and date**:
  `https://www.loc.gov/collections/chronicling-america/?q="cross-word"&dates=1914/1924&fo=json&c=80&at=results,pagination`
  - `dates=YYYY/YYYY` or `YYYY-MM-DD/YYYY-MM-DD`; `c` = results per page (20/40/80/160; 160 returned 503s); `at=results,pagination` drops the 2 MB of facets; `sp=N` pages (`pagination.next` gives the next URL; a 404 means past the end); `sb=date` sorts by date.
  - **One title**: add `fa=number_lccn:sn83030193`. Without `q` it lists every page of the title in the range.
  - `q` is a token match: `"cross-word"` also matches the ordinary phrase "cross word", and `fun's` with an apostrophe returns 0 hits (the query itself fails, so use `fun`). Single word `crossword` is a different, much smaller set.
  - Reported hit counts (`pagination.of`) are approximate, and paging stops around the 2,000th result (the 26th page of 80), so run big queries a year at a time.
- **Each result** has `page_id` (`sn83030193-1914-09-22-ed-1-0655`), `date`, `number_lccn`, `partof_title`, `id` (page URL `https://www.loc.gov/resource/<lccn>/<date>/ed-<n>/?sp=<page>`) and `image_url`, a IIIF base.
- **Page image, full resolution**: `https://tile.loc.gov/image-services/iiif/service:ndnp:<awardee>:<batch>:data:<lccn>:<reel>:<issue>:<seq>/full/pct:100/0/default.jpg` (JPEG, ~5400x6300, 4-5 MB, 15 s). The original JP2 is faster (1 s): `https://tile.loc.gov/storage-services/service/ndnp/<awardee>/<batch>/data/<lccn>/<reel>/<issue>/<seq>.jp2`. The `.pdf` there is 403.
- **OCR text**: the ALTO file, same path with `.xml` (~0.9 MB, 0.3 s). The `.txt` at that path is 404. `chronam.py --ocr` turns ALTO into a `.txt`.
- **Rate limits**: the loc.gov documentation allows bulk use within limits (burst limit about 20 requests / 10 s; exceeding it brings HTTP 429 and a block of minutes). In practice the search endpoint is slow (35-50 s a page of 80) and returns occasional 503s; the tile and storage hosts are fast. The tool pauses 3 s between requests, retries 429/5xx with growing waits, and sends a User-Agent naming the project.

## Searches run

All with `at=results,pagination&fo=json`, harvested by paging.

| query (`q`) | `dates` | hits |
|---|---|---|
| `"cross-word"` | 1914/1924 | 2,098 reported, 2,000 retrieved (1,060 of them in 1924) |
| `"cross-word puzzle"` | 1914/1923 | 30 |
| `"cross word puzzle"` | 1914/1923 | 29 |
| `crossword` | 1914/1923 | 105 |
| `"cross-word puzzle solution"`, `"fun's cross-word puzzle"`, `"funs cross-word puzzle"` | 1914/1924 | 0 |
| `"cross-word puzzle" "weekly joke book"` | 1914/1924 | 1 (Evening World 1915-08-28) |
| `"cross-word puzzle" fun` | 1914/1919 | 3 (Evening World 1915-08-28; Rock Island Argus 1919-08-02, 12-06) |

## Hits by title, 1914-1923 (`"cross-word"`, pages)

Most of these are not puzzles. Reading the OCR of about twenty of them: the bulk are "never a cross word between us" fiction, the old children's riddle "Cross-Word Enigma" / "Crosswords" (a word-building rhyme, not a grid), and "My first is in Nevada" letter riddles headed CROSS WORD PUZZLE (Rock Island Argus 1919, Wilmington Evening Journal 1921). Counts show where to look, not how many puzzles exist.

| title | LCCN | hits | first | last |
|---|---|---|---|---|
| Birmingham Age-Herald | sn85038485 | 48 | 1914-03-03 | 1923-05-13 |
| Washington Times | sn84026749 | 26 | 1914-10-24 | 1923-12-31 |
| **The Evening World** | sn83030193 | 24 | 1914-09-22 | 1922-11-14 |
| Evening Star (Washington) | sn83045462 | 16 | 1915-12-15 | 1923-04-03 |
| El Paso Herald | sn88084272 | 16 | 1914-05-12 | 1920-09-18 |
| New-York Tribune | sn83030214 | 13 | 1914-06-21 | 1922-10-05 |
| Beatrice Daily Express | sn84020107 | 12 | 1914-01-08 | 1922-08-28 |
| Omaha Daily Bee | sn99021999 | 12 | 1916-03-02 | 1922-04-23 |
| Seattle Star | sn87093407 | 12 | 1914-05-28 | 1923-02-02 |
| Rock Island Argus (and Daily Union) | sn92053934, sn92053933 | 11 + 11 | 1914-10-14 | 1922-11-04 |
| Wilmington Evening Journal | sn85042354 | 11 | 1914-08-18 | 1922-08-21 |
| Washington Herald | sn83045433 | 10 | 1914-04-10 | 1921-03-02 |

(Many further titles have 3-9 hits; the full harvest is not kept in the repo. Re-run `chronam.py <lccn> 1914-01-01 1923-12-31 --q '"cross-word"'` for any title.)

### Known partners (papers.tsv)

**None are in Chronicling America**: Minneapolis Journal, Pittsburgh Press, Tacoma Daily Ledger, Boston Globe, LA Sunday Tribune, New Orleans States, Salt Lake Telegram, Shreveport Times, Fort Wayne Journal-Gazette, Seattle Post-Intelligencer. (The San Antonio Light, listed in papers.tsv as not yet searched, *is* here, sn85060004, but has only 3 hits, all 1923.) Not there either: the Los Angeles Evening Express, the Buffalo Courier-Express, and the New York Sunday World itself. (The Tacoma Times, sn88085187, is a different paper from the Tacoma Daily Ledger.) The Seattle Star (sn87093407) is a rival of the P-I, not a partner as far as we know.

### The Evening World (sn83030193)

Does it print the Sunday puzzle, its solution or the series number? **No.** Of its 24 `"cross-word"` hits, all but one are "cross word" in fiction (read in the OCR); the exception is the first item below. The `crossword` query adds the other two. All three are advertisements for the Sunday World:

- **1915-08-28 p.4** (Saturday), https://www.loc.gov/resource/sn83030193/1915-08-28/ed-1/?sp=4 : the Sunday World ad lists, under "FUN, the Great Weekly Joke Book", "'Dogs,' Steinigans. A Puzzle Letter and a Cross-Word Puzzle for the Children." Spot-checked in the OCR text. The earliest Evening World mention found, 20 months after the series began (1913-12-21).
- **1916-08-25 p.6** (Friday), https://www.loc.gov/resource/sn83030193/1916-08-25/ed-1/?sp=6 : "Puzzles in cross-words and rebus form and snappy jokes in the Fun Book."
- **1919-07-31 p.14** (Thursday), https://www.loc.gov/resource/sn83030193/1919-07-31/ed-1/?sp=14 : "The World Magazine's famous cross-word Puzzles are always in demand" (in the Sunday World Magazine ad). Dated evidence that the puzzle ran in 1919, under the Magazine name.

These help establish that the series existed and ran through 1919 in the Sunday World (and what it was called there), but give no grid, solution or number. More such ads probably exist but would need a different search (e.g. `fun "joke book"`, `"sunday world"` + `puzzle`) to gather.

### Papers new to the record

Nothing found that carries FUN. Four candidates for a cross-word that is *not* FUN, for orientation only: the Birmingham Age-Herald's weekly **"Cross-Word Corner"** (Sundays 1922-11-19 on, verified grid-style column with "solution to last week's cross-word puzzle", constructor credits from readers; https://www.loc.gov/resource/sn85038485/1922-11-19/ed-1/?sp=56), a similar weekly in the Washington Tribune (1921-10 to 1923-07), a daily cluster of 1921-03-03 to 03-12 in the Washington Herald, South Bend News-Times and Ardmoreite (not read), and the New-York Tribune's Sunday children's page with "Cross-Word Enigma" (1914, a rhyme riddle, not a grid).

## The three needs

1. **January 1914 (World Nos. 3-6)**: Chronicling America cannot supply them. No hit for `"cross-word"` before 1914-03 is a puzzle; I read the Topeka State Journal (1914-01-01), Beatrice Daily Express (01-08), Delta Independent (02-20) and Atlanta Georgian (02-22), all "never a cross word". The New-York Tribune's Sunday "Cross-Word Enigma" (1914-01-04 p.34, 01-25 p.32) is a riddle. The one source worth trying is the Evening World's Saturday ads of 1913-12 to 1914-01 for the Sunday World's FUN (no puzzle, but a date check for the series start).
2. **Dated FUN puzzles in 1918-1923**: none. The Evening World ad of 1919-07-31 says the puzzles ran; no partner paper that reprinted them is digitized here. The 1918-23 titles with repeated hits (table above) are noise or other series.
3. **LA Evening Express, Buffalo Courier-Express**: not in Chronicling America. (The California Digital Newspaper Collection, cdnc.ucr.edu, holds the Los Angeles Evening Express's own run and may be worth a separate look; not tried here.)

## Using the tool

```
python tools/chronam.py sn83030193 1915-08-28 1915-08-28 --q '"cross-word puzzle"'        # list
python tools/chronam.py sn83030193 1915-08-01 1915-08-31 --issues                          # issue dates
python tools/chronam.py sn83030193 1915-08-28 1915-08-28 --q '"cross-word puzzle"' --ocr DIR   # OCR text
python tools/chronam.py <LCCN> <FROM> <TO> [--q PHRASE] --fetch <folder>                   # images + pages.tsv
```

`--fetch` writes `<Paper>_<YYYY>_<MM>_<DD>_<page>.jpg` and `pages.tsv` (file, issue, date, page, url, captured, note); existing files are skipped so a run can be resumed. Tested on one page (Evening World 1915-08-28 p.4, 4 MB). A full year of a daily without `--q` is ~5,000 pages, so give a phrase or a short range.
