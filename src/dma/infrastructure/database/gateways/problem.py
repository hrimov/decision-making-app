from typing import Iterable, NoReturn

from sqlalchemy import func, select, Select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from dma.application.common.pagination import (
    LimitOffsetPagination,
    LimitOffsetPaginationResult,
    SortOrder,
)
from dma.application.common.exceptions import DatabaseGatewayError
from dma.application.problem import dto
from dma.application.problem.filters import ProblemFilters, ProblemStateFilters
from dma.application.problem.exceptions import (
    ProblemIdNotExists,
    ProblemStateIdNotExists,
    ProblemStateNameNotExists,
)
from dma.infrastructure.database.converters.problem import (
    convert_db_model_to_problem_dto,
    convert_db_model_to_problem_state_dto,
    convert_problem_create_dto_to_db_model,
    convert_problem_state_create_dto_to_db_model,
    update_problem_fields,
)
from dma.infrastructure.database.exception_mapper import exception_mapper
from dma.infrastructure.database.models.problem import (
    Problem as ProblemModel,
    ProblemState as ProblemStateModel,
)
from .base import SQLAlchemyGateway


class ProblemMemberGatewayImpl(SQLAlchemyGateway):
    def _parse_error(self, error: DBAPIError) -> NoReturn:
        raise NotImplementedError


class ProblemStateGatewayImpl(SQLAlchemyGateway):
    @exception_mapper
    async def create_problem_state(
            self, problem_state_dto: dto.ProblemStateCreate,
    ) -> dto.ProblemState:
        database_problem_state = convert_problem_state_create_dto_to_db_model(
            problem_state_dto,
        )
        self.session.add(database_problem_state)

        try:
            await self.session.flush((database_problem_state,))
        except IntegrityError as error:
            self._parse_error(error)

        return convert_db_model_to_problem_state_dto(database_problem_state)

    @exception_mapper
    async def get_problem_state_by_id(self, id_: int) -> dto.ProblemState:
        problem_state: ProblemStateModel | None = await self.session.get(
            ProblemStateModel, id_,
        )

        if problem_state is None:
            raise ProblemStateIdNotExists(id_)

        return convert_db_model_to_problem_state_dto(problem_state)

    @exception_mapper
    async def get_problem_state_by_name(self, name: str) -> dto.ProblemState:
        statement = select(ProblemStateModel).where(ProblemStateModel.name == name)
        problem_state: ProblemStateModel | None = await self.session.scalar(statement)

        if problem_state is None:
            raise ProblemStateNameNotExists(name)

        return convert_db_model_to_problem_state_dto(problem_state)

    @exception_mapper
    async def get_problem_states(
            self,
            filters: ProblemStateFilters,
            pagination: LimitOffsetPagination,
    ) -> dto.ProblemStates:
        statement = select(ProblemStateModel)
        statement = self._apply_filters(statement, filters)
        statement = self._apply_pagination(statement, pagination)

        result: Iterable[ProblemStateModel] = await self.session.scalars(statement)
        problem_states = [
            convert_db_model_to_problem_state_dto(problem_state)
            for problem_state in result
        ]
        problem_states_count = await self._get_problem_states_count(filters)
        return dto.ProblemStates(
            data=problem_states,
            pagination=LimitOffsetPaginationResult.from_pagination(
                pagination, total=problem_states_count,
            ),
        )

    # noinspection PyMethodMayBeStatic
    def _apply_filters(self, statement: Select, filters: ProblemStateFilters) -> Select:  # noqa
        return statement

    # noinspection PyMethodMayBeStatic
    def _apply_pagination(self, statement: Select, pagination: LimitOffsetPagination) -> Select:  # noqa
        return statement

    def _parse_error(self, error: DBAPIError) -> NoReturn:
        raise NotImplementedError

    async def _get_problem_states_count(self, filters: ProblemStateFilters) -> int:
        statement = select(func.count(ProblemStateModel.id))
        statement = self._apply_filters(statement, filters)
        problem_states_count: int | None = await self.session.scalar(statement)
        return problem_states_count if problem_states_count is not None else 0


class ProblemGatewayImpl(SQLAlchemyGateway):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

        self.state_gateway = ProblemStateGatewayImpl(session)
        self.member_gateway = ProblemMemberGatewayImpl(session)

    @exception_mapper
    async def get_problem_by_id(self, id_: int) -> dto.Problem:
        problem: ProblemModel | None = await self.session.get(ProblemModel, id_)

        if problem is None:
            raise ProblemIdNotExists(id_)

        return convert_db_model_to_problem_dto(problem)

    @exception_mapper
    async def get_problems(
            self, filters: ProblemFilters, pagination: LimitOffsetPagination,
    ) -> dto.Problems:
        statement = select(ProblemModel)
        statement = self._apply_filters(statement, filters)
        statement = self._apply_pagination(statement, pagination)

        result: Iterable[ProblemModel] = await self.session.scalars(statement)
        problems = [convert_db_model_to_problem_dto(problem) for problem in result]
        problems_count = await self._get_problems_count(filters)
        return dto.Problems(
            data=problems,
            pagination=LimitOffsetPaginationResult.from_pagination(
                pagination, total=problems_count,
            ),
        )

    @exception_mapper
    async def create_problem(self, problem_dto: dto.ProblemCreate) -> dto.Problem:
        database_problem = convert_problem_create_dto_to_db_model(problem_dto)
        self.session.add(database_problem)

        try:
            await self.session.flush((database_problem,))
        except IntegrityError as error:
            self._parse_error(error)

        return convert_db_model_to_problem_dto(database_problem)

    @exception_mapper
    async def update_problem(self, problem_dto: dto.ProblemUpdate) -> dto.Problem:
        existing_problem_dto: dto.Problem = await self.get_problem_by_id(problem_dto.id)
        existing_problem: ProblemModel = update_problem_fields(
            existing_problem=existing_problem_dto,
            problem_update_dto=problem_dto,
        )

        try:
            await self.session.merge(existing_problem)
        except IntegrityError as error:
            self._parse_error(error)

        return convert_db_model_to_problem_dto(existing_problem)

    # noinspection PyMethodMayBeStatic
    # TODO: implement proper error handling
    def _parse_error(self, error: DBAPIError) -> NoReturn:
        match error.orig.diag.constraint_name:  # type: ignore
            case _:
                raise DatabaseGatewayError from error

    # noinspection PyMethodMayBeStatic
    # TODO: implement necessary filters for the Problem
    def _apply_filters(self, statement: Select, filters: ProblemFilters) -> Select:  # noqa
        return statement

    # noinspection PyMethodMayBeStatic
    def _apply_pagination(
            self, statement: Select, pagination: LimitOffsetPagination,
    ) -> Select:
        if pagination.order is SortOrder.ASC:
            statement = statement.order_by(ProblemModel.id.asc())
        else:
            statement = statement.order_by(ProblemModel.id.desc())

        if pagination.offset is not None:
            statement = statement.offset(pagination.offset)
        if pagination.limit is not None:
            statement = statement.limit(pagination.limit)

        return statement

    async def _get_problems_count(self, filters: ProblemFilters) -> int:
        statement = select(func.count(ProblemModel.id))
        statement = self._apply_filters(statement, filters)
        problems_count: int | None = await self.session.scalar(statement)
        return problems_count if problems_count is not None else 0
