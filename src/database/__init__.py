import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis
from contextlib import contextmanager
from src.repo.log.__init__ import handler


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


redis_client = redis.Redis(host=Config.REDIS_HOST,
                           port=Config.REDIS_PORT, db=0)

engine = create_engine(
    Config.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        handler.log.error("Database error: %s", e)
        raise e
    finally:
        db.close()


@contextmanager
def get_redis() -> redis.Redis:
    try:
        yield redis_client
    except Exception as e:
        handler.log.error("Redis error: %s", e)
        raise e
