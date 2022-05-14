import yfinance as yf


def load(ticker):
    data = yf.download(  # or pdr.get_data_yahoo(...
        tickers=ticker,
        period="20d",
        interval="1h",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None,
    )
    return data
