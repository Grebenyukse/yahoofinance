import schedule
import time

from service.marketdata import update_market_info
from service.signals import update_signals, publish_alerts

# schedule.every().hour.do(update_market_info)
# schedule.every().hour.do(update_signals)
# schedule.every().hour.do(publish_alerts)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)

# print('start update market info')
# update_market_info()
# print('start update signals')
# update_signals()
print('start sending alerts')
publish_alerts()
print('finish mf')
