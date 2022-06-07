import pandas as pd
from config import engine


def save_signals(signals):
    signals.to_sql('signals', engine, if_exists='append', index=False)


def read_signals():
    query = """
        SELECT * from "signals" where published = 0
    """
    sql_query = pd.read_sql_query(query, engine)
    if sql_query.empty:
        return sql_query
    sql_query['messages'] = sql_query.agg(lambda x: 'Ticker=https://finance.yahoo.com/chart/' + x['Ticker']
                                                    + ' Extremum Datetime=' + str(x['Datetime'])
                                                    + ' Expert=' + x['Expert']
                                                    + ' Trend=' + str(x['Trend'])
                                                    + ' Description=' + x['Description'], axis=1)
    messages = sql_query[['signals_id', 'messages', 'Ticker', 'Expert']]
    # унификация публикуемых сообщений
    return messages


def mark_as_published(signal_id):
    with engine.begin() as conn:
        query = f"""
        UPDATE "signals" 
        set published = 1 
        where signals_id = {signal_id}
    """
        result = conn.execute(query)
        print(result.rowcount, "Record updated successfully into Signals")


def get_saved_signals(signal):
    trend = signal['Trend']
    datetime = signal['Datetime']
    ticker = signal['Ticker']
    criteria = signal['Criteria']
    expert = signal['Expert']
    with engine.begin() as conn:
        query = f"""
            select count(*) from "signals" 
            where "Trend" = '{trend}'
                and "Ticker" = '{ticker}'
                and DATE_PART('day', "signals"."Datetime"::timestamp - '{datetime}'::timestamp) < 1
                and "Criteria" = '{criteria}'
                and "Expert" = '{expert}'
        """
        result = conn.execute(query)
        count = result.fetchone()[0]
        return count
