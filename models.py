from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)

engine = create_async_engine(url="sqlite+aiosqlite:///database.db")

async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    message_thread_id: Mapped[int] = mapped_column(Integer)
    is_blocked: Mapped[bool] = mapped_column(Boolean)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)