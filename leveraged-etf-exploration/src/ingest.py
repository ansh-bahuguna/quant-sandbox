import os
from datetime import date
import pandas as pd
import yfinance as yf
import sqlite3


DB_PATH= "data/etf.db"
START_DATE = "2010-01-01"


#Leveraged & Inverse to rotate between
TICKERS_LEV = ["SPXL","SPXS","TQQQ","SQQQ"]

#Benchmark
TICKERS_BENCH = ["SPY"]
ALL = TICKERS_LEV + TICKERS_BENCH


def main():
    os.makedirs("data", exist_ok=True)


    #Create db and schema
    conn= sqlite3.connect(DB_PATH)
    with open("schema.sql", "r", encoding = "utf-8") as f:
        conn.executescript(f.read())
    conn.commit()

    #Insert Securities
    for s in ALL:
        conn.execute(
            "INSERT OR IGNORE INTO securities(symbol,name) VALUES (?,?)", (s,s)
        )
    conn.commit()


    #Download adjusted close+ volume
    df = yf.download(
        ALL, start = START_DATE , end = str(date.today()), auto_adjust = True, progress= False
    )

    if isinstance(df.columns, pd.MultiIdex):
        adj = df["Adj Close"].copy()
        vol = df["Volume"].copy()

    else:
        #fallback for single ticker
        adj = df["Adj Close"].to_frame(ALL[0])
        vol = df["Volume"].to_frame(ALL[0])


    adj = adj.ffill().dropna(how="all")
    vol = vol.reindex_like(adj).fillna(0)

    # long format
    adj_long = adj.reset_index().melt(id_vars="Date", var_name = "symbol",value_name= "adj_close")
    vol_long = vol.reset_index().melt(id_vars="Date",var_name="symbol", value_name="vol_close")
    data = adj_long.merge(vol_long, on=["Date","symbol"])
    data["date"] = data ["Date"].dt.strftime("%Y-%m-%d")


    rows = data[["symbol","date","adj_close", "volume"]].dropna().values.tolist()
    conn.executemany(
        "Insert OR REPLACE INTO prices(symbol,date,adj_close,volume) VALUES(?,??,?,?)",
        rows,
    )
    conn.commit()
    conn.close()
    print(f"Ingested rows: {len(rows)}")


if __name__ == "__main__":
    main()