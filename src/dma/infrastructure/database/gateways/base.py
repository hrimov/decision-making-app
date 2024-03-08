from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyGateway:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
