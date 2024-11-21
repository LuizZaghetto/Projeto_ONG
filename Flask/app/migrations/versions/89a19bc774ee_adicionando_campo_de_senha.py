"""Adicionando campo de senha

Revision ID: 89a19bc774ee
Revises: 87eca19e7410
Create Date: 2024-11-20 22:14:00.064584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89a19bc774ee'
down_revision = '87eca19e7410'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ong', schema=None) as batch_op:
        batch_op.add_column(sa.Column('senha_hash', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ong', schema=None) as batch_op:
        batch_op.drop_column('senha_hash')

    # ### end Alembic commands ###
