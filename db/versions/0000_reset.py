from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    query = """
        DROP TABLE if exists public."EURUSD" cascade;
        DROP TABLE if exists public.market_data cascade;
        DROP TABLE if exists public.category;
        DROP TABLE if exists public.signals;
        DROP TABLE if exists public.tickers;
        """
    op.execute(query)

def downgrade():
    query = """
        DROP TABLE if exists public."EURUSD" cascade;
        DROP TABLE if exists public.market_data cascade;
        DROP TABLE if exists public.category;
        DROP TABLE if exists public.signals;
        DROP TABLE if exists public.tickers;
        """
    op.execute(query)
