#!/usr/bin/env python3
"""List and fetch Chronicling America (Library of Congress) newspaper pages through the loc.gov JSON API.

  chronam.py LCCN FROM TO [--q PHRASE] [--tsv]        list matching pages: date, page, title, URL
  chronam.py LCCN FROM TO [--q PHRASE] --fetch DIR    also download each page image (full resolution
                                                      JPEG) into DIR and write DIR/pages.tsv in the
                                                      folder-source format of ../newyorkworld-scans
  chronam.py LCCN FROM TO [--q PHRASE] --ocr DIR      save each page's OCR text (.txt, from the ALTO file) as well
  chronam.py LCCN FROM TO --issues                    list the issue dates only (no search phrase needed)

LCCN is the Library of Congress control number of a title (sn83030193 = The Evening World); FROM and TO
are YYYY-MM-DD. Without --q every page of the date range is listed (a year of a daily is ~5,000 pages, so
narrow the range or give a phrase). Pages are listed in date order and --limit N stops after N.
Method and findings: docs/CHRONAM.md.

Be polite: loc.gov throttles bursts (HTTP 429 means stop for a while) and often answers 503 when busy.
Requests pause --pause seconds (default 3), retry with growing waits, and send a User-Agent naming the project.
Existing files in DIR are skipped, so an interrupted fetch can be re-run.
"""
import argparse
import csv
import datetime as dt
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UA = "EveryPuzzleProject-newyorkworld/0.1 (https://github.com/EveryPuzzleProject; adejarnatt@gmail.com)"
SEARCH = "https://www.loc.gov/collections/chronicling-america/"
PAGES_COLS = ["file", "issue", "date", "page", "url", "captured", "note"]

_last = [0.0]


