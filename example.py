import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

data = yf.download("AAPL", start="2022-03-20", end="2022-04-01")
data = data.iloc[:,0:4]
data.reset_index(inplace=True)

def plot_candlesticks(df, names = ('Date','Open','High','Low','Close'), mv = [5,25,75]):
        stocks = df.copy()
        Date, Open, Close, Low, High = names
        stocks.sort_index(ascending=False, inplace = True)
        colors = ['red', 'blue', 'yellow']

        candle = go.Figure(data = [go.Candlestick(x = stocks[Date], name = 'Trade',
                                                       open = stocks[Open], 
                                                       high = stocks[High], 
                                                       low = stocks[Low], 
                                                       close = stocks[Close]),])
        for i in range(len(mv)):
            stocks[f'{str(mv[i])}-SMA'] = stocks[Close].rolling(mv[i], min_periods = 1).mean()
            candle.add_trace(go.Scatter(name=f'{str(mv[i])} MA',x=stocks[Date], y=stocks[f'{str(mv[i])}-SMA'], 
                                             line=dict(color=colors[i], width=2)))

      
        candle.show()

plot_candlesticks(data)