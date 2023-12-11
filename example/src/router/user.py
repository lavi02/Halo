# slack_router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from example.src.config.config import Config
from example.src.database.__init__ import *
from example.src.service.jwt import *

class UserAPIRouter:
    def __init__(self):
        self.router = APIRouter()

        self.user_login()

    def user_token(self):
        @app.post("/token")
        async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)): 
            user = AuthManager.authenticate_user(db, form_data.username, form_data.password)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
            
            access_token = AuthManager.create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
            return {"access_token": access_token, "token_type": "bearer"}

    def user_login(self):
        @self.router.get("/test")
        async def login(id: str, password: str):
            if result == None:
                return JSONResponse(status_code=200, content={"message": "success"})
            else:
                return JSONResponse(status_code=400, content={"message": "failed"})