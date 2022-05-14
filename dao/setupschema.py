from dao.config import engine

def setup_schema():
    with engine.begin() as conn:
        query = f"""
        CREATE TABLE public."EURUSD" (
        "Datetime" timestamptz NULL,
        "Ticker" text NULL,
        "Adj Close" float8 NULL,
        "Close" float8 NULL,
        "High" float8 NULL,
        "Low" float8 NULL,
        "Open" float8 NULL,
        "Volume" float8 NULL,
        data_id serial4 NOT NULL,
        CONSTRAINT "EURUSD_pkey" PRIMARY KEY (data_id)
        );

        CREATE TABLE public.category (
        "name" varchar(255) NOT NULL,
        description varchar(255) NULL,
        CONSTRAINT category_pkey PRIMARY KEY (name)
        );

        CREATE TABLE public.signals (
        "Ticker" text NULL,
        "Datetime" timestamptz NULL,
        "Expert" text NULL,
        "Trend" int8 NULL,
        "Criteria" int8 NULL,
        "Description" text NULL,
        signals_id serial4 NOT NULL,
        published int4 NOT NULL DEFAULT 0,
        CONSTRAINT signals_pkey PRIMARY KEY (signals_id)
        );

        CREATE TABLE public.tickers (
        ticker varchar NOT NULL,
        country varchar NULL,
        exchange varchar NULL,
        category varchar NULL
        );
        """
        result = conn.execute(query)
        print(result.rowcount, "Record updated successfully into Signals")


def clear_schema():
    with engine.begin() as conn:
        query = """
        DROP TABLE if exists public."EURUSD" cascade;
        DROP TABLE if exists public.category;
        DROP TABLE if exists public.signals;
        DROP TABLE if exists public.tickers;
        """
        result = conn.execute(query)
        print(result.rowcount, "Record updated successfully into Signals")