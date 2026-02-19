"""rename formated_phone_number to formatted_phone_number

Revision ID: 8f3efdf3d839
Revises: cbe52a266999
Create Date: 2026-02-19 19:14:03.814152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f3efdf3d839'
down_revision = 'cbe52a266999'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'responses_clean', 
        'formated_phone_number',
        new_column_name='formatted_phone_number'
    )



def downgrade():
    op.alter_column(
        'responses_clean',
        'formatted_phone_number',
        new_column_name='formated_phone_number'
    )
