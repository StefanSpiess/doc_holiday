"""Add zip_code to Address

Revision ID: e57802b7066f
Revises: 
Create Date: 2025-01-10 16:49:41.374802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e57802b7066f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_information',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('mobile_number', sa.String(length=15), nullable=True),
    sa.Column('landline_number', sa.String(length=15), nullable=True),
    sa.Column('email_address', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('zip_code', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('street', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('house_number', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('concern_of', sa.String(length=50), nullable=True))
        batch_op.alter_column('employee_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.drop_column('address')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.VARCHAR(length=255), nullable=False))
        batch_op.alter_column('employee_id',
               existing_type=sa.String(length=50),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.drop_column('concern_of')
        batch_op.drop_column('house_number')
        batch_op.drop_column('street')
        batch_op.drop_column('city')
        batch_op.drop_column('zip_code')

    op.drop_table('contact_information')
    # ### end Alembic commands ###