"""0008_add_images_table

Revision ID: 9868c224d768
Revises: 609a46ee73ec
Create Date: 2024-08-28 13:53:18.640219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9868c224d768'
down_revision: Union[str, None] = '609a46ee73ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('publication_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['publication_id'], ['publications.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('publications', 'images')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publications', sa.Column('images', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=False))
    op.drop_table('publication_images')
    # ### end Alembic commands ###