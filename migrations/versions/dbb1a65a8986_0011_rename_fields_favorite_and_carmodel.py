"""0011_rename_fields_Favorite_and_CarModel

Revision ID: dbb1a65a8986
Revises: c7b2b206523a
Create Date: 2024-09-01 18:04:26.335160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbb1a65a8986'
down_revision: Union[str, None] = 'c7b2b206523a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorites', sa.Column('car_model_id', sa.Integer(), nullable=False))
    op.drop_constraint('favorites_model_id_fkey', 'favorites', type_='foreignkey')
    op.create_foreign_key(None, 'favorites', 'car_models', ['car_model_id'], ['id'])
    op.drop_column('favorites', 'model_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorites', sa.Column('model_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'favorites', type_='foreignkey')
    op.create_foreign_key('favorites_model_id_fkey', 'favorites', 'car_models', ['model_id'], ['id'])
    op.drop_column('favorites', 'car_model_id')
    # ### end Alembic commands ###
