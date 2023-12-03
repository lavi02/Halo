from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, VARCHAR, DATETIME, func, JSON, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AnalysisTable(Base):  # 분석 결과 테이블
    __tablename__ = 'analysis'
    analysis_id = Column(VARCHAR(16), primary_key=True,
                         nullable=False)  # 분석 아이디
    user_id = Column(VARCHAR(16), nullable=False)  # 유저 아이디
    inputs = Column(JSON, nullable=False)  # 입력값
    outputs = Column(JSON, nullable=False)  # 출력값
    base_time = Column(DATETIME, nullable=False)  # 기준 시간
    base_stop = Column(INTEGER, nullable=False)  # 기준 정지
    created_at = Column(DATETIME, nullable=False, default=func.now())  # 분석 생성일


class Analysis(BaseModel):
    analysis_id: str
    user_id: str
    inputs: dict
    outputs: dict
    base_time: datetime
    base_stop: int
    created_at: datetime

    class Config:
        orm_mode = True
