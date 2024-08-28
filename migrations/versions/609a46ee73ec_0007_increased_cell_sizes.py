"""0007_increased_cell_sizes

Revision ID: 609a46ee73ec
Revises: 6a1364962420
Create Date: 2024-08-28 11:27:43.417774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '609a46ee73ec'
down_revision: Union[str, None] = '6a1364962420'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('car_models', 'generation',
               existing_type=sa.VARCHAR(length=25),
               type_=sa.String(length=30),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('car_models', 'generation',
               existing_type=sa.String(length=30),
               type_=sa.VARCHAR(length=25),
               existing_nullable=False)
    # ### end Alembic commands ###
