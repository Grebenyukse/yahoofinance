import pandas as pd
from exchange.yahoo import load

tickers = pd.DataFrame(data=['MSFT'], columns=['Ticker'])
print('oleg')

prices = load('MSFT')
print('ivan')