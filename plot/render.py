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

    candle.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[16, 9], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )
    candle.show()
    # oleg


def plot_test(df, names=('Open', 'High', 'Low', 'Close')):
    stocks = df.copy()
    Open, High, Low, Close = names
    candle = go.Figure(data=[go.Candlestick(x=stocks.index, name='Trade',
                                            open=stocks[Open],
                                            high=stocks[High],
                                            low=stocks[Low],
                                            close=stocks[Close]), ])
    candle.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[16, 9], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )
    candle.show()