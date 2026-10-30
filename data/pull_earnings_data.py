"""INFO 367 Group 4: pull earnings releases from the SEC and the stock move after each one.

No API keys needed. Everything here is free and public.
Before you run it, put YOUR OWN name and email in USER_AGENT. The SEC asks for this.

Run:  python3 pull_earnings_data.py
Needs: pip install pandas yfinance, and tickers.csv in the same folder.
Out:  earnings_events.csv  (one row per earnings release)
"""
import json, time, subprocess, datetime as dt
import pandas as pd
import yfinance as yf

USER_AGENT = "Your Name you@example.com"   # change this to your own name and email
TICKERS = pd.read_csv("tickers.csv").ticker.tolist()   # 110 S&P 500 companies, 10 per sector (random, seed 367)
SINCE = "2024-10-01"                              # only releases on or after this date
SEED_NOTE = "prices from yfinance, filings from SEC EDGAR"

def sec_get(url):
    # curl is used because some Macs fail python's https check. Stay under 10 requests a second.
    time.sleep(0.2)
    out = subprocess.run(["curl", "-s", "-H", f"User-Agent: {USER_AGENT}", url], capture_output=True, text=True)
    return out.stdout

def cik_map():
    j = json.loads(sec_get("https://www.sec.gov/files/company_tickers.json"))
    return {v["ticker"]: str(v["cik_str"]).zfill(10) for v in j.values()}

def earnings_filings(cik):
    j = json.loads(sec_get(f"https://data.sec.gov/submissions/CIK{cik}.json"))
    r = j["filings"]["recent"]
    rows = []
    for i, form in enumerate(r["form"]):
        if form == "8-K" and "2.02" in r["items"][i] and r["filingDate"][i] >= SINCE:
            rows.append({"accession": r["accessionNumber"][i], "filing_date": r["filingDate"][i],
                         "accepted_utc": r["acceptanceDateTime"][i], "main_doc": r["primaryDocument"][i]})
    return rows

def main():
    ciks = cik_map()
    events = []
    for t in TICKERS:
        if t not in ciks:
            print("no CIK for", t); continue
        for f in earnings_filings(ciks[t]):
            f.update({"ticker": t, "cik": ciks[t]}); events.append(f)
        print(t, "ok")
    ev = pd.DataFrame(events).drop_duplicates("accession")   # News Corp (NWS and NWSA) files one release for both share classes
    ev["accepted_et"] = pd.to_datetime(ev.accepted_utc, utc=True).dt.tz_convert("America/New_York")
    px = yf.download(TICKERS + ["SPY"], start="2024-09-15", end=str(dt.date.today()),
                     auto_adjust=False, progress=False)["Close"]
    px.index = px.index.tz_localize(None) if px.index.tz is None else px.index.tz_convert(None)
    days = list(px.index)
    out = []
    for _, e in ev.iterrows():
        d = pd.Timestamp(e.accepted_et.date()); hhmm = e.accepted_et.hour * 100 + e.accepted_et.minute
        after = [x for x in days if x > d]
        upto = [x for x in days if x <= d]
        if hhmm >= 1600:               # after the close: reaction is the next trading day
            base_day = upto[-1] if upto else None; react_day = after[0] if after else None; timing = "after close"
        elif hhmm < 930:               # before the open: same day, from yesterday's close
            before = [x for x in days if x < d]
            base_day = before[-1] if before else None; react_day = d if d in days else None; timing = "before open"
        else:                          # during the day: mixed, flag it
            before = [x for x in days if x < d]
            base_day = before[-1] if before else None; react_day = d if d in days else None; timing = "during day"
        if base_day is None or react_day is None or e.ticker not in px.columns:
            continue
        m = px.loc[react_day, e.ticker] / px.loc[base_day, e.ticker] - 1
        s = px.loc[react_day, "SPY"] / px.loc[base_day, "SPY"] - 1
        out.append({"ticker": e.ticker, "cik": e.cik, "accession": e.accession, "main_doc": e.main_doc, "filing_date": e.filing_date,
                    "accepted_et": e.accepted_et.strftime("%Y-%m-%d %H:%M"), "timing": timing,
                    "base_close_day": base_day.date(), "reaction_day": react_day.date(),
                    "stock_move_pct": round(m * 100, 2), "spy_move_pct": round(s * 100, 2),
                    "move_vs_spy_pct": round((m - s) * 100, 2)})
    pd.DataFrame(out).to_csv("earnings_events.csv", index=False)
    print("wrote earnings_events.csv with", len(out), "rows.", SEED_NOTE)

if __name__ == "__main__":
    main()
