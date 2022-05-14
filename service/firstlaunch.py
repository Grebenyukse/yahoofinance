
from dao.setupschema import clear_schema, setup_schema
from files.get_tickers import load_tickers


def first_launch():
    clear_schema()
    setup_schema()
    load_tickers()