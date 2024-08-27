"""0006_edit_column_nullable

Revision ID: 6a1364962420
Revises: bb17c36d3c7a
Create Date: 2024-08-26 19:08:01.551544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a1364962420'
down_revision: Union[str, None] = 'bb17c36d3c7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('publications', 'engine_volume',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('publications', 'engine_volume',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    # ### end Alembic commands ###
