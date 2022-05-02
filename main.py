from fibo import get_fibo_signals
from file_io import get_chunked_tickers
from dao import update_tickers_data, fetch_market_data_for_ticker, get_list_of_persisted_tickers, save_signals
from sqlalchemy import create_engine

path_to_storage = '/Users/18950416/PycharmProjects/QuantConnectStubs/data'
engine = create_engine('postgresql://postgres:admin@localhost:5432/yahoo')


def update_market_info():
    # Обновляем информацию по всем символам
    tickers = get_chunked_tickers()
    for tickets in tickers:
        update_tickers_data(tickets)


def update_signals():
    # Загружаем информацию о тикете, проверяем сигнал, постим сигнал в таблицу
    tickers = get_list_of_persisted_tickers()

    for ticker in tickers['Ticker']:
        data = fetch_market_data_for_ticker(ticker)
        signal = get_fibo_signals(data)
        if not None:
            save_signals(signal)


# update_market_info()
update_signals()
