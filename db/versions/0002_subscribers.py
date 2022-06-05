from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    query = f"""
        CREATE TABLE public.subscribers (
        id serial not null primary key,
        chat_id bigint NOT NULL unique,
        user_id bigint NOT NULL unique,
        name text NULL,
        surname text NULL,
        username text NOT NULL)
        """
    op.execute(query)

def downgrade():
    query = """
        DROP TABLE if exists public.subscribers cascade;
        """
    op.execute(query)
