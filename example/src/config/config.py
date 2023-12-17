# config if development - .env.development
# config if production - .env.production

import os
from dataclasses import dataclass
from fastapi import FastAPI

app = FastAPI()


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/halo")
    MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "root")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "halo")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
