import pytest
import pytest_asyncio

from functools import reduce

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.problem.filters import ProblemFilters
from src.app.application.common.pagination import LimitOffsetPagination, SortOrder
from src.app.application.problem.dto import (
    Problem as ProblemDTO,
    Problems as ProblemsDTO,
    ProblemCreate as ProblemCreateDTO,
    ProblemUpdate as ProblemUpdateDTO
)
from src.app.application.user.dto import (
    UserCreate as UserCreateDTO
)
from src.app.infrastructure.database.gateways.problem import ProblemGatewayImpl
from src.app.infrastructure.database.gateways.user import UserGatewayImpl


async def test_create_problem(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
        problem_to_create: ProblemCreateDTO,
):
    # we need a user present in the database with id # 1
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        await user_gateway.create_user(user_to_create)

    problem_gateway = ProblemGatewayImpl(session)
    async with session.begin():
        problem_dto: ProblemDTO = await problem_gateway.create_problem(problem_to_create)

    assert problem_dto.title == problem_to_create.title
    assert problem_dto.description == problem_to_create.description
    assert problem_dto.private == problem_to_create.private
    assert isinstance(problem_dto.id, int)


async def test_update_problem(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
        problem_to_create: ProblemCreateDTO,
):
    # we need a user present in the database with id # 1
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        await user_gateway.create_user(user_to_create)

    problem_gateway = ProblemGatewayImpl(session)
    async with session.begin():
        problem_dto: ProblemDTO = await problem_gateway.create_problem(problem_to_create)

    updated_title, updated_description = "update_title", "updated_description"
    problem_to_update = ProblemUpdateDTO(
        id=problem_dto.id,
        title=updated_title,
        description=updated_description,
    )
    async with session.begin():
        new_problem_dto: ProblemDTO = await problem_gateway.update_problem(problem_to_update)

    assert problem_dto.id == new_problem_dto.id
    assert problem_dto.creator_id == new_problem_dto.creator_id
    assert problem_dto.state_id == new_problem_dto.state_id
    assert problem_dto.title != new_problem_dto.title
    assert problem_dto.description != new_problem_dto.description
    assert new_problem_dto.title == updated_title
    assert new_problem_dto.description == updated_description


async def test_get_problem_by_id(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
        problem_to_create: ProblemCreateDTO,
):
    # we need a user present in the database with id # 1
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        await user_gateway.create_user(user_to_create)

    problem_gateway = ProblemGatewayImpl(session)
    async with session.begin():
        created_problem: ProblemDTO = await problem_gateway.create_problem(problem_to_create)

    problem_dto: ProblemDTO = await problem_gateway.get_problem_by_id(created_problem.id)

    assert problem_dto.id == created_problem.id
    assert problem_dto.title == created_problem.title
    assert problem_dto.description == created_problem.description
    assert problem_dto.creator_id == created_problem.creator_id
    assert problem_dto.state_id == created_problem.state_id
    assert problem_dto.private == created_problem.private


async def test_get_problems(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
        problem_to_create: ProblemCreateDTO,
):
    # we need a user present in the database with id # 1
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        await user_gateway.create_user(user_to_create)

    problem_gateway = ProblemGatewayImpl(session)

    insert_problems_count: int = 10

    async with session.begin():
        for i in range(insert_problems_count):
            await problem_gateway.create_problem(problem_to_create)

    filters = ProblemFilters()
    pagination = LimitOffsetPagination()
    result: ProblemsDTO = await problem_gateway.get_problems(filters=filters, pagination=pagination)

    assert result.pagination.total == insert_problems_count
    assert len(result.data) == insert_problems_count


async def test_get_problems_order(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
        problem_to_create: ProblemCreateDTO,
):
    # we need a user present in the database with id # 1
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        await user_gateway.create_user(user_to_create)

    problem_gateway = ProblemGatewayImpl(session)

    insert_problems_count: int = 10
    limit: int = 5

    async with session.begin():
        for i in range(insert_problems_count):
            await problem_gateway.create_problem(problem_to_create)

    filters = ProblemFilters()
    pagination = LimitOffsetPagination(limit=5, order=SortOrder.DESC)
    result: ProblemsDTO = await problem_gateway.get_problems(filters=filters, pagination=pagination)

    assert result.pagination.total == insert_problems_count
    assert len(result.data) == limit

    # check every ID will be smaller than previous one
    assert reduce(
        lambda previous, current: (previous[0] and previous[1].id < current.id, current),
        result.data,
        (True, result.data[0])
    )

    filters = ProblemFilters()
    pagination = LimitOffsetPagination(limit=5, order=SortOrder.ASC)
    result: ProblemsDTO = await problem_gateway.get_problems(filters=filters, pagination=pagination)

    assert result.pagination.total == insert_problems_count
    assert len(result.data) == limit

    # check every ID will be bigger than previous one
    assert reduce(
        lambda previous, current: (previous[0] and previous[1].id > current.id, current),
        result.data,
        (True, result.data[0])
    )


async def test_get_problems_limit_offset(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
        problem_to_create: ProblemCreateDTO,
):
    # we need a user present in the database with id # 1
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        await user_gateway.create_user(user_to_create)

    problem_gateway = ProblemGatewayImpl(session)

    insert_problems_count: int = 10
    limit: int = 5
    offset: int = 3

    async with session.begin():
        for i in range(insert_problems_count):
            await problem_gateway.create_problem(problem_to_create)

    filters = ProblemFilters()
    pagination = LimitOffsetPagination(limit=limit, offset=offset, order=SortOrder.ASC)
    result: ProblemsDTO = await problem_gateway.get_problems(filters=filters, pagination=pagination)

    assert result.pagination.total == insert_problems_count
    assert len(result.data) == limit
    assert all([problem.id == offset + i for i, problem in enumerate(result.data, 1)])
