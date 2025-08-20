import os, pandas as pd, matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
ENGINE = create_engine(
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST','localhost')}:{os.getenv('MYSQL_PORT','3306')}/{os.getenv('MYSQL_DB','StockDB')}"
)

q = """
SELECT date, ticker, open, high, low, close, adj_close, volume
FROM stock_prices
WHERE ticker='AAPL'
ORDER BY date;
"""
df = pd.read_sql_query(sql=text(q), con=ENGINE, parse_dates=["date"])
print(df.head(10))
print("Row count:", len(df), "| Date range:", df["date"].min(), "→", df["date"].max())

df.plot(x="date", y="adj_close", title="AAPL Adj Close (from MySQL)")
plt.show()
