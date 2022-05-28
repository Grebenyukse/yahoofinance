from dao.marketdata import get_last_loaded_date, update_market_data
from exchange.yahoo import load
from service.tickers import get_chunked_tickers
from datetime import date, timedelta, datetime

DEFAULT_START_DATE = '2022-01-01'


# Обновляем информацию по всем символам
def update_market_info():
	tickers = get_chunked_tickers()
	# tickers =['MSFT AAPL']
	for tickets in tickers:
		ticketList = tickets.split(' ')
		lastUpdatedDate = get_last_loaded_date(ticketList)
		if lastUpdatedDate is None:
			startDate = DEFAULT_START_DATE
		else:
			yesterday = date.today() - timedelta(days=1)
			startDate = min(lastUpdatedDate.date(), yesterday).strftime("%Y-%m-%d")
		prices = load(tickets, startDate)
		update_market_data(prices)
