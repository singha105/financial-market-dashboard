import yfinance as yf
import pandas as pd
from pathlib import Path

TICKERS = ["AAPL", "MSFT", "AMZN", "JPM"]
OUT = Path("data/raw"); OUT.mkdir(parents=True, exist_ok=True)

df = yf.download(TICKERS, start="2020-01-01", auto_adjust=False, progress=False)
if isinstance(df.columns, pd.MultiIndex):
    lvl0 = set(map(str, df.columns.get_level_values(0).unique()))
    if any(t in lvl0 for t in TICKERS):
        tidy = df.stack(level=0).reset_index().rename(columns={'level_1':'ticker'})
    else:
        tidy = df.stack(level=1).reset_index().rename(columns={'level_1':'ticker'})
else:
    df = df.reset_index(); tidy = df.copy(); tidy["ticker"] = TICKERS[0]

tidy.columns = [str(c).strip().lower().replace(" ", "_") for c in tidy.columns]
wanted = ["date","ticker","open","high","low","close","adj_close","volume"]
tidy = tidy[[c for c in wanted if c in tidy.columns]].sort_values(["ticker","date"]).reset_index(drop=True)

(combined := OUT / "prices_all.csv")
tidy.to_csv(combined, index=False)
print(f"Saved combined: {combined} ({len(tidy)} rows)")

for t in TICKERS:
    tidy[tidy["ticker"] == t].to_csv(OUT / f"{t}.csv", index=False)
print("Saved per-ticker CSVs to", OUT)
print(tidy.head())
