"""empty message

Revision ID: 85c8058a5515
Revises: c58e5c9833d8
Create Date: 2023-08-28 14:43:32.995640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85c8058a5515'
down_revision = 'c58e5c9833d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Subjects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Suggest', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Subjects', schema=None) as batch_op:
        batch_op.drop_column('Suggest')

    # ### end Alembic commands ###
