from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, VARCHAR, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CacheTable(Base):  # 캐싱 테이블
    __tablename__ = 'coord_cache'
    address = Column(VARCHAR(50), primary_key=True, nullable=False)  # 주소
    lat = Column(DECIMAL(3, 6), nullable=False)  # 위도
    lng = Column(DECIMAL(3, 6), nullable=False)  # 경도


class Poi(BaseModel):
    address: str
    lat: float
    lng: float

    class Config:
        orm_mode = True
