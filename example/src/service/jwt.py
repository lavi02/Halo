from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext

from example.src.database.models.user.user import User
from abc import ABCMeta, abstractmethod


class JwtBase(metaclass=ABCMeta):
    @abstractmethod
    def get_current_user(self, token: str):
        pass


class AuthBase(metaclass=ABCMeta):
    @abstractmethod
    def verify_password(self, plain_password, hashed_password):
        pass

    @abstractmethod
    def get_password_hash(self, password):
        pass

    @abstractmethod
    def create_access_token(self, data, expires_delta):
        pass

    @abstractmethod
    def get_user(self, db, username):
        pass

    @abstractmethod
    def authenticate_user(self, db, username, password):
        pass


class AuthManager(AuthBase):
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


class JWTAuthenticator(JwtBase):
    @staticmethod
    def get_current_user(token: str = Depends(AuthManager.oauth2_scheme)):
        try:
            payload = jwt.decode(token, AuthManager.SECRET_KEY, algorithms=[
                                 AuthManager.ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            return username
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
