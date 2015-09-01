"""Add registration tables

Revision ID: f9bb2a03ceb
Revises: 3fcf833adc2d
Create Date: 2015-09-01 16:21:03.682231
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from indico.core.db.sqlalchemy import UTCDateTime


# revision identifiers, used by Alembic.
revision = 'f9bb2a03ceb'
down_revision = '3fcf833adc2d'


def upgrade():
    op.create_table(
        'registration_forms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False, index=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('introduction', sa.Text(), nullable=False),
        sa.Column('start_dt', UTCDateTime, nullable=True),
        sa.Column('end_dt', UTCDateTime, nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('require_user', sa.Boolean(), nullable=False),
        sa.Column('registration_limit', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.events.id']),
        sa.PrimaryKeyConstraint('id'),
        schema='events'
    )

    op.create_table(
        'registration_form_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('registration_form_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['events.registration_form_items.id']),
        sa.ForeignKeyConstraint(['registration_form_id'], ['events.registration_forms.id']),
        sa.PrimaryKeyConstraint('id'),
        schema='events'
    )

    op.create_table(
        'registration_form_field_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('field_id', sa.Integer(), nullable=False),
        sa.Column('data', postgresql.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['field_id'], ['events.registration_form_items.id']),
        sa.PrimaryKeyConstraint('id'),
        schema='events'
    )

    op.create_table(
        'registrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('registration_form_id', sa.Integer(), nullable=False, index=True),
        sa.Column('user_id', sa.Integer(), nullable=True, index=True),
        sa.Column('submitted_dt', UTCDateTime, nullable=False),
        sa.ForeignKeyConstraint(['registration_form_id'], ['events.registration_forms.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.users.id']),
        sa.PrimaryKeyConstraint('id'),
        schema='events'
    )

    op.create_table(
        'registration_data',
        sa.Column('registration_id', sa.Integer(), nullable=False),
        sa.Column('field_data_id', sa.Integer(), nullable=False),
        sa.Column('data', postgresql.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['field_data_id'], ['events.registration_form_field_data.id']),
        sa.ForeignKeyConstraint(['registration_id'], ['events.registrations.id']),
        sa.PrimaryKeyConstraint('registration_id', 'field_data_id'),
        schema='events'
    )


def downgrade():
    op.drop_table('registration_data', schema='events')
    op.drop_table('registrations', schema='events')
    op.drop_table('registration_form_field_data', schema='events')
    op.drop_table('registration_form_items', schema='events')
    op.drop_table('registration_forms', schema='events')
