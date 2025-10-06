from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://library_user:library_pass@db:5432/library_db"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql+psycopg2://library_user:library_pass@db:5432/library_db"
    )
    TEST_DATABASE_URL: str = (
        "postgresql+asyncpg://library_user:library_pass@test-db:5432/library_test_db"
    )


settings = Settings()
