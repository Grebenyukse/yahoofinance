from dao.marketdata import fetch_market_data_for_ticker
from dao.signals import save_signals, read_signals
from dao.tickers import get_ticker_names
from exchange.telegram import send_alert
from expert.fibo import get_fibo_signals


# Загружаем информацию о тикете, проверяем сигнал, постим сигнал в таблицу
def update_signals():
    tickers = get_ticker_names()
    for ticker in tickers['Ticker']:
        data = fetch_market_data_for_ticker(ticker)
        signal = get_fibo_signals(data)
        if signal is not None:
            save_signals(signal)


# читаем сигнал и публикуем
def publish_alerts():
    messages = read_signals()
    for message in messages:
        send_alert(message)
