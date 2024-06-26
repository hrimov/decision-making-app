"""Initial

Revision ID: 563a3bad61c9
Revises: 
Create Date: 2023-12-09 20:00:32.160164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '563a3bad61c9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('problem_states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_problem_states'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('photo_path', sa.String(), nullable=True),
    sa.Column('reputation', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_table('problems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('private', sa.Boolean(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], name=op.f('fk_problems_creator_id_users')),
    sa.ForeignKeyConstraint(['state_id'], ['problem_states.id'], name=op.f('fk_problems_state_id_problem_states')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_problems'))
    )
    op.create_table('problem_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], name=op.f('fk_problem_members_problem_id_problems')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_problem_members_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_problem_members'))
    )
    op.create_table('problem_statements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('content_path', sa.String(), nullable=True),
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], name=op.f('fk_problem_statements_problem_id_problems')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_problem_statements'))
    )
    op.create_table('suggestion_stages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('ended_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], name=op.f('fk_suggestion_stages_problem_id_problems')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_suggestion_stages'))
    )
    op.create_table('voting_stages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('ended_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], name=op.f('fk_voting_stages_problem_id_problems')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_voting_stages'))
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=100), nullable=False),
    sa.Column('posted', sa.DateTime(timezone=True), nullable=False),
    sa.Column('problem_member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['problem_member_id'], ['problem_members.id'], name=op.f('fk_comments_problem_member_id_problem_members')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comments'))
    )
    op.create_table('problem_statement_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('problem_statement_id', sa.Integer(), nullable=False),
    sa.Column('parent_comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['problem_statement_comments.id'], name=op.f('fk_problem_statement_comments_parent_comment_id_problem_statement_comments')),
    sa.ForeignKeyConstraint(['problem_statement_id'], ['problem_statements.id'], name=op.f('fk_problem_statement_comments_problem_statement_id_problem_statements')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_problem_statement_comments'))
    )
    op.create_table('suggestions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('content_path', sa.String(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['problem_members.id'], name=op.f('fk_suggestions_creator_id_problem_members')),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], name=op.f('fk_suggestions_problem_id_problems')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_suggestions'))
    )
    op.create_table('results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.Column('suggestion_id', sa.Integer(), nullable=False),
    sa.Column('decision', sa.String(), nullable=False),
    sa.Column('content_path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['suggestion_id'], ['suggestions.id'], name=op.f('fk_results_suggestion_id_suggestions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_results'))
    )
    op.create_table('suggestion_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('suggestion_id', sa.Integer(), nullable=False),
    sa.Column('parent_comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['suggestion_comments.id'], name=op.f('fk_suggestion_comments_parent_comment_id_suggestion_comments')),
    sa.ForeignKeyConstraint(['suggestion_id'], ['suggestions.id'], name=op.f('fk_suggestion_comments_suggestion_id_suggestions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_suggestion_comments'))
    )
    op.create_table('suggestion_votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('voter_id', sa.Integer(), nullable=False),
    sa.Column('suggestion_id', sa.Integer(), nullable=False),
    sa.Column('voting_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['suggestion_id'], ['suggestions.id'], name=op.f('fk_suggestion_votes_suggestion_id_suggestions')),
    sa.ForeignKeyConstraint(['voter_id'], ['problem_members.id'], name=op.f('fk_suggestion_votes_voter_id_problem_members')),
    sa.ForeignKeyConstraint(['voting_id'], ['voting_stages.id'], name=op.f('fk_suggestion_votes_voting_id_voting_stages')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_suggestion_votes'))
    )
    op.create_table('result_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('result_id', sa.Integer(), nullable=False),
    sa.Column('parent_comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['result_comments.id'], name=op.f('fk_result_comments_parent_comment_id_result_comments')),
    sa.ForeignKeyConstraint(['result_id'], ['results.id'], name=op.f('fk_result_comments_result_id_results')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_result_comments'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result_comments')
    op.drop_table('suggestion_votes')
    op.drop_table('suggestion_comments')
    op.drop_table('results')
    op.drop_table('suggestions')
    op.drop_table('problem_statement_comments')
    op.drop_table('comments')
    op.drop_table('voting_stages')
    op.drop_table('suggestion_stages')
    op.drop_table('problem_statements')
    op.drop_table('problem_members')
    op.drop_table('problems')
    op.drop_table('users')
    op.drop_table('problem_states')
    # ### end Alembic commands ###
