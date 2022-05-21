import pandas as pd

from dao.tickers import get_ticker_names


def get_chunked_tickers():
    data = get_ticker_names()
    test_list = data['Ticker'].tolist()
    chunk_size = 100
    output = [test_list[i:i + chunk_size] for i in range(0, len(test_list), chunk_size)]
    tickers = list(map(lambda item: ' '.join(str(x) for x in item), output))
    return tickers
