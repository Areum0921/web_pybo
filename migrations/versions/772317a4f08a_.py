"""empty message

Revision ID: 772317a4f08a
Revises: 51267fecac8f
Create Date: 2021-05-05 12:07:12.554520

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '772317a4f08a'
down_revision = '51267fecac8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint('fk_question_category_name_category', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_question_category_name_category', 'category', ['category_name'], ['name'], ondelete='CASCADE')

    op.create_table('category',
    sa.Column('name', sa.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('name', name='pk_category'),
    sa.UniqueConstraint('name', name='uq_category_name')
    )
    # ### end Alembic commands ###
