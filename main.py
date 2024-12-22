from contextlib import asynccontextmanager
import logging
import platform
import uvicorn
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.core.settings import APPS_MODELS, DATABASE_URI
from src.admin.router import router as admin_router
from src.user.router import router as user_router
from tortoise.contrib.fastapi import RegisterTortoise


@asynccontextmanager 
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        db_url=DATABASE_URI,
        modules={"models": APPS_MODELS}
    ):
        yield

def create_app():
    app = FastAPI(
        title="XU",
        docs_url="/",
        lifespan=lifespan
    )

    app.include_router(user_router)

    app.include_router(admin_router)

        

    origins = ["*"]
        
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app_ = create_app()

loop: Literal["auto", "uvloop"]
if platform == "linux":
    try:
        import uvloop

        uvloop.install()
        loop = "uvloop"
    except ModuleNotFoundError:
        loop = "auto"
else:
    loop = "auto"
# ===============================

server = uvicorn.Server(
    uvicorn.Config(
        app_,
        host="0.0.0.0",
        port=8000,
        workers=1,
        reload=False,
        log_level=logging.INFO,
        loop=loop,
    ),
)

server.run()