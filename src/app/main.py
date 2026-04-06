from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield  # schema managed by Alembic; no create_all


app = FastAPI(title="Agile Team Helper", lifespan=lifespan)
app.include_router(router)
