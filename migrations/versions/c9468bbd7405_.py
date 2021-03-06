"""empty message

Revision ID: c9468bbd7405
Revises: 327b13989ec1
Create Date: 2021-03-30 10:14:00.234627

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'c9468bbd7405'
down_revision = '327b13989ec1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('modify_date', sa.DateTime(), nullable=True))

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('modify_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_column('modify_date')

    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_column('modify_date')

    # ### end Alembic commands ###
