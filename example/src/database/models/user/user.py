from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, VARCHAR, DATETIME, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserTable(Base):  # 유저 테이블
    __tablename__ = 'users'  # 테이블 이름
    user_id = Column(VARCHAR(16), primary_key=True, nullable=False)  # 유저 아이디
    password = Column(VARCHAR(20), nullable=False)  # 유저 비밀번호
    email = Column(VARCHAR(100), nullable=False)  # 유저 이메일
    status = Column(VARCHAR(16), nullable=False, default='active')  # 유저 상태
    created_at = Column(DATETIME, nullable=False, default=func.now())  # 유저 생성일


class User(BaseModel):
    user_id: str
    password: str
    email: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
