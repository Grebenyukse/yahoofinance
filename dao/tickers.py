import plotly.io as pio
import pandas as pd

from dao.config import engine

pio.renderers.default = "browser"


def get_ticker_names():
    query = """
        select distinct "Ticker" from Tickers
    """
    return pd.read_sql_query(query, engine)
