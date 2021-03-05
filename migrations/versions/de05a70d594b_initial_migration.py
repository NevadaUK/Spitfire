"""Initial migration.

Revision ID: de05a70d594b
Revises: 16a1a88302be
Create Date: 2021-02-28 14:15:04.680516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de05a70d594b'
down_revision = '16a1a88302be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'group', ['group_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
