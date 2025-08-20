import yfinance as yf
import pandas as pd
from pathlib import Path

OUT = Path("data/raw")
OUT.mkdir(parents=True, exist_ok=True)
df = yf.download("AAPL", start="2020-01-01", auto_adjust=False, progress=False)
df = df.reset_index()
flat_cols = []
for c in df.columns:
    if isinstance(c, tuple):
        c = "_".join(str(x) for x in c if x)
    else:
        c = str(c)
    c = c.strip().lower().replace(" ", "_")
    flat_cols.append(c)
df.columns = flat_cols
if "ticker" not in df.columns:
    df.insert(1, "ticker", "AAPL")

out_path = OUT / "AAPL.csv"
df.to_csv(out_path, index=False)
print("Saved:", out_path)
print(df.head(3))
