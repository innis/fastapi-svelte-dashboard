# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from functools import lru_cache
from os import path

from . import config
from .dependencies import get_query_token, get_token_header
from .routers import events, gift
from .internal import admin

g_conf = config.Settings()
dep_list = []

if g_conf.env == "live":
    dep_list.append(Depends(get_token_header))  # live 환경일때는 api 에 x-token 체크를 합니다.
    openapi_url=None
    docs_url=None
    redoc_url=None
else:
    openapi_url="/openapi.json"
    docs_url="/docs"
    redoc_url="/redoc"

app = FastAPI(
    openapi_url=openapi_url, docs_url=docs_url, redoc_url=redoc_url,
    version=g_conf.version
    )

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="admin-app/public/assets"), name="assets")
app.mount("/build", StaticFiles(directory="admin-app/public/build"), name="build")

app.include_router(
    events.router,
    tags=["events"],
    dependencies=dep_list
    )
app.include_router(
    gift.router,
    tags=["gifts"],
    dependencies=dep_list
)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=dep_list,
    responses={418: {"description": "I'm a teapot"}},
)

class Admin(BaseModel):
    id: int
    email: str
    created_at: datetime
    disabled: bool

@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/info")
async def info(conf: config.Settings = Depends(get_settings)):
    buildtm = None
    filename = "/code/docker.buildtm"
    if path.isfile(filename):
        with open(filename, "r") as f:
            buildtm = f.readline().strip()

    return {
        "build_time": buildtm,
        "app_name": conf.app_name,
        "admin_email": conf.admin_email,
        "app_version": conf.version,
        "environment": conf.env
    }

