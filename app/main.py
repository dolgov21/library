from contextlib import asynccontextmanager

import uvicorn
from api.v1 import client_router, librarian_router
from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Application startup...")
    yield
    logger.debug("Application down.")


app = FastAPI()

app.include_router(client_router)
app.include_router(librarian_router)

if __name__ == "__main__":
    uvicorn.run("main:app", app_dir="app")
