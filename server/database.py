from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from server.config import settings

engine = create_async_engine(
    url=settings.get_database_url,
    echo=settings.DB_ECHO,
    pool_size=20,
    max_overflow=15,
)

async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def create_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def drop_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


class Base(DeclarativeBase):
    pass
