from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:admin@localhost:5432/yahoo')
