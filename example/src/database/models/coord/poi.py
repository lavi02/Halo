from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, VARCHAR, DATETIME, func, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PoiTable(Base):  # 분석 결과 테이블
    __tablename__ = 'POIs'
    poi_id = Column(VARCHAR(16), primary_key=True, nullable=False)  # 분석 아이디
    user_id = Column(VARCHAR(16), nullable=False)  # 유저 아이디
    place_name = Column(VARCHAR(50), nullable=False)  # 장소 이름
    address = Column(VARCHAR(50), nullable=False)  # 주소
    lat = Column(DECIMAL(3, 6), nullable=False)  # 위도
    lng = Column(DECIMAL(3, 6), nullable=False)  # 경도
    created_at = Column(DATETIME, nullable=False, default=func.now())  # 분석 생성일


class Poi(BaseModel):
    poi_id: str
    user_id: str
    place_name: str
    address: str
    lat: float
    lng: float
    created_at: datetime

    class Config:
        orm_mode = True
