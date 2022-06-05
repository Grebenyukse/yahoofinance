import pandas as pd
from config import engine


def save_subscriber(subscriber):
    chat_id, user_id, name, surname, username = subscriber
    with engine.begin() as conn:
        query = f"""
        insert into subscribers (chat_id, user_id, name, surname, username)
        values ({chat_id}, {user_id}, '{name}', '{surname}', '{username}')
        on conflict (chat_id) do nothing;
    """
        result = conn.execute(query)
        print(result.rowcount, "Record updated successfully into subscribers")
    return result.rowcount

def fetch_subscribers():
    query = """
        SELECT chat_id from subscribers
    """
    sql_query = pd.read_sql_query(query, engine).dropna(subset=['chat_id'], inplace=False)
    if sql_query.empty:
        return list()
    return list(sql_query['chat_id'])

def unsubscribe(user_id):
    with engine.begin() as conn:
        query = f"""
        delete from subscribers s
        where s.user_id = {user_id}
    """
        result = conn.execute(query)
        print(result.rowcount, "Subscriber deleted successfully")
