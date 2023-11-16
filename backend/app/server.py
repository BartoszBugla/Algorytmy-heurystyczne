import os

from app.core.config import config

from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.functions import functions_router
from app.storage import storage_router
from app.algorithms import algorithms_router


origins = [
    "http://localhost:5173",
]


def init_routers(app_: FastAPI) -> None:
    app_.include_router(functions_router)
    app_.include_router(storage_router)
    app_.include_router(algorithms_router)


def init_middleware(app_: FastAPI) -> None:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Algorytmy metaherustyczne API",
        description="Algorytmy metaherustyczne API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
        # dependencies=[Depends(Logging)],
        # middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_middleware(app_=app_)

    return app_


app = create_app()
