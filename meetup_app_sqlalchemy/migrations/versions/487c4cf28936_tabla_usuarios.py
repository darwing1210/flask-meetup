"""Tabla usuarios

Revision ID: 487c4cf28936
Revises: 
Create Date: 2019-10-24 23:01:47.480249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '487c4cf28936'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=64), nullable=True),
    sa.Column('apellido', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('rol', sa.String(length=64), nullable=True),
    sa.Column('lugar', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuario_email'), 'usuario', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_usuario_email'), table_name='usuario')
    op.drop_table('usuario')
    # ### end Alembic commands ###
