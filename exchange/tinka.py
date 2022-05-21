import logging
import os
from datetime import timedelta
from pathlib import Path
import pandas as pd
import numpy as np

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.caching.cache_settings import MarketDataCacheSettings
from tinkoff.invest.services import MarketDataCache
from tinkoff.invest.utils import now

TOKEN = "t.eDmKGfqdXmwDFW9279RZc3xhYLKpuu8IP7HNhMtvU7FgQ4gIu7fAhSArpOyrNGcIImz_aW_qDgcEbryMk34I-Q"
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)


def main():
    with Client(TOKEN) as client:
        r = client.instruments.shares()
        shares_info = []
        for s in r.instruments:
            shares_info.append((s.ticker, s.figi, s.currency, s.class_code, s.lot, s.exchange, s.name, s.real_exchange))

        f = client.instruments.futures()
        for f in f.instruments:
            shares_info.append((f.ticker, f.figi, f.currency, f.class_code, f.lot, f.exchange, f.name, f.real_exchange))
    
        df = pd.DataFrame(shares_info, columns=['Ticker', 'Figi', 'Currency','Class', 'Lot', 'Exchange', 'Name', 'Real_exchange'])
        df.to_csv("tinka_tickers2.csv", sep=";")
        print('oleg')
    return 0


if __name__ == "__main__":
    main()