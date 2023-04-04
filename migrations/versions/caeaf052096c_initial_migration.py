"""Initial migration

Revision ID: caeaf052096c
Revises: 
Create Date: 2022-08-13 23:03:55.773538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'caeaf052096c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('communications',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('message', sa.String(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=False),
                    sa.Column('sender', sa.String(), nullable=False),
                    sa.Column('receiver', sa.String(), nullable=False),
                    sa.Column('is_queued', sa.Boolean(),
                              server_default='0', nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('flightschedules',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('creation_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.Column('upload_date', sa.DateTime(), nullable=True),
                    sa.Column('execution_time', sa.DateTime(), nullable=True),
                    sa.Column('status', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('housekeeping',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('satellite_mode', sa.String(
                        length=32), nullable=True),
                    sa.Column('battery_voltage', sa.Float(), nullable=True),
                    sa.Column('current_in', sa.Float(), nullable=True),
                    sa.Column('current_out', sa.Float(), nullable=True),
                    sa.Column('no_MCU_resets', sa.Integer(), nullable=True),
                    sa.Column('last_beacon_time',
                              sa.DateTime(), nullable=False),
                    sa.Column('tle', sa.String(length=256), nullable=True),
                    sa.Column('watchdog_1', sa.Integer(), nullable=True),
                    sa.Column('watchdog_2', sa.Integer(), nullable=True),
                    sa.Column('watchdog_3', sa.Integer(), nullable=True),
                    sa.Column('panel_1_current', sa.Float(), nullable=True),
                    sa.Column('panel_2_current', sa.Float(), nullable=True),
                    sa.Column('panel_3_current', sa.Float(), nullable=True),
                    sa.Column('panel_4_current', sa.Float(), nullable=True),
                    sa.Column('panel_5_current', sa.Float(), nullable=True),
                    sa.Column('panel_6_current', sa.Float(), nullable=True),
                    sa.Column('temp_1', sa.Float(), nullable=True),
                    sa.Column('temp_2', sa.Float(), nullable=True),
                    sa.Column('temp_3', sa.Float(), nullable=True),
                    sa.Column('temp_4', sa.Float(), nullable=True),
                    sa.Column('temp_5', sa.Float(), nullable=True),
                    sa.Column('temp_6', sa.Float(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('passovers',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('aos_timestamp', sa.DateTime(), nullable=True),
                    sa.Column('los_timestamp', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('telecommands',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('command_name', sa.String(
                        length=64), nullable=True),
                    sa.Column('num_arguments', sa.Integer(), nullable=True),
                    sa.Column('is_dangerous', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('username', sa.String(
                        length=128), nullable=True),
                    sa.Column('password_hash', sa.String(
                        length=128), nullable=True),
                    sa.Column('is_admin', sa.Boolean(),
                              server_default='0', nullable=False),
                    sa.Column('slack_id', sa.String(
                        length=128), nullable=True),
                    sa.Column('creator_id', sa.Integer(), nullable=True),
                    sa.Column('subscribed_to_slack', sa.Boolean(),
                              server_default='0', nullable=True),
                    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('slack_id'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('automatedcommands',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('command_id', sa.Integer(), nullable=False),
                    sa.Column('priority', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['command_id'], ['telecommands.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('blacklistedtokens',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('token', sa.String(length=256), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('flightschedulecommands',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('command_id', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.Column('flightschedule_id',
                              sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['command_id'], ['telecommands.id'], ),
                    sa.ForeignKeyConstraint(['flightschedule_id'], [
                        'flightschedules.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('powerchannels',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('hk_id', sa.Integer(), nullable=False),
                    sa.Column('channel_no', sa.Integer(), nullable=True),
                    sa.Column('enabled', sa.Boolean(), nullable=True),
                    sa.Column('current', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['hk_id'], ['housekeeping.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('automatedcommandsargs',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('index', sa.Integer(), nullable=True),
                    sa.Column('argument', sa.String(length=8), nullable=True),
                    sa.Column('automatedcommand_id',
                              sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['automatedcommand_id'], [
                        'automatedcommands.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('flightschedulecommandsargs',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('index', sa.Integer(), nullable=True),
                    sa.Column('argument', sa.String(length=8), nullable=True),
                    sa.Column('flightschedulecommand_id',
                              sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['flightschedulecommand_id'], [
                        'flightschedulecommands.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flightschedulecommandsargs')
    op.drop_table('automatedcommandsargs')
    op.drop_table('powerchannels')
    op.drop_table('flightschedulecommands')
    op.drop_table('blacklistedtokens')
    op.drop_table('automatedcommands')
    op.drop_table('users')
    op.drop_table('telecommands')
    op.drop_table('passovers')
    op.drop_table('housekeeping')
    op.drop_table('flightschedules')
    op.drop_table('communications')
    # ### end Alembic commands ###
