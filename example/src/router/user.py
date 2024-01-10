# slack_router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from example.src.database.__init__ import get_db
from example.src.database.models.user.user import *
from example.src.database.__init__ import *
from example.src.service.jwt import *


class UserAPIRouter:
    def __init__(self):
        self.router = APIRouter()

        self.check_health()
        self.user_token()
        self.user_login()
        self.user_register()

    def check_health(self):
        @self.router.get("/health")
        async def health():
            return JSONResponse(status_code=200, content={"message": "success"})

    def user_token(self):
        @self.router.post("/token")
        async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
            user = AuthManager.authenticate_user(
                db, form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

            access_token = AuthManager.create_access_token(data={"sub": user.username})
            return {"access_token": access_token, "token_type": "bearer"}

    def user_login(self):
        @self.router.get("/login")
        async def login(id: str, password: str, db = Depends(get_db)):
            user = AuthManager.authenticate_user(db, id, password)
            if user:
                access_token = AuthManager.create_access_token(data={"sub": user.username})
                return JSONResponse(status_code=200, content={"message": "success", "token": access_token})
            else:
                return JSONResponse(status_code=400, content={"message": "failed"})
            
    def user_register(self):
        @self.router.post("/register")
        async def register(userInfo: User, db = Depends(get_db)):
            user = AuthManager.get_user(db, userInfo.user_id)
            if user:
                return JSONResponse(status_code=400, content={"message": "failed"})
            else:
                hashed_password = AuthManager.get_password_hash(userInfo.password)
                db_user = UserTable(user_id=userInfo.user_id, password=hashed_password, email=userInfo.email)
                db.add(db_user)
                db.commit()
                return JSONResponse(status_code=200, content={"message": "success"})