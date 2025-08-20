import os, numpy as np, pandas as pd, matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path

# read DB creds
load_dotenv()
engine = create_engine(
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST','localhost')}:{os.getenv('MYSQL_PORT','3306')}/{os.getenv('MYSQL_DB','StockDB')}"
)

# pull AAPL series
df = pd.read_sql_query(text("""
  SELECT date, adj_close FROM stock_prices
  WHERE ticker='AAPL' ORDER BY date
"""), engine, parse_dates=['date']).set_index('date')

# moving averages
df['ma50'] = df['adj_close'].rolling(50).mean()
df['ma200'] = df['adj_close'].rolling(200).mean()

# drawdown = price / running_max - 1
df['drawdown'] = df['adj_close'] / df['adj_close'].cummax() - 1

# plot with drawdown shading
fig_path = Path("reports/figures/aapl_ma_drawdown.png")
fig_path.parent.mkdir(parents=True, exist_ok=True)
ax = df[['adj_close','ma50','ma200']].plot(figsize=(8,4),
                                           title='AAPL Adj Close with 50D/200D MA + Drawdown Shading')
ax.set_ylabel('USD'); ax.grid(True)
ax.legend(['Adj Close (USD)','50D MA','200D MA'])

dd_mask = (df['drawdown'] < -0.20).values  # shade worse than -20%
ax.fill_between(df.index, ax.get_ylim()[0], ax.get_ylim()[1], where=dd_mask, alpha=0.12, step='mid')

plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
print("Saved figure:", fig_path)

# headline stats
ret_total = df['adj_close'].iloc[-1] / df['adj_close'].iloc[0] - 1
years = (df.index[-1] - df.index[0]).days / 365.25
cagr = (1 + ret_total)**(1/years) - 1
daily = df['adj_close'].pct_change().dropna()
ann_vol = daily.std() * np.sqrt(252)
max_dd = df['drawdown'].min()

stats_path = Path("reports/figures/aapl_headline_stats.txt")
stats_path.write_text(
    f"Total return: {ret_total:.2%}\n"
    f"CAGR: {cagr:.2%}\n"
    f"Annualized volatility: {ann_vol:.2%}\n"
    f"Max drawdown: {max_dd:.2%}\n"
)
print("Saved stats:", stats_path)