def request(url: str, pause: float, timeout: int = 170) -> bytes:
    """GET with a pause since the last request, a User-Agent, and retries on 429/5xx and dropped connections."""
    for attempt in range(5):
        wait = _last[0] + pause - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout) as r:
                data = r.read()
            _last[0] = time.time()
            return data
        except urllib.error.HTTPError as e:
            _last[0] = time.time()
            if e.code == 404:
                raise
            delay = 60 * (attempt + 1) if e.code == 429 else 10 * (attempt + 1)
            print(f"  HTTP {e.code} for {url[:100]}; waiting {delay}s", file=sys.stderr)
            time.sleep(delay)
        except (urllib.error.URLError, http.client.HTTPException, TimeoutError, ConnectionError, OSError) as e:
            _last[0] = time.time()
            print(f"  {e!r}; waiting {10 * (attempt + 1)}s", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    raise SystemExit(f"giving up on {url}")


def search_url(lccn: str, start: str, end: str, q: str | None, per_page: int) -> str:
    params = {"dates": f"{start}/{end}", "fo": "json", "c": per_page, "at": "results,pagination",
              "fa": f"number_lccn:{lccn}", "sb": "date"}
    if q:
        params["q"] = q
    return SEARCH + "?" + urllib.parse.urlencode(params)


def pages(lccn: str, start: str, end: str, q: str | None, pause: float, per_page: int = 80):
    """Yield one dict per page: lccn, date, page (sequence number), title, url, image (IIIF base), ocr (txt URL)."""
    url = search_url(lccn, start, end, q, per_page)
    while url:
        try:
            d = json.loads(request(url, pause))
        except urllib.error.HTTPError as e:
            if e.code == 404:  # loc.gov answers 404 for a page past the last
                return
            raise
        for r in d.get("results", []):
            if (r.get("number_lccn") or [""])[0] != lccn:
                continue
            m = re.match(r"sn\d+-(\d{4}-\d\d-\d\d)-ed-(\d+)-(\d+)$", r.get("page_id") or "")
            if not m:
                continue
            res = (r.get("resource") or {}).get("url") or r.get("id", "")
            seq = re.search(r"[?&]sp=(\d+)", r.get("id", ""))
            iiif = next((u for u in r.get("image_url", []) if "/iiif/" in u), "")
            base = iiif.split("/full/")[0] if iiif else ""
            yield {
                "lccn": lccn, "date": m.group(1), "edition": int(m.group(2)),
                "page": int(seq.group(1)) if seq else int(m.group(3)),
                "title": (r.get("partof_title") or [""])[0],
                "url": (r.get("id") or "").split("&q=")[0].replace("http://", "https://"),
                "image": base + "/full/pct:100/0/default.jpg" if base else "",
                "ocr": ocr_url(base),
            }
        url = (d.get("pagination") or {}).get("next")


def ocr_url(iiif_base: str) -> str:
    """IIIF id service:ndnp:nbu:batch_X:data:sn123:reel:issue:seq -> .../storage-services/service/ndnp/nbu/batch_X/data/sn123/reel/issue/seq.xml
    (the page's ALTO OCR; the .txt next to it is a 404, the .jp2 is the original scan)"""
    if "/iiif/" not in iiif_base:
        return ""
    ident = urllib.parse.unquote(iiif_base.split("/iiif/", 1)[1])
    return "https://tile.loc.gov/storage-services/" + ident.replace(":", "/") + ".xml"


def alto_text(xml: bytes) -> str:
    """Plain text of an ALTO file, one line per TextLine."""
    lines = []
    for el in ET.fromstring(xml).iter():
        if el.tag.rsplit("}", 1)[-1] == "TextLine":
            lines.append(" ".join(s.get("CONTENT", "") for s in el if s.tag.rsplit("}", 1)[-1] == "String"))
    return "\n".join(lines) + "\n"


def slug(title: str) -> str:
    """'The Evening world (New York, N.Y.), 1887-1931' -> 'The_Evening_World'"""
    t = re.sub(r"\s*\(.*", "", title).strip()
    return "_".join(w.capitalize() if w.islower() else w for w in re.sub(r"[^A-Za-z0-9 ]", "", t).split())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lccn")
    ap.add_argument("start")
    ap.add_argument("end")
    ap.add_argument("--q", help="phrase to search the page OCR for, e.g. '\"cross-word\"'")
    ap.add_argument("--fetch", metavar="DIR", help="download page images into DIR and write DIR/pages.tsv")
    ap.add_argument("--ocr", metavar="DIR", help="download page OCR text into DIR")
    ap.add_argument("--issues", action="store_true", help="list issue dates, one per line")
    ap.add_argument("--tsv", action="store_true", help="list as tab-separated values")
    ap.add_argument("--limit", type=int, default=0, help="stop after N pages")
    ap.add_argument("--pause", type=float, default=3.0, help="seconds between requests (default 3)")
    a = ap.parse_args()
    for d in (a.start, a.end):
        dt.date.fromisoformat(d)

    found = []
    for p in pages(a.lccn, a.start, a.end, a.q, a.pause):
        found.append(p)
        if a.limit and len(found) >= a.limit:
            break
    found.sort(key=lambda p: (p["date"], p["page"]))

    if a.issues:
        for d in sorted({p["date"] for p in found}):
            print(d)
        return
    for p in found:
        print("\t".join([p["date"], str(p["page"]), p["title"], p["url"]]) if a.tsv
              else f"{p['date']}  p.{p['page']:<3} {p['title'][:48]:<48} {p['url']}")
    print(f"{len(found)} pages", file=sys.stderr)

    if a.fetch:
        out = Path(a.fetch)
        out.mkdir(parents=True, exist_ok=True)
        tsv = out / "pages.tsv"
        rows = {}
        if tsv.exists():
            with open(tsv, newline="", encoding="utf-8") as f:
                rows = {r["file"]: r for r in csv.DictReader(f, delimiter="\t")}
        today = dt.date.today().isoformat()
        for p in found:
            name = f"{slug(p['title'])}_{p['date'].replace('-', '_')}_{p['page']}.jpg"
            if not (out / name).exists():
                (out / name).write_bytes(request(p["image"], a.pause))
                print("fetched", name, file=sys.stderr)
            rows[name] = {"file": name, "issue": f"{slug(p['title']).lower().replace('_', '-')}-{p['date']}",
                          "date": p["date"], "page": p["page"], "url": p["url"], "captured": today,
                          "note": "Chronicling America, Library of Congress"}
        with open(tsv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, PAGES_COLS, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(sorted(rows.values(), key=lambda r: (r["date"], int(r["page"]))))
    if a.ocr:
        out = Path(a.ocr)
        out.mkdir(parents=True, exist_ok=True)
        for p in found:
            name = f"{slug(p['title'])}_{p['date'].replace('-', '_')}_{p['page']}.txt"
            if not (out / name).exists():
                (out / name).write_text(alto_text(request(p["ocr"], a.pause)), encoding="utf-8")
                print("fetched", name, file=sys.stderr)


if __name__ == "__main__":
    main()
