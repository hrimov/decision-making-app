from typing import Iterable, NoReturn

from sqlalchemy import func, select, Select
from sqlalchemy.exc import DBAPIError, IntegrityError

from dma.application.common.pagination import (
    LimitOffsetPagination,
    LimitOffsetPaginationResult,
    SortOrder,
)
from dma.application.common.exceptions import DatabaseGatewayError
from dma.application.user import dto
from dma.application.user.exceptions import (
    UserIdNotExists,
    UserNicknameNotExists,
)
from dma.application.user.filters import UserFilters
from dma.infrastructure.database.converters.user import (
    convert_db_model_to_user_dto,
    convert_user_create_dto_to_db_model,
    update_user_fields,
)
from dma.infrastructure.database.exception_mapper import exception_mapper
from dma.infrastructure.database.models.user import User as UserModel

from .base import SQLAlchemyGateway


class UserGatewayImpl(SQLAlchemyGateway):
    @exception_mapper
    async def get_user_by_id(self, id_: int) -> dto.User:
        user: UserModel | None = await self.session.get(UserModel, id_)

        if user is None:
            raise UserIdNotExists(id_)

        return convert_db_model_to_user_dto(user)

    @exception_mapper
    async def get_user_by_nickname(self, nickname: str) -> dto.User:
        statement = select(UserModel).where(UserModel.nickname == nickname)
        user: UserModel | None = await self.session.scalar(statement)

        if user is None:
            raise UserNicknameNotExists(nickname)

        return convert_db_model_to_user_dto(user)

    @exception_mapper
    async def get_users(
            self, filters: UserFilters, pagination: LimitOffsetPagination,
    ) -> dto.Users:
        statement = select(UserModel)
        statement = self._apply_filters(statement, filters)
        statement = self._apply_pagination(statement, pagination)

        result: Iterable[UserModel] = await self.session.scalars(statement)
        users = [convert_db_model_to_user_dto(user) for user in result]
        users_count = await self._get_users_count(filters)
        return dto.Users(
            data=users,
            pagination=LimitOffsetPaginationResult.from_pagination(
                pagination, total=users_count,
            ),
        )

    @exception_mapper
    async def create_user(self, user_dto: dto.UserCreate) -> dto.User:
        database_user = convert_user_create_dto_to_db_model(user_dto)
        self.session.add(database_user)

        try:
            await self.session.flush((database_user,))
        except IntegrityError as error:
            self._parse_error(error)

        return convert_db_model_to_user_dto(database_user)

    @exception_mapper
    async def update_user(self, user_dto: dto.UserUpdate) -> dto.User:
        existing_user: dto.User = await self.get_user_by_id(user_dto.id)
        updated_user: UserModel = update_user_fields(
            existing_user=existing_user,
            user_update_dto=user_dto,
        )

        try:
            await self.session.merge(updated_user)
        except IntegrityError as error:
            self._parse_error(error)

        return convert_db_model_to_user_dto(updated_user)

    # noinspection PyMethodMayBeStatic
    # TODO: implement proper error handling
    def _parse_error(self, error: DBAPIError) -> NoReturn:
        match error.orig.diag.constraint_name:  # type: ignore
            case _:
                raise DatabaseGatewayError from error

    # noinspection PyMethodMayBeStatic
    # TODO: implement necessary filters for the User
    def _apply_filters(self, statement: Select, filters: UserFilters) -> Select:  # noqa
        return statement

    # noinspection PyMethodMayBeStatic
    def _apply_pagination(
            self, statement: Select, pagination: LimitOffsetPagination,
    ) -> Select:
        if pagination.order is SortOrder.ASC:
            statement = statement.order_by(UserModel.id.asc())
        else:
            statement = statement.order_by(UserModel.id.desc())

        if pagination.offset is not None:
            statement = statement.offset(pagination.offset)
        if pagination.limit is not None:
            statement = statement.limit(pagination.limit)

        return statement

    async def _get_users_count(self, filters: UserFilters) -> int:
        statement = select(func.count(UserModel.id))
        statement = self._apply_filters(statement, filters)
        users_count: int | None = await self.session.scalar(statement)
        return users_count if users_count is not None else 0
