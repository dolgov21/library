from contextlib import asynccontextmanager

import uvicorn
from api.v1 import client_router, librarian_router
from app_setup import setup_logger
from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    logger.debug("Application startup...")
    yield
    logger.debug("Application down.")


app = FastAPI()

app.include_router(client_router)
app.include_router(librarian_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, app_dir="app")
