"""Other Tables

Revision ID: c615132d0bb0
Revises: e6b0d836b7c9
Create Date: 2021-02-02 17:45:06.914088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c615132d0bb0'
down_revision = 'e6b0d836b7c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('question_text', sa.String(length=500), nullable=True),
    sa.Column('a', sa.String(length=250), nullable=True),
    sa.Column('b', sa.String(length=250), nullable=True),
    sa.Column('c', sa.String(length=250), nullable=True),
    sa.Column('d', sa.String(length=250), nullable=True),
    sa.Column('e', sa.String(length=250), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.Column('point', sa.Integer(), nullable=True),
    sa.Column('true_answer', sa.String(length=1), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_exams',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_answers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('answer', sa.String(length=1), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_answers')
    op.drop_table('users_exams')
    op.drop_table('question')
    # ### end Alembic commands ###
