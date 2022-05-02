from dao.marketdata import update_market_data
from exchange.yahoo import load
from service.tickers import get_chunked_tickers


# Обновляем информацию по всем символам
def update_market_info():
    tickers = get_chunked_tickers()
    for tickets in tickers:
        prices = load(tickets)
        update_market_data(prices)
