from colorama import Style
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from config import project_path

pio.renderers
pio.renderers.default = "notebook_connected"

def plot_candlesticks(df, fibo_xaxe, fibo_382, fibo_618, markers, price_open, stop_loss, take_profit, infimum, supremum, names=('Datetime', 'Open', 'High', 'Low', 'Close')):
    stocks = df.head(400)
    Datetime, Open, High, Low, Close = names

    candle = go.Figure(data=[go.Candlestick(x=stocks.index, name=stocks.iloc[0]['Ticker'],
                                            open=stocks[Open],
                                            high=stocks[High],
                                            low=stocks[Low],
                                            close=stocks[Close]), ])
    candle.add_trace(go.Line(name='FIBO 38,2 ' + str(format(fibo_382, '.4f')),
                             x=fibo_xaxe,
                             y=np.repeat(fibo_382, len(fibo_xaxe)),
                             line=dict(color='red', width=2)))

    candle.add_trace(go.Line(name='FIBO 61,8 ' + str(format(fibo_618, '.4f')),
                            x=fibo_xaxe,
                            y=np.repeat(fibo_618, len(fibo_xaxe)),
                            line=dict(color='blue', width=2)))
    candle.add_trace(go.Line(name='Inf ' + str(format(infimum, '.4f')),
                            x=fibo_xaxe,
                            y=np.repeat(infimum, len(fibo_xaxe)),
                            line=dict(color='brown', width=1)))
    candle.add_trace(go.Line(name='Sup ' + str(format(supremum, '.4f')),
                            x=fibo_xaxe,
                            y=np.repeat(supremum, len(fibo_xaxe)),
                            line=dict(color='brown', width=1)))

    position_xaxe = list(range(0, fibo_xaxe[0]))

    candle.add_trace(go.Line(name='SL ' + str(format(stop_loss, '.4f')),
                        x=position_xaxe,
                        y=np.repeat(stop_loss, len(position_xaxe)),
                        line=dict(color='firebrick', width=2, dash='dash')))
    candle.add_trace(go.Line(name='TP ' + str(format(take_profit, '.4f')),
                        x=position_xaxe,
                        y=np.repeat(take_profit, len(position_xaxe)),
                        line=dict(color='lime', width=2, dash='dash')))
    candle.add_trace(go.Line(name='Price_open ' + str(format(price_open, '.4f')),
                        x=position_xaxe,
                        y=np.repeat(price_open, len(position_xaxe)),
                        line=dict(color='darkcyan', width=2, dash='dash')))

    if not markers.empty:
        for m in markers.index:
            candle.add_trace(
                go.Scatter(
                    mode='markers',
                    x=[markers.loc[m, 'x']],
                    y=[markers.loc[m, 'y']],
                    marker=dict(
                        color=markers.loc[m, 'color'],
                        size=6,
                        line=dict(
                            color='MediumPurple',
                            width=3
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
    candle.update_layout(xaxis_rangeslider_visible=False)
    candle.update_xaxes(autorange="reversed")
    # candle.show()
    candle.write_image(project_path + "yahoofinance\\plot\\images\\fig.jpeg")
    

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