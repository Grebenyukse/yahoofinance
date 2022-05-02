import pandas as pd

from dao.config import engine


def remove_duplicates_signals():
    with engine.begin() as conn:
        query = """
            with cte AS
            (
            SELECT data_id,
                   row_number() OVER (PARTITION BY t."Datetime",
                                                   t."Ticker"
                                      ORDER BY t."Ticker") rn
                   FROM "signals" t
            )
            DELETE FROM "signals" t2
                   USING cte
                   WHERE cte.rn > 1
                         AND cte.data_id = t2.data_id;
        """
        result = conn.execute(query)
        print(result.rowcount, "Record updated successfully into EURUSD")


def save_signals(signals):
    signals.to_sql('signals', engine, if_exists='append', index=False)


def read_signals():
    query = """
        SELECT * from "signals" where published = 0
    """
    sql_query = pd.read_sql_query(query, engine)
    df = pd.DataFrame(sql_query, columns=['Ticker', 'Datetime', 'Expert',
                                          'Trend', 'Criteria', 'Description', 'signals_id'])
    messages = pd.DataFrame(data=[df.agg(lambda x: 'Ticker=' + x['Ticker']
                                                   + ' Datetime=' + str(x['Datetime'])
                                                   + ' Expert=' + x['Expert']
                                                   + ' Trend=' + str(x['Trend'])
                                                   + ' Description=' + x['Description'], axis=1).T, df['signals_id']],
                            columns=['messages', 'signals_id'])
    # унификация публикуемых сообщений

    return messages
