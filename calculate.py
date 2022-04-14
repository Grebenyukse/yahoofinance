import yfinance as yf
from connect import getConnection
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

pio.renderers.default = "browser"

engine = create_engine('postgresql://postgres:admin@localhost:5432/yahoo')


def load(tiker):
   
    sql_query = pd.read_sql_query('''
                                   SELECT
                                   *
                                   FROM "EURUSD"
                                   ''', engine)

    df = pd.DataFrame(sql_query, columns=['Datetime', 'Open', 'High', 'Low', 'Close'])
    
    print(df)
    fig = go.Figure(data=[go.Candlestick(x=df['Datetime'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    fig.show()


load('MSFT')

