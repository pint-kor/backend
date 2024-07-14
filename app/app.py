from contextlib import asynccontextmanager

from app.db import on_startup
from fastapi import FastAPI

from app.auth import AuthRouters
from app.blog import BlogRouter
from app.event import EventRouter
from app.place import PlaceRouter
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router, kwargs in AuthRouters:
    app.include_router(router=router, **kwargs)
    
app.include_router(router=BlogRouter, tags=["blog"])
app.include_router(router=EventRouter, tags=["event"])
app.include_router(router=PlaceRouter, tags=["place"])