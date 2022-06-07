import pandas as pd
import os

from dao.marketdata import fetch_market_data_for_ticker
from dao.signals import save_signals, read_signals, mark_as_published, get_saved_signals
from dao.tickers import get_ticker_names, get_ticker_names_micex
from exchange.telegram import send_photo
from exchange.yahoo import load_ticker_info
from expert.fibo import get_fibo_signals
from expert.gap import get_gap_signals
from plot import render
from plot.render import plot_candlesticks
from config import project_path

SCREENSHOT_PATH = project_path + "yahoofinance\\plot\\images\\fig.jpeg"


# Загружаем информацию о тикете, проверяем сигнал, постим сигнал в таблицу
def update_signals_fibo():
    tickers = get_ticker_names()
    # tickers = pd.DataFrame(data=['MSFT'], columns=['Ticker'])
    for ticker in tickers['Ticker']:
        data = fetch_market_data_for_ticker(ticker)
        signals = get_fibo_signals(data)
        if signals is None:
            continue
        signals['filter'] = signals[['Trend', 'Datetime', 'Ticker', 'Criteria', 'Expert']]\
            .apply(lambda x: 1 if get_saved_signals(x) == 0 else None, axis=1)
        filtered_signals = signals.dropna(subset=['filter']).drop(labels=['filter'], axis=1)
        if not filtered_signals.empty:
            print('save signals' + ticker)
            save_signals(filtered_signals)

def update_signals_gap():
    tickers = get_ticker_names_micex()
    for ticker in tickers['Ticker']:
        data = fetch_market_data_for_ticker(ticker)
        signals = get_gap_signals(data)
        if signals is None:
            continue
        signals['filter'] = signals[['Trend', 'Datetime', 'Ticker', 'Criteria', 'Expert']]\
            .apply(lambda x: 1 if get_saved_signals(x) == 0 else None, axis=1)
        filtered_signals = signals.dropna(subset=['filter']).drop(labels=['filter'], axis=1)
        if not filtered_signals.empty:
            print('save signals' + ticker)
            save_signals(filtered_signals)


# читаем сигнал, публикуем, помечаем как опубликованный
def publish_alerts():
    messages = read_signals()
    if messages.empty:
        return
    for index, x in messages.iterrows():
        market_data = fetch_market_data_for_ticker(x['Ticker'])
        render_data = None
        if x['Expert'] == 'Gap touch':
            render_data = get_gap_signals(market_data, True)
        if x['Expert'] == 'Fibo touch 38.2' or x['Expert'] == 'Fibo touch 61.8':
            render_data = get_fibo_signals(market_data, True)
        if render_data is None:
            break
        data, fibo_xaxe, fibo_382, fibo_618, markers, price_open, stop_loss, take_profit, infimum, supremum = render_data
        plot_candlesticks(data, fibo_xaxe, fibo_382, fibo_618, markers, price_open, stop_loss, take_profit, infimum, supremum)
        send_photo(SCREENSHOT_PATH, x['messages'], x['signals_id'])
        os.remove(SCREENSHOT_PATH)
        mark_as_published(x['signals_id'])


