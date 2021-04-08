"""empty message

Revision ID: 5496eea3137d
Revises: cb2d168fd653
Create Date: 2021-03-29 14:28:48.432364

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '5496eea3137d'
down_revision = 'cb2d168fd653'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_answer')
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), server_default='1', nullable=True))
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.create_foreign_key(batch_op.f('fk_question_user_id_user'), 'user', ['user_id'], ['id'], ondelete='CASCADE')

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
        batch_op.drop_constraint(batch_op.f('fk_question_user_id_user'), type_='foreignkey')
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_column('user_id')

    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    op.create_table('_alembic_tmp_answer',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('question_id', sa.INTEGER(), nullable=True),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('create_date', sa.DATETIME(), nullable=False),
    sa.Column('ip', sa.VARCHAR(length=50), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
