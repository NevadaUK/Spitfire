"""Initial migration.

Revision ID: a6e4fafd1e6b
Revises: e684ba4cf03d
Create Date: 2021-02-27 12:15:37.851685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6e4fafd1e6b'
down_revision = 'e684ba4cf03d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'group', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'group_id')
    # ### end Alembic commands ###
