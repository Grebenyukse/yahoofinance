import yfinance as yf
import datetime as datetime


def load(ticker= 'MSFT', startTime='2022-01-01'):
    data = yf.download(  # or pdr.get_data_yahoo(...
        tickers = ticker,
            # List of tickers to download
        # period : str
            # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # Either Use period parameter or use start and end
        interval='1h',
            # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # Intraday data cannot extend last 60 days
        start= startTime,
            # Download start date string (YYYY-MM-DD) or _datetime.
            # Default is 1900-01-01
        end= datetime.datetime.now().strftime("%Y-%m-%d"),
            # Download end date string (YYYY-MM-DD) or _datetime.
            # Default is now
        group_by='ticker',
            # Group by 'ticker' or 'column' (default)
        prepost=False,
            # Include Pre and Post market data in results?
            # Default is False
        # auto_adjust: bool
            # Adjust all OHLC automatically? Default is False
        # actions: bool
            # Download dividend + stock splits data. Default is False
        # threads: bool / int
            # How many threads to use for mass downloading. Default is True
        # proxy: str
            # Optional. Proxy server URL scheme. Default is None
        # rounding: bool
            # Optional. Round values to 2 decimal places?
        # show_errors: bool
            # Optional. Doesn't print errors if True
        # timeout: None or float
            # If not None stops waiting for a response after given number of
            # seconds. (Can also be a fraction of a second e.g. 0.01)
    )
    return data
