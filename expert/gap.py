from cmath import inf
import pandas as pd

from expert.fibo import get_position_info


def get_gap_signals(data, render=False):
    tickerData: pd.DataFrame = data.head(100)
    result_df = None
    if len(tickerData.index) < 20:
        return result_df
    print('check for gap in ' + tickerData.iloc[0]['Ticker'])
    
    range_size =  tickerData['High'].max() - tickerData['Low'].min()
    min_gap_size = range_size*0.1

    supremum = None
    infimum = None
    gap_bar = None
    markers_touples_infimum = []
    markers_touples_supremum = []
    for i in range(0, len(tickerData.index)-1):
        gap = tickerData.iloc[i]['Open'] - tickerData.iloc[i+1]['Close']
        if abs(gap) > min_gap_size:
            if gap > 0:
                supremum = tickerData.iloc[i]['Open']
                infimum = tickerData.iloc[i+1]['Close']
                trend = 1
            else:
                supremum = tickerData.iloc[i+1]['Close']
                infimum = tickerData.iloc[i]['Open']
                trend = -1
            gap_bar = i
            break
    if gap_bar == None:
        return result_df
    if gap_bar == 0:
        return result_df
    gap_is_broken = False
    sigma = range_size*0.03
    omega = range_size*0.01
    for j in range(0, gap_bar-1):
        if trend == -1:
            if tickerData.iloc[j]['High'] -  supremum > omega:
                gap_is_broken = True
                markers_touples_supremum.append((j, tickerData.iloc[j]['High'], 'black'))
        if trend == 1:
            if infimum - tickerData.iloc[j]['Low'] > omega:
                gap_is_broken = True
                markers_touples_infimum.append((j, tickerData.iloc[j]['Low'], 'black'))
    if gap_is_broken:
        return result_df
    supremum_touches = 0
    infimum_touches = 0
    k=0
    while k < gap_bar:
        if trend == -1:
            if supremum - tickerData.iloc[k]['High'] < sigma:
                supremum_touches +=1
                k +=2
                markers_touples_supremum.append((k, tickerData.iloc[k]['High'], 'black'))
        if trend == 1:
            if tickerData.iloc[k]['Low'] - infimum < sigma:
                infimum_touches +=1
                k+=2
                markers_touples_infimum.append((k, tickerData.iloc[k]['Low'], 'black'))
        k+=1
    columns = ['Ticker', 'Datetime', 'Expert', 'Trend', 'Criteria', 'Description']
    take_profit = None
    stop_loss = None
    price_open = None
    markers = None
    if supremum_touches > 1:
        take_profit = supremum
        stop_loss = infimum - min_gap_size
        price_open = infimum
        markers = pd.DataFrame(columns=['x', 'y', 'color'], data=markers_touples_supremum)
        result_df = pd.DataFrame(data=[[tickerData.iloc[0]['Ticker'],
                                   tickerData.iloc[gap_bar]['Datetime'],
                                   'Gap touch',
                                   trend,
                                   supremum_touches,
                                   'touches:' + str(supremum_touches) + '.' + get_position_info(price_open, take_profit, stop_loss)]],
                            columns=columns)
    if infimum_touches > 1:
        take_profit = infimum
        stop_loss = supremum + min_gap_size
        price_open = supremum
        markers =  pd.DataFrame(columns=['x', 'y', 'color'], data=markers_touples_infimum)
        result_df =  pd.DataFrame(data=[[tickerData.iloc[0]['Ticker'],
                                   tickerData.iloc[gap_bar]['Datetime'],
                                   'Gap touch',
                                   trend,
                                   infimum_touches,
                                   'touches:' + str(infimum_touches) + '.' + get_position_info(price_open, take_profit, stop_loss)]],
                            columns=columns)
    if render:
        if supremum_touches > 1 or infimum_touches > 1:
            fibo_xaxe = list(range(gap_bar, gap_bar+1))
            fibo_382=infimum
            fibo_618=supremum
            data=tickerData
            return (data, fibo_xaxe, fibo_382, fibo_618, markers, price_open, stop_loss, take_profit, infimum, supremum)
    return result_df
