import pandas as pd


def get_chunked_tickers():
    data = pd.read_excel(io="C:\\Users\\admin\\PycharmProjects\\yahoofinance\\tickers.xlsx",
                         sheet_name=0,
                         header=0,
                         na_filter=True,
                         index_col=None,
                         usecols="A:A")
    test_list = data['Ticker'].tolist()
    chunk_size = 10
    output = [test_list[i:i + chunk_size] for i in range(0, len(test_list), chunk_size)]
    tickers = list(map(lambda item: ' '.join(str(x) for x in item), output))
    return tickers