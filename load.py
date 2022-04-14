import yfinance as yf
from connect import getConnection
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

pio.renderers.default = "browser"

engine = create_engine('postgresql://postgres:admin@localhost:5432/yahoo')


def load(tiker):
    symb = yf.Ticker(tiker)
    # get stock info
    symb.info
    # get historical market data
    hist = symb.history()

    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers=tiker,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period="5d",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval="1h",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by='ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust=True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost=True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads=True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy=None,
    )

    # # show actions (dividends, splits)
    data.to_sql('EURUSD', engine, if_exists='replace', index=True)
    commonData = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Ticker'], index='Datetime')
    for i, j in data.iterrows():
        print(i)
        print(j)

sql_query = pd.read_sql_query('''
                                   SELECT
                                   ticker, exchange
                                   FROM "tickers"
                                   ''', engine)

ticketsPerExchange = sql_query.groupby(["exchange"]).agg(lambda x: ' '.join(x))


for name in ticketsPerExchange.index:
    tickets = ticketsPerExchange.loc[name].values[0]
    load(tickets)

load('MSFT')
