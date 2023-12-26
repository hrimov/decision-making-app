"""Add ProblemState values

Revision ID: bba922808903
Revises: 563a3bad61c9
Create Date: 2023-12-25 21:46:29.128828

"""
import enum
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bba922808903'
down_revision: Union[str, None] = '563a3bad61c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class ProblemStateEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DELAYED = "DELAYED"
    SUGGESTING = "SUGGESTING"
    VOTING = "VOTING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        f'''INSERT INTO problem_states (name) VALUES 
        {','.join([f"('{state.value}')" for state in ProblemStateEnum])};
        '''
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
        TRUNCATE problem_states CASCADE;
        """
    )
    # ### end Alembic commands ###
