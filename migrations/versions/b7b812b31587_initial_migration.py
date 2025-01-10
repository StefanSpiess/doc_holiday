"""Initial migration

Revision ID: b7b812b31587
Revises: 
Create Date: 2025-01-10 18:33:31.297813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7b812b31587'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('generic_object',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('employee_id', sa.String(length=50), nullable=False),
    sa.Column('zip_code', sa.String(length=10), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('street', sa.String(length=100), nullable=True),
    sa.Column('house_number', sa.String(length=10), nullable=True),
    sa.Column('concern_of', sa.String(length=50), nullable=True),
    sa.Column('is_emergency_contact', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('salary_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('salary', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact_information',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('mobile_number', sa.String(length=15), nullable=True),
    sa.Column('landline_number', sa.String(length=15), nullable=True),
    sa.Column('email_address', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['generic_object.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('related_object_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['related_object_id'], ['generic_object.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry')
    op.drop_table('contact_information')
    op.drop_table('salary_history')
    op.drop_table('generic_object')
    # ### end Alembic commands ###
