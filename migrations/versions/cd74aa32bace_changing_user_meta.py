"""Changing USer meta

Revision ID: cd74aa32bace
Revises: c6a5ea2945ad
Create Date: 2025-02-15 16:14:51.605406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'cd74aa32bace'
down_revision: Union[str, None] = 'c6a5ea2945ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'first_name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###
