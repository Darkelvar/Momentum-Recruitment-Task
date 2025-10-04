from fastapi import FastAPI
from app.api.v1 import books


app = FastAPI(
    title="Momentum Recruitment Task Library API",
    version="1.0.0",
    description="System for managing a simple library API",
)


app.include_router(books.router, prefix="/api/v1")
