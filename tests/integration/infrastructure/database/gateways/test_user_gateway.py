import pytest
import pytest_asyncio

from functools import reduce

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.user.filters import UserFilters
from src.app.application.common.pagination import LimitOffsetPagination, SortOrder
from src.app.application.user.dto import (
    User as UserDTO,
    Users as UsersDTO,
    UserCreate as UserCreateDTO,
    UserUpdate as UserUpdateDTO
)
from src.app.infrastructure.database.gateways.user import UserGatewayImpl


async def test_create_user(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
):
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        user_dto: UserDTO = await user_gateway.create_user(user_to_create)

    assert user_dto.nickname == user_to_create.nickname
    assert user_dto.fullname == user_to_create.fullname
    assert user_dto.email == user_to_create.email
    assert isinstance(user_dto.id, int)
    assert isinstance(user_dto.reputation, int)
    assert user_dto.reputation == 0


async def test_update_user(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
):
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        user_dto: UserDTO = await user_gateway.create_user(user_to_create)

    updated_email, updated_fullname = "update_email", "updated_fullname"
    user_to_update = UserUpdateDTO(
        id=user_dto.id,
        email=updated_email,
        fullname=updated_fullname,
    )
    async with session.begin():
        new_user_dto: UserDTO = await user_gateway.update_user(user_to_update)

    assert user_dto.id == new_user_dto.id
    assert user_dto.email != new_user_dto.email
    assert user_dto.fullname != new_user_dto.fullname
    assert new_user_dto.email == updated_email
    assert new_user_dto.fullname == updated_fullname


async def test_get_user_by_nickname(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
):
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        await user_gateway.create_user(user_to_create)

    user_dto: UserDTO = await user_gateway.get_user_by_nickname(user_to_create.nickname)

    assert user_dto.nickname == user_to_create.nickname
    assert user_dto.fullname == user_to_create.fullname
    assert user_dto.email == user_to_create.email


async def test_get_user_by_id(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
):
    user_gateway = UserGatewayImpl(session)
    async with session.begin():
        created_user: UserDTO = await user_gateway.create_user(user_to_create)

    user_dto: UserDTO = await user_gateway.get_user_by_id(created_user.id)

    assert user_dto.id == created_user.id
    assert user_dto.email == created_user.email
    assert user_dto.nickname == created_user.nickname
    assert user_dto.fullname == created_user.fullname


async def test_get_users(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
):
    user_gateway = UserGatewayImpl(session)

    insert_users_count: int = 10

    async with session.begin():
        for i in range(insert_users_count):
            await user_gateway.create_user(user_to_create)

    filters = UserFilters()
    pagination = LimitOffsetPagination()
    result: UsersDTO = await user_gateway.get_users(filters=filters, pagination=pagination)

    assert result.pagination.total == insert_users_count
    assert len(result.data) == insert_users_count


async def test_get_users_order(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
):
    user_gateway = UserGatewayImpl(session)

    insert_users_count: int = 10
    limit: int = 5

    async with session.begin():
        for i in range(insert_users_count):
            await user_gateway.create_user(user_to_create)

    filters = UserFilters()
    pagination = LimitOffsetPagination(limit=5, order=SortOrder.DESC)
    result: UsersDTO = await user_gateway.get_users(filters=filters, pagination=pagination)

    assert result.pagination.total == insert_users_count
    assert len(result.data) == limit

    # check every ID will be smaller than previous one
    assert reduce(
        lambda previous, current: (previous[0] and previous[1].id < current.id, current),
        result.data,
        (True, result.data[0])
    )

    filters = UserFilters()
    pagination = LimitOffsetPagination(limit=5, order=SortOrder.ASC)
    result: UsersDTO = await user_gateway.get_users(filters=filters, pagination=pagination)

    assert result.pagination.total == insert_users_count
    assert len(result.data) == limit

    # check every ID will be bigger than previous one
    assert reduce(
        lambda previous, current: (previous[0] and previous[1].id > current.id, current),
        result.data,
        (True, result.data[0])
    )


async def test_get_users_limit_offset(
        session: AsyncSession,
        user_to_create: UserCreateDTO,
):
    user_gateway = UserGatewayImpl(session)

    insert_users_count: int = 10
    limit: int = 5
    offset: int = 3

    async with session.begin():
        for i in range(insert_users_count):
            await user_gateway.create_user(user_to_create)

    filters = UserFilters()
    pagination = LimitOffsetPagination(limit=limit, offset=offset, order=SortOrder.ASC)
    result: UsersDTO = await user_gateway.get_users(filters=filters, pagination=pagination)

    assert result.pagination.total == insert_users_count
    assert len(result.data) == limit
    assert all([user.id == offset + i for i, user in enumerate(result.data, 1)])
