"""empty message

Revision ID: a57d9002619e
Revises: ff769a1bccb7
Create Date: 2019-04-11 20:01:06.842709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a57d9002619e'
down_revision = 'ff769a1bccb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grade', sa.Column('normal_timestamp', sa.String(), nullable=True))
    op.create_index(op.f('ix_grade_normal_timestamp'), 'grade', ['normal_timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_grade_normal_timestamp'), table_name='grade')
    op.drop_column('grade', 'normal_timestamp')
    # ### end Alembic commands ###