from datetime import datetime
import pandas as pd
from dao.marketdata import get_last_loaded_date
from exchange.yahoo import load
import datetime as datetime

from files.get_tickers import load_tickers
from service.marketdata import update_market_info

load_tickers()
print('oleg')

