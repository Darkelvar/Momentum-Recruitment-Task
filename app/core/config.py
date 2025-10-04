from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://library_user:library_pass@db:5432/library_db"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql+psycopg2://library_user:library_pass@db:5432/library_db"
    )


settings = Settings()
