import os, pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path

# Load DB creds from .env
load_dotenv()
USER=os.getenv("MYSQL_USER"); PWD=os.getenv("MYSQL_PASSWORD")
HOST=os.getenv("MYSQL_HOST","localhost"); PORT=os.getenv("MYSQL_PORT","3306")
DB=os.getenv("MYSQL_DB","StockDB")

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

# Read the combined CSV from Day 2
csv_path = Path("data/raw/prices_all.csv")
df = pd.read_csv(csv_path, parse_dates=["date"])

# Ensure required columns exist
required = ["date","ticker","open","high","low","close","adj_close","volume"]
import os, pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
USER=os.getenv("MYSQL_USER"); PWD=os.getenv("MYSQL_PASSWORD")
HOST=os.getenv("MYSQL_HOST","localhost"); PORT=os.getenv("MYSQL_PORT","3306")
DB=os.getenv("MYSQL_DB","StockDB")

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

csv_path = Path("data/raw/prices_all.csv")
df = pd.read_csv(csv_path, parse_dates=["date"])

required = ["date","ticker","open","high","low","close","adj_close","volume"]
missing = set(required) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}")

df = df.drop_duplicates(subset=["ticker","date"])

df.to_sql("stock_prices", con=engine, if_exists="append", index=False)

with engine.connect() as c:
    total = c.execute(text("SELECT COUNT(*) FROM stock_prices")).scalar()
    print("Rows in stock_prices:", total)
