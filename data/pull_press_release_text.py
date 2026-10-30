"""INFO 367 Group 4: download the press release text (Exhibit 99.1) for each row in earnings_events.csv.

No API keys needed. Put YOUR OWN name and email in USER_AGENT first. The SEC asks for this.
Needs: pip install pandas beautifulsoup4, and earnings_events.csv from pull_earnings_data.py.
Run:  python3 pull_press_release_text.py          (add a number to test, e.g. python3 pull_press_release_text.py 10)
Out:  press_releases_raw.csv  (accession, ticker, found, words, text)
Nothing is cut short here. We decide the cut rule as a group later and write it in the provenance statement.
"""
import sys, json, re, time, subprocess
import pandas as pd
from bs4 import BeautifulSoup

USER_AGENT = "Your Name you@example.com"   # change this to your own name and email

def sec_get(url):
    time.sleep(0.2)                              # stays under 10 requests a second
    return subprocess.run(["curl", "-s", "-L", "-H", f"User-Agent: {USER_AGENT}", url],
                          capture_output=True, text=True).stdout

def find_exhibit(cik, accession, main_doc=""):
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession.replace('-', '')}/"
    try:
        items = json.loads(sec_get(base + "index.json"))["directory"]["item"]
    except Exception:
        return None
    names = [i["name"] for i in items if i["name"].lower().endswith((".htm", ".html"))]
    for pat in (r"99[-_.]?1", r"ex[-_]?99", r"press"):
        for n in names:
            if re.search(pat, n.lower()):
                return base + n
    # fallback: any other page in the filing that is not the 8-K cover page, not an index, not a table file
    others = [n for n in names if "index" not in n.lower() and not re.match(r"R\d+\.htm", n) and n != main_doc]
    return base + others[0] if others else None

def clean(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style"]):
        t.decompose()
    return re.sub(r"\s+", " ", soup.get_text(" ")).strip()

def main():
    ev = pd.read_csv("earnings_events.csv")
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(ev)
    rows = []
    for e in ev.head(limit).itertuples():
        url = find_exhibit(e.cik, e.accession, getattr(e, 'main_doc', ''))
        text = clean(sec_get(url)) if url else ""
        rows.append({"accession": e.accession, "ticker": e.ticker, "found": bool(url),
                     "words": len(text.split()), "url": url, "text": text})
        print(e.ticker, e.filing_date, "words:", len(text.split()))
    pd.DataFrame(rows).to_csv("press_releases_raw.csv", index=False)

if __name__ == "__main__":
    main()
