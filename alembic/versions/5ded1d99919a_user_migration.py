"""User migration

Revision ID: 5ded1d99919a
Revises: 4c266fe5acc9
Create Date: 2024-01-30 16:47:50.204831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ded1d99919a'
down_revision = '4c266fe5acc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('birthdate')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.VARCHAR(), nullable=False))
        batch_op.add_column(sa.Column('birthdate', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###
