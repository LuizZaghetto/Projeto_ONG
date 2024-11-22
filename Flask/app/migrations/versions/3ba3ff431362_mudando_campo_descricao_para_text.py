"""Mudando campo descricao para text

Revision ID: 3ba3ff431362
Revises: 137426cd9d4b
Create Date: 2024-11-20 11:13:50.462753

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3ba3ff431362'
down_revision = '137426cd9d4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bicho', schema=None) as batch_op:
        batch_op.alter_column('descricao',
               existing_type=mysql.VARCHAR(length=500),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bicho', schema=None) as batch_op:
        batch_op.alter_column('descricao',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=500),
               existing_nullable=True)

    # ### end Alembic commands ###