from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from example.src.database.models.user.user import User

class AuthManager:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    SECRET_KEY = "your_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return AuthManager.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return AuthManager.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthManager.SECRET_KEY, algorithm=AuthManager.ALGORITHM)

    @staticmethod
    def get_user(db, username: str):
        return db.query(User).filter(User.user_id == username).first()

    @staticmethod
    def authenticate_user(db, username: str, password: str):
        user = AuthManager.get_user(db, username)
        if not user or not AuthManager.verify_password(password, user.hashed_password):
            return False
        return user
