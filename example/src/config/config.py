# config if development - .env.development
# config if production - .env.production

import os
from dataclasses import dataclass 

class Config:
    
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))