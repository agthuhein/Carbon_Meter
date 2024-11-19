"""modify company model

Revision ID: 4835f5e470a4
Revises: 
Create Date: 2024-11-19 02:48:15.695354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4835f5e470a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('zip', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_column('zip')

    # ### end Alembic commands ###
