"""0001_create_db

Revision ID: 4686660bff65
Revises: 
Create Date: 2024-08-30 13:18:56.106235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4686660bff65'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=20), nullable=False),
    sa.Column('model', sa.String(length=20), nullable=False),
    sa.Column('generation', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('url', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('added_time', sa.DateTime(), nullable=False),
    sa.Column('car_model_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_model_id'], ['car_models.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.Column('publication_date', sa.DateTime(), nullable=False),
    sa.Column('link', sa.String(length=75), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('engine_type', sa.String(length=50), nullable=False),
    sa.Column('engine_hp', sa.String(length=10), nullable=False),
    sa.Column('engine_volume', sa.String(length=10), nullable=True),
    sa.Column('transmission_type', sa.String(length=10), nullable=False),
    sa.Column('car_drive', sa.String(length=20), nullable=False),
    sa.Column('mileage', sa.String(length=10), nullable=False),
    sa.Column('car_year', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('car_model_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_model_id'], ['car_models.id'], ),
    sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('link')
    )
    op.create_table('publication_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['publication_id'], ['publications.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publication_prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('price_date', sa.DateTime(), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['publication_id'], ['publications.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_favorites',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('favorite_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['favorite_id'], ['favorites.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'favorite_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_favorites')
    op.drop_table('publication_prices')
    op.drop_table('publication_images')
    op.drop_table('publications')
    op.drop_table('favorites')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('sites')
    op.drop_table('car_models')
    # ### end Alembic commands ###