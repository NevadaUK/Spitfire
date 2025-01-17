"""Initial migration2324.

Revision ID: c9ee6c685126
Revises: 79a8412b3ea8
Create Date: 2021-03-07 22:17:29.427729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9ee6c685126'
down_revision = '79a8412b3ea8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'fileuploaded')
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
    op.add_column('file', sa.Column('fileuploaded', sa.VARCHAR(length=20), nullable=False))
    # ### end Alembic commands ###
