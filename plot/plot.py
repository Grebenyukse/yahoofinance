import plotly.graph_objects as go
import plotly.io as pio
pio.renderers
pio.renderers.default = "notebook_connected"

def plot_candlesticks(df, names=('Datetime', 'Open', 'High', 'Low', 'Close', 'fibo_382', 'fibo_618')):
    stocks = df.copy()
    Datetime, Open, Close, Low, High, fibo_382, fibo_618 = names
    colors = ['red', 'blue', 'yellow']

    candle = go.Figure(data=[go.Candlestick(x=stocks[Datetime], name='Trade',
                                            open=stocks[Open],
                                            high=stocks[High],
                                            low=stocks[Low],
                                            close=stocks[Close]), ])
    candle.add_trace(go.Line(name=fibo_382,
                             x=stocks[Datetime],
                             y=stocks[fibo_382],
                             line=dict(color=colors[0], width=2)))
    candle.add_shape(
        type='line',
        x0=stocks[Datetime].min(),
        y0=fibo_382,
        x1=stocks[Datetime].max(),
        y1=fibo_382,
        line=dict(
            color='Red',
        )
    )
    candle.show()