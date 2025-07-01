import os
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy import create_engine
from settings.env import PGSQL_URL
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from redis import Redis, ConnectionPool
from settings.env import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_INDEX


def create_app() -> FastAPI:
    app = FastAPI(title="My API")
    return app


def get_redis_client() -> Redis:
    pool = ConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=REDIS_INDEX,
        decode_responses=True,
    )
    return Redis(connection_pool=pool)


cache_queue = get_redis_client()

Base = declarative_base()

engine = create_engine(
    PGSQL_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)

# 如果你想要线程安全的 session，也可以这么写
DBSession = scoped_session(SessionLocal)