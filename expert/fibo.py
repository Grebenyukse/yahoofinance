import pandas as pd

from plot.plot import plot_candlesticks


def get_fibo_signals(data):
    tickerData = data.head(100)
    if len(tickerData.index) < 20:
        return None
    supremum_bar = tickerData['High'].idxmax()
    supremum = tickerData['High'].max()
    infimum_bar = tickerData['Low'].idxmin()
    infimum = tickerData['Low'].min()
    trend = 1 if supremum_bar > infimum_bar else -1
    fibo_382 = None
    fibo_618 = None
    range_size = supremum - infimum
    if trend == 1:
        fibo_382 = infimum + 0.618 * range_size
        fibo_618 = infimum + 0.382 * range_size
    else:
        fibo_618 = infimum + 0.618 * range_size
        fibo_382 = infimum + 0.382 * range_size
    isbroken_382 = False
    isbroken_618 = False
    last_extremum = int(min(supremum_bar, infimum_bar))

    touches_382 = 0
    touches_681 = 0
    sigma = range_size * 0.03  # погрешность определения сигнала 3%
    alpha = range_size * 0.01  # погрешность определения пробоя 1%

    # check fibo levels is broken
    for i in range(0, last_extremum):
        if trend == 1:
            if tickerData.iloc[i]['Low'] < fibo_382 - alpha:
                isbroken_382 = True
            if tickerData.iloc[i]['Low'] < fibo_618 - alpha:
                isbroken_618 = True
        if trend == -1:
            if tickerData.iloc[i]['High'] > fibo_382 + alpha:
                isbroken_382 = True
            if tickerData.iloc[i]['High'] > fibo_618 + alpha:
                isbroken_618 = True
        # count touches

        j = 0
        while j < last_extremum:
            if trend == 1:
                if tickerData.iloc[j]['Low'] - fibo_382 < sigma:
                    touches_382 += 1
                    j += 2
                if tickerData.iloc[j]['Low'] - fibo_618 < sigma:
                    touches_681 += 1
                    j += 2
            if trend == -1:
                if fibo_382 - tickerData.iloc[j]['High'] < sigma:
                    touches_382 += 1
                    j += 2
                if fibo_618 - tickerData.iloc[j]['High'] < sigma:
                    touches_681 += 1
                    j += 2
            j += 1

    columns = ['Ticker', 'Datetime', 'Expert', 'Trend', 'Criteria', 'Description']
    if (not isbroken_382 and touches_382 >= 2) or (not isbroken_618 and touches_681 >= 2) or True:
        data['fibo_382'] = data['Close'].agg(lambda x: fibo_382)
        data['fibo_618'] = data['Close'].agg(lambda x: fibo_618)
        plot_candlesticks(data)
    if not isbroken_382 and touches_382 >= 2:
        return pd.DataFrame(data=[[tickerData.iloc[0]['Ticker'],
                                   tickerData.iloc[last_extremum]['Datetime'],
                                   'Fibbo touch 38.2',
                                   trend,
                                   touches_382,
                                   'touches_382=' + str(touches_382)]],
                            columns=columns)
    if not isbroken_618 and touches_681 >= 2:
        return pd.DataFrame(data=[[tickerData.iloc[0]['Ticker'],
                                   tickerData.iloc[last_extremum]['Datetime'],
                                   'Fibo touch 61.8',
                                   trend,
                                   touches_681,
                                   'touches_681=' + str(touches_681)]],
                            columns=columns)
    return None
