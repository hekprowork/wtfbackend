"""empty message

Revision ID: 0158fc51f56a
Revises: 65056f85c992
Create Date: 2023-08-08 14:18:23.225437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0158fc51f56a'
down_revision = '65056f85c992'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('BaseWorks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('BaseWorkName', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('BaseWorks', schema=None) as batch_op:
        batch_op.drop_column('BaseWorkName')

    # ### end Alembic commands ###
