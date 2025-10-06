import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import get_session
from app.main import app


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    return create_async_engine(
        settings.TEST_DATABASE_URL,
        future=True,
        echo=False,
        poolclass=None,
        pool_pre_ping=True,
        pool_recycle=3600,
    )


@pytest_asyncio.fixture(autouse=True)
async def clean_database(db_session):
    try:
        await db_session.execute(text("DELETE FROM books"))
        await db_session.commit()
    except Exception:
        await db_session.rollback()
        await db_session.execute(text("TRUNCATE TABLE books RESTART IDENTITY CASCADE"))
        await db_session.commit()
    finally:
        await db_session.rollback()


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=False)

    async with engine.connect() as connection:
        transaction = await connection.begin()

        session_factory = sessionmaker(
            bind=connection, class_=AsyncSession, expire_on_commit=False
        )
        session = session_factory()

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()
            await connection.close()
            await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
