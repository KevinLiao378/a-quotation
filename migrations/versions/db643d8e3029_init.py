"""'init'

Revision ID: db643d8e3029
Revises: 
Create Date: 2020-12-17 15:03:36.834276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db643d8e3029'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_games_name'), 'games', ['name'], unique=True)
    op.create_table('heroes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_heroes_name'), 'heroes', ['name'], unique=True)
    op.create_table('quotations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=200), nullable=True),
    sa.Column('audio_url', sa.String(length=200), nullable=True),
    sa.Column('hero_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hero_id'], ['heroes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quotations')
    op.drop_index(op.f('ix_heroes_name'), table_name='heroes')
    op.drop_table('heroes')
    op.drop_index(op.f('ix_games_name'), table_name='games')
    op.drop_table('games')
    # ### end Alembic commands ###