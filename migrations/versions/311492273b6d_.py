"""empty message

Revision ID: 311492273b6d
Revises: 6e30accbfc49
Create Date: 2021-03-29 12:06:49.529934

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '311492273b6d'
down_revision = '6e30accbfc49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_user_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_username'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_user_email'), type_='unique')

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###
