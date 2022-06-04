
from dao.tickers import get_ticker_names
from files.get_tickers import load_tickers
import alembic.config
alembicArgs = [
    '--raiseerr',
    'upgrade', 'head',
]
alembic.config.main(argv=alembicArgs)


def first_launch():
    alembic.config.main(argv=alembicArgs)
    if get_ticker_names().empty:
        load_tickers()
    else:
        print('skip load tickers')