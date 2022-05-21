import schedule
import time
from dao.setupschema import clear_schema, setup_schema
from files.get_tickers import load_tickers
from service.firstlaunch import first_launch

from service.marketdata import update_market_info
from service.signals import update_signals, publish_alerts

# schedule.every().hour.do(update_market_info)
# schedule.every().hour.do(update_signals)
# schedule.every().hour.do(publish_alerts)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)

first_launch()


print('start update market info')
update_market_info()
print('start update signals')
# update_signals()
print('start sending alerts')
publish_alerts()
print('finish mf')