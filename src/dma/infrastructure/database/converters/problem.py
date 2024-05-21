from dataclasses import fields

from dma.application.problem import dto
from dma.infrastructure.database.models.problem import (
    Problem as ProblemModel,
    ProblemState as ProblemStateModel,
)


def convert_db_model_to_problem_dto(problem: ProblemModel) -> dto.Problem:
    return dto.Problem(
        id=problem.id,
        title=problem.title,
        description=problem.description,
        creator_id=problem.creator_id,
        private=problem.private,
        state_id=problem.state_id,
    )


def convert_problem_dto_to_db_model(problem_dto: dto.Problem) -> ProblemModel:
    return ProblemModel(
        id=problem_dto.id,
        title=problem_dto.title,
        description=problem_dto.description,
        creator_id=problem_dto.creator_id,
        private=problem_dto.private,
        state_id=problem_dto.state_id,
    )


def convert_problem_create_dto_to_db_model(
        problem_dto: dto.ProblemCreate,
) -> ProblemModel:
    return ProblemModel(
        title=problem_dto.title,
        description=problem_dto.description,
        creator_id=problem_dto.creator_id,
        private=problem_dto.private,
        state_id=problem_dto.state_id,
    )


def update_problem_fields(
        existing_problem: dto.Problem, problem_update_dto: dto.ProblemUpdate,
) -> ProblemModel:
    result_model = ProblemModel()
    for field in fields(existing_problem):
        existing_field_value = getattr(existing_problem, field.name)

        if hasattr(problem_update_dto, field.name):
            new_value = getattr(problem_update_dto, field.name)
        else:
            new_value = None

        settable_value = new_value if new_value is not None else existing_field_value
        setattr(result_model, field.name, settable_value)
    return result_model


def convert_problem_state_create_dto_to_db_model(
        problem_state_dto: dto.ProblemStateCreate,
) -> ProblemStateModel:
    return ProblemStateModel(
        name=problem_state_dto.name,
    )


def convert_db_model_to_problem_state_dto(
        problem: ProblemStateModel,
) -> dto.ProblemState:
    return dto.ProblemState(
        id=problem.id,
        name=problem.name,
    )
