import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer  # type: ignore[import-untyped]


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer("postgres:15-alpine")
    if os.name == "nt":  # Note: from testcontainers/testcontainers-python#108
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        connection_url = postgres.get_connection_url().replace("psycopg2", "psycopg")
        yield connection_url
    finally:
        postgres.stop()


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> AlembicConfig:
    config = AlembicConfig("alembic.ini")
    config.set_main_option("sqlalchemy.url", postgres_url)
    return config


@pytest.fixture(scope="function", autouse=True)
def upgrade_database_schema(
        alembic_config: AlembicConfig,
) -> Generator[None, None, None]:
    upgrade(alembic_config, "head")
    yield
    downgrade(alembic_config, "base")


@pytest.fixture(scope="session")
def engine(postgres_url: str) -> AsyncEngine:
    return create_async_engine(url=postgres_url)


@pytest_asyncio.fixture()
async def session_factory(
        engine: AsyncEngine,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    session_factory_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False,
    )
    yield session_factory_
    await engine.dispose()


@pytest_asyncio.fixture()
async def session(
        session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session_:
        yield session_
