"""Add and modify company and usage

Revision ID: 3d89818c8ab3
Revises: 91badb9e7a3f
Create Date: 2024-11-19 16:48:28.751909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d89818c8ab3'
down_revision = '91badb9e7a3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.alter_column('postal_code',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.alter_column('postal_code',
               existing_type=sa.String(length=20),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
