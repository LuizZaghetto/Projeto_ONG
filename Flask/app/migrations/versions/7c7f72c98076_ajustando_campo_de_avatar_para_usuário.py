"""Ajustando campo de avatar para usuário

Revision ID: 7c7f72c98076
Revises: 4e9ee9b56801
Create Date: 2024-12-03 17:12:09.806551

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7c7f72c98076'
down_revision = '4e9ee9b56801'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bicho', schema=None) as batch_op:
        batch_op.alter_column('sexo',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)

    with op.batch_alter_table('pessoa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_path', sa.String(length=150), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pessoa', schema=None) as batch_op:
        batch_op.drop_column('avatar_path')

    with op.batch_alter_table('bicho', schema=None) as batch_op:
        batch_op.alter_column('sexo',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)

    # ### end Alembic commands ###
