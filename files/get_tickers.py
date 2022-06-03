import pandas as pd

from config import engine
from config import project_path


def load_tickers():
    data = pd.read_excel(io=project_path + "yahoofinance\\files\\tinka_tickers.xlsx",
                         sheet_name=0,
                         header=0,
                         na_filter=True,
                         index_col=None,
                         usecols="K:K")
    data.dropna(subset="Yahoo", inplace=True)
    data.to_sql('tickers', engine, if_exists='replace', index=False)