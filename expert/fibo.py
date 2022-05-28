import pandas as pd

from plot.render import plot_candlesticks, plot_test


def get_fibo_signals(data, render=False):
    tickerData = data.head(100)
    if len(tickerData.index) < 20:
        return None
    supremum_bar = tickerData['High'].idxmax()
    supremum = tickerData['High'].max()
    infimum_bar = tickerData['Low'].idxmin()
    infimum = tickerData['Low'].min()
    trend = 1 if supremum_bar < infimum_bar else -1
    fibo_382 = None
    fibo_618 = None
    range_size = supremum - infimum
    if trend == 1:
        fibo_382 = infimum + 0.382 * range_size
        fibo_618 = infimum + 0.618 * range_size
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
    markers_touples_382 = []
    markers_touples_618 = []
    # check fibo levels is broken
    for i in range(0, last_extremum):
        if trend == 1:
            if tickerData.iloc[i]['Low'] < fibo_382 - alpha:
                isbroken_382 = True
                markers_touples_382.append((i, tickerData.iloc[i]['Low'], 'black'))
            if tickerData.iloc[i]['Low'] < fibo_618 - alpha:
                isbroken_618 = True
                markers_touples_618.append((i, tickerData.iloc[i]['Low'], 'black'))
        if trend == -1:
            if tickerData.iloc[i]['High'] > fibo_382 + alpha:
                isbroken_382 = True
                markers_touples_382.append((i, tickerData.iloc[i]['High'], 'black'))
            if tickerData.iloc[i]['High'] > fibo_618 + alpha:
                isbroken_618 = True
                markers_touples_618.append((i, tickerData.iloc[i]['High'], 'black'))
        # count touches

        j = 0
        while j < last_extremum:
            if trend == 1:
                if tickerData.iloc[j]['Low'] - fibo_382 < sigma:
                    touches_382 += 1
                    j += 2
                    markers_touples_382.append((j, fibo_382, 'black'))
                if tickerData.iloc[j]['Low'] - fibo_618 < sigma:
                    touches_681 += 1
                    j += 2
                    markers_touples_618.append((j, fibo_618, 'black'))
            if trend == -1:
                if fibo_382 - tickerData.iloc[j]['High'] < sigma:
                    touches_382 += 1
                    j += 2
                    markers_touples_382.append((j, fibo_382, 'black'))
                if fibo_618 - tickerData.iloc[j]['High'] < sigma:
                    touches_681 += 1
                    j += 2
                    markers_touples_618.append((j, fibo_618, 'black'))
            j += 1

    columns = ['Ticker', 'Datetime', 'Expert', 'Trend', 'Criteria', 'Description']
    result_df = None
    price_open = None
    stop_loss = supremum if trend == 1 else infimum
    take_profit = fibo_618
    markers = None
    if (not isbroken_382) and (touches_382 >= 2):
        markers = pd.DataFrame(columns=['x', 'y', 'color'], data=markers_touples_382)
        price_open = (stop_loss + fibo_382)/2
        result_df = pd.DataFrame(data=[[tickerData.iloc[0]['Ticker'],
                                   tickerData.iloc[last_extremum]['Datetime'],
                                   'Fibbo touch 38.2',
                                   trend,
                                   touches_382,
                                   'touches:' + str(touches_382) + '.' + get_position_info(price_open, take_profit, stop_loss)]],
                            columns=columns)
    if (not isbroken_618) and (touches_681 >= 2):
        markers = pd.DataFrame(columns=['x', 'y', 'color'], data=markers_touples_618)
        price_open = fibo_382
        result_df = pd.DataFrame(data=[[tickerData.iloc[0]['Ticker'],
                                   tickerData.iloc[last_extremum]['Datetime'],
                                   'Fibo touch 61.8',
                                   trend,
                                   touches_681,
                                   'touches:' + str(touches_681) + get_position_info(price_open, take_profit, stop_loss)]],
                            columns=columns)
    if render:
        if ((not isbroken_382) and (touches_382 >= 2)) or ((not isbroken_618) and (touches_681 >= 2)):
            left_e = max(supremum_bar, infimum_bar)
            right_e = min(supremum_bar, infimum_bar)
            fibo_xaxe = list(range(right_e, left_e))
            return (data, fibo_xaxe, fibo_382, fibo_618, markers, price_open, stop_loss, take_profit, infimum, supremum)
    return result_df


def get_position_info(price_open, take_profit, stop_loss):
    tp_to_sl = abs((price_open-take_profit)/(price_open-stop_loss))
    position_info = '\r\n PriceOpen:' + str(format(price_open, '.4f'))+ '. \r\n SL:' + str(format(stop_loss, '.4f')) + '. \r\n TP:' + str(format(take_profit, '.4f')) + '. \r\n Kprofit:' + str(format(tp_to_sl, '.2f'))
    return position_info