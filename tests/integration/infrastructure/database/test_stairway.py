import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from alembic.script import Script, ScriptDirectory


def get_revisions(alembic_config: AlembicConfig) -> list[Script]:
    # Get directory object with Alembic migrations
    script_location = alembic_config.get_main_option(
        "script_location", default="./src/dma/infrastructure/database/migrations",
    )
    revisions_dir = ScriptDirectory(script_location)

    # Get & sort migrations, from first to last
    revisions: list[Script] = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.fixture(scope="module", autouse=True)
def drop_db(alembic_config: AlembicConfig) -> None:
    downgrade(alembic_config, "base")


@pytest.mark.order("first")
def test_migrations_stairway(alembic_config: AlembicConfig) -> None:
    for revision in get_revisions(alembic_config):
        upgrade(alembic_config, revision.revision)

        # We need -1 for downgrading first migration (its down_revision is None)
        downgrade(alembic_config, revision.down_revision or "-1")  # type: ignore[arg-type]
        upgrade(alembic_config, revision.revision)
