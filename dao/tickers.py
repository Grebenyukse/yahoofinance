import plotly.io as pio
import pandas as pd

from dao.config import engine

pio.renderers.default = "browser"


def get_ticker_names():
    query = """
        select distinct "Yahoo" as "Ticker" from tickers
    """
    return pd.read_sql_query(query, engine)
