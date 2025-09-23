-- barebones schema
CREATE TABLE IF NOT EXISTS securities
(
    symbol TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS prices
(
    symbol TEXT,
    date TEXT, -- Year-Month-Date
    adj_close REAL,
    volume INTEGER,
    primary KEY(symbol, date)

);

CREATE TABLE IF NOT EXISTS factors
(
    symbol TEXT,
    date TEXT, 
    mom_12_1 REAL,  -- should be 12 month return excluding last month
    ma200 REAL,     -- 200 day moving average
    primary KEY(symbol,date)
);

CREATE TABLE IF NOT EXISTS signals
(
    date TEXT, -- month end signal date
    strategy TEXT, -- strategy chosen
    symbol TEXT, -- ETF choice
    weight REAL, -- 0 or 1
    PRIMARY key(date, strategy)
);

CREATE TABLE IF NOT EXISTS perf
(
    date TEXT,
    strategy TEXT,
    nav REAL, --cumulative portfolio value( start with 100)
    ret REAL, --daily return 
    drawdown REAL,
    PRIMARY KEY(date, strategy)

);
