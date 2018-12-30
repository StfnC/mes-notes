"""grades table

Revision ID: 0b0f3e134821
Revises: 63962361d0bc
Create Date: 2018-11-29 16:34:32.003191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b0f3e134821'
down_revision = '63962361d0bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_grade_mark'), 'grade', ['mark'], unique=False)
    op.create_index(op.f('ix_grade_timestamp'), 'grade', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_grade_timestamp'), table_name='grade')
    op.drop_index(op.f('ix_grade_mark'), table_name='grade')
    op.drop_table('grade')
    # ### end Alembic commands ###
