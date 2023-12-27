from fastapi import FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from typing import Dict, Tuple
from src.service.tsp.solver import run
from example.src.config.config import app
from fastapi import Depends, HTTPException
from example.src.database.__init__ import get_db
from example.src.database.models.optimize.result import AnalysisTable
from example.src.database.dml.analysis import analysisQuery
from example.src.service.jwt import JWTAuthenticator

# 1. FastAPI 설정
app = FastAPI()


class Waypoints(BaseModel):
    waypoints: Dict[str, Tuple[float, float]]


class RouteOptimizer:
    def __init__(self, waypoints: Dict[str, Tuple[float, float]]):
        self.waypoints = waypoints

    def optimize_route(self) -> Dict[str, Tuple[float, float]]:
        try:
            optimized_waypoints = run(self.waypoints)
            return optimized_waypoints
        except Exception as e:
            raise e


class OptAPIRouter:
    def __Init__(self):
        self.router = APIRouter()

    def optimize_waypoints(self):
        @app.post("/optimize")
        async def optimize(waypoints: Waypoints,  current_user: str = Depends(JWTAuthenticator.get_current_user)):
            try:
                optimizer = RouteOptimizer(waypoints.waypoints)
                optimized_route = optimizer.optimize_route()
                return optimized_route
            except Exception as e:
                raise HTTPException(status_code=200, detail=str(e))
        
    def get_analysis_by_user(self):
        @app.get("/analysis/user/{user_id}", response_model=List[AnalysisTable])
        async def get_analysis_by_user(user_id: str, current_user: str = Depends(JWTAuthenticator.get_current_user), db: Session = Depends(get_db)):
            return analysisQuery.get_analysis_by_user_id(user_id)

    def get_analysis_by_id(self):
        @app.get("/analysis/{analysis_id}", response_model=AnalysisTable)
        async def get_analysis_by_id(analysis_id: str, current_user: str = Depends(JWTAuthenticator.get_current_user), db: Session = Depends(get_db)):
            analysis = analysisQuery.get_analysis_by_id(analysis_id)
            if analysis is None:
                raise HTTPException(status_code=404, detail="Analysis not found")
            return analysis
