import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
pio.renderers
pio.renderers.default = "notebook_connected"

def plot_candlesticks(df, fibo_xaxe, fibo_382, fibo_618, markers, names=('Datetime', 'Open', 'High', 'Low', 'Close')):
    stocks = df.copy()
    Datetime, Open, High, Low, Close = names

    candle = go.Figure(data=[go.Candlestick(x=stocks.index, name='Trade',
                                            open=stocks[Open],
                                            high=stocks[High],
                                            low=stocks[Low],
                                            close=stocks[Close]), ])
    candle.add_trace(go.Line(name=fibo_382,
                             x=fibo_xaxe,
                             y=np.repeat(fibo_382, len(fibo_xaxe)),
                             line=dict(color='red', width=2)))

    candle.add_trace(go.Line(name=fibo_618,
                            x=fibo_xaxe,
                            y=np.repeat(fibo_618, len(fibo_xaxe)),
                            line=dict(color='blue', width=2)))
    if not markers.empty:
        for index, m in markers:
            candle.add_trace(
                go.Scatter(
                    mode='markers',
                    x=[m['x']],
                    y=[m['y']],
                    marker=dict(
                        color=m['color'],
                        size=3,
                        line=dict(
                            color='MediumPurple',
                            width=1
                        )
                    ),
                    showlegend=False
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
    candle.update_xaxes(autorange="reversed")
    candle.show()


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