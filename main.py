from fastapi import APIRouter as FastAPIRouter
from fastapi import FastAPI
from example.src.router.user import UserAPIRouter
from src.repo.log.__init__ import handler

class MainAPIRouter:
    def __init__(self):
        self.router = FastAPIRouter() 
        self.user_router = UserAPIRouter()

        self.initialize_routes()

    def initialize_routes(self):
        self.router.include_router(self.user_router.router, tags=["slack"])

async def startup():
    # if not Config.REAL:
    #     asyncio.create_task(start_periodic_tasks())
    #     handler.log.info("Periodic tasks started")

    handler.log.info("Server started")

api_router = MainAPIRouter() 

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
app.add_event_handler("startup", startup)
app.include_router(api_router.router, prefix="/api/v1") 

# docker-compose up -f docker-compose.yml --build -d