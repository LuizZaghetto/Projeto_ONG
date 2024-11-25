"""Ajustando CPF

Revision ID: c8e4b3571348
Revises: f939153f179e
Create Date: 2024-11-25 17:15:02.499167

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c8e4b3571348'
down_revision = 'f939153f179e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pessoa', schema=None) as batch_op:
        batch_op.alter_column('CPF',
               existing_type=mysql.VARCHAR(length=15),
               type_=sa.String(length=14),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pessoa', schema=None) as batch_op:
        batch_op.alter_column('CPF',
               existing_type=sa.String(length=14),
               type_=mysql.VARCHAR(length=15),
               existing_nullable=False)

    # ### end Alembic commands ###
