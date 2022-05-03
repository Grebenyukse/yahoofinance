from dao.marketdata import fetch_market_data_for_ticker
from dao.signals import save_signals, read_signals, mark_as_published, get_saved_signals
from dao.tickers import get_ticker_names
from exchange.telegram import send_alert
from expert.fibo import get_fibo_signals


# Загружаем информацию о тикете, проверяем сигнал, постим сигнал в таблицу
def update_signals():
    tickers = get_ticker_names()
    for ticker in tickers['Ticker']:
        data = fetch_market_data_for_ticker(ticker)
        signals = get_fibo_signals(data)
        if signals is None:
            continue
        signals['filter'] = signals[['Trend', 'Datetime', 'Ticker']]\
            .apply(lambda x: 1 if get_saved_signals(x) == 0 else None, axis=1)
        filtered_signals = signals.dropna(subset=['filter']).drop(labels=['filter'], axis=1)
        if not filtered_signals.empty:
            save_signals(filtered_signals)


# читаем сигнал, публикуем, помечаем как опубликованный
def publish_alerts():
    messages = read_signals()
    for index, x in messages.iterrows():
        send_alert(x['messages'])
        mark_as_published(x['signals_id'])

