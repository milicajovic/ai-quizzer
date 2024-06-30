"""Initial migration

Revision ID: 84d7c47e9a55
Revises: 
Create Date: 2024-06-30 12:07:21.463487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84d7c47e9a55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('picture', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email'))
    )
    op.create_table('quiz',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_owner_id', sa.String(length=36), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_owner_id'], ['user.id'], name=op.f('fk_quiz_user_owner_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_quiz'))
    )
    op.create_table('page_scan',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('quiz_id', sa.String(length=36), nullable=True),
    sa.Column('page_position', sa.Integer(), nullable=True),
    sa.Column('file_name', sa.String(length=255), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], name=op.f('fk_page_scan_quiz_id_quiz')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_page_scan'))
    )
    op.create_table('prep_session',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('quiz_id', sa.String(length=36), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], name=op.f('fk_prep_session_quiz_id_quiz')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_prep_session_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_prep_session'))
    )
    op.create_table('question',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('quiz_id', sa.String(length=36), nullable=True),
    sa.Column('page_scan_id', sa.String(length=36), nullable=True),
    sa.Column('question_text', sa.String(length=1000), nullable=True),
    sa.Column('answer', sa.String(length=1000), nullable=True),
    sa.Column('difficulty_level', sa.Integer(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['page_scan_id'], ['page_scan.id'], name=op.f('fk_question_page_scan_id_page_scan')),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], name=op.f('fk_question_quiz_id_quiz')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_question'))
    )
    op.create_table('answer',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('question_id', sa.String(length=36), nullable=True),
    sa.Column('prep_session_id', sa.String(length=36), nullable=True),
    sa.Column('answer_text', sa.String(length=1000), nullable=True),
    sa.Column('audio_file_name', sa.String(length=255), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('feedback', sa.String(length=1000), nullable=True),
    sa.Column('correctness', sa.Float(), nullable=True),
    sa.Column('completeness', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['prep_session_id'], ['prep_session.id'], name=op.f('fk_answer_prep_session_id_prep_session')),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_answer_question_id_question')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_answer_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_answer'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.drop_table('question')
    op.drop_table('prep_session')
    op.drop_table('page_scan')
    op.drop_table('quiz')
    op.drop_table('user')
    # ### end Alembic commands ###
