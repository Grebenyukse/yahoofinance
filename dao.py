import yfinance as yf

from sqlalchemy import create_engine
import plotly.io as pio
import pandas as pd

pio.renderers.default = "browser"
engine = create_engine('postgresql://postgres:admin@localhost:5432/yahoo')


def load(ticker):
    data = yf.download(  # or pdr.get_data_yahoo(...
        tickers=ticker,
        period="5d",
        interval="1h",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None,
    )
    return data


def update_tickers_data(tickers_joined):
    prices = load(tickers_joined)
    pr2 = prices.stack(0).reset_index()
    newCols = pr2.columns.get_level_values(0)
    newCols.values[1] = 'Ticker'
    newCols.values[0] = 'Datetime'
    pr2.columns = newCols
    pr3 = pr2.dropna(subset=['Close'])
    pr3.to_sql('EURUSD', engine, if_exists='append', index=False)
    remove_duplicates_market_data()


def remove_duplicates_market_data():
    with engine.begin() as conn:
        query = """
            with cte AS
            (
            SELECT data_id,
                   row_number() OVER (PARTITION BY t."Datetime",
                                                   t."Ticker"
                                      ORDER BY t."Ticker") rn
                   FROM "EURUSD" t
            )
            DELETE FROM "EURUSD" t2
                   USING cte
                   WHERE cte.rn > 1
                         AND cte.data_id = t2.data_id;
        """
        result = conn.execute(query)
        print(result.rowcount, "Record updated successfully into EURUSD")


def remove_duplicates_signals():
    with engine.begin() as conn:
        query = """
            with cte AS
            (
            SELECT data_id,
                   row_number() OVER (PARTITION BY t."Datetime",
                                                   t."Ticker"
                                      ORDER BY t."Ticker") rn
                   FROM "signals" t
            )
            DELETE FROM "signals" t2
                   USING cte
                   WHERE cte.rn > 1
                         AND cte.data_id = t2.data_id;
        """
        result = conn.execute(query)
        print(result.rowcount, "Record updated successfully into EURUSD")


def get_list_of_persisted_tickers():
    try:
        sql_query = pd.read_sql_query('''
                                           SELECT distinct
                                           "Ticker"
                                           FROM "EURUSD"
                                           ''', engine)
        df = pd.DataFrame(sql_query, columns=['Ticker'])
        return df
    except Exception as error:
        print("Failed to read list of tickers", error)


def fetch_market_data_for_ticker(ticker):
    try:
        query = f"""
        SELECT * FROM "EURUSD" t1 where t1."Ticker" = '{ticker}' 
        LIMIT 10000
        """
        sql_query = pd.read_sql_query(query, engine)
        df = pd.DataFrame(sql_query, columns=['Ticker', 'Datetime', 'Open', 'High', 'Low', 'Close'])
        return df
    except Exception as error:
        print("Failed to read list of tickers", error)


def save_signals(signals):
    signals.to_sql('signals', engine, if_exists='append', index=False)
