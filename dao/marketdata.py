from ast import Tuple
import pandas as pd

from dao.config import engine


def update_market_data(prices):
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


def fetch_market_data_for_ticker(ticker):
    try:
        query = f"""
        SELECT * FROM "EURUSD" t1 where t1."Ticker" = '{ticker}' 
        ORDER BY "Datetime" desc
        """
        sql_query = pd.read_sql_query(query, engine)
        df = pd.DataFrame(sql_query, columns=['Ticker', 'Datetime', 'Open', 'High', 'Low', 'Close'])
        return df
    except Exception as error:
        print("Failed to read list of tickers", error)

def get_last_loaded_date(tickerList):
    params = tuple(tickerList)
    with engine.begin() as conn:
        query = f"""
        select min(t2."Datetime") from  
            (SELECT "Ticker", max("Datetime") as "Datetime" from "EURUSD"
            where "Ticker" in {params}
            group by "Ticker") as t2
        group by t2."Datetime"
        """
        response = conn.execute(query, engine)
        row = response.fetchone()
        if row is None:
            return None
        result = row['min'] 
        return result
