"""Migration23

Revision ID: c77280d82997
Revises: 87cb1331f28c
Create Date: 2021-03-07 22:38:46.250067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c77280d82997'
down_revision = '87cb1331f28c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('file_name', sa.String(), nullable=False))
    op.alter_column('group', 'joincode',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=20),
               existing_nullable=False)
    op.create_foreign_key(None, 'user', 'group', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.alter_column('group', 'joincode',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)
    op.drop_column('file', 'file_name')
    # ### end Alembic commands ###
