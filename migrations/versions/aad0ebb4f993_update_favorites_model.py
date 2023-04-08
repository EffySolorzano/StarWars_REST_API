"""update Favorites model

Revision ID: aad0ebb4f993
Revises: 9a83d4072cf1
Create Date: 2023-04-08 02:34:28.700085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aad0ebb4f993'
down_revision = '9a83d4072cf1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('people_name', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('planet_name', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('starship_model', sa.Integer(), nullable=True))
        batch_op.drop_constraint('favorites_user_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_planet_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_people_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_starship_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'planets', ['planet_name'], ['name'])
        batch_op.create_foreign_key(None, 'people', ['people_name'], ['name'])
        batch_op.create_foreign_key(None, 'user', ['user_name'], ['name'])
        batch_op.create_foreign_key(None, 'starships', ['starship_model'], ['model'])
        batch_op.drop_column('planet_id')
        batch_op.drop_column('user_id')
        batch_op.drop_column('starship_id')
        batch_op.drop_column('people_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('starship_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorites_starship_id_fkey', 'starships', ['starship_id'], ['id'])
        batch_op.create_foreign_key('favorites_people_id_fkey', 'people', ['people_id'], ['id'])
        batch_op.create_foreign_key('favorites_planet_id_fkey', 'planets', ['planet_id'], ['id'])
        batch_op.create_foreign_key('favorites_user_id_fkey', 'user', ['user_id'], ['id'])
        batch_op.drop_column('starship_model')
        batch_op.drop_column('planet_name')
        batch_op.drop_column('people_name')
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###
