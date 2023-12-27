from example.src.database.models.optimize.result import AnalysisTable
from example.src.database.__init__ import get_db


class AnalysisManager:
    def __init__(self, db_session):
        self.db_session = db_session

    def save_optimization_result(self, result: dict, user_id: str):
        analysis = AnalysisTable(
            user_id=user_id,
            inputs=result['inputs'],
            outputs=result['outputs'],
            base_time=result['base_time'],
            base_stop=result['base_stop'],
        )
        self.db_session.add(analysis)
        self.db_session.commit()
        self.db_session.refresh(analysis)
        return analysis

    def get_analysis_by_user_id(self, user_id: str):
        return self.db_session.query(AnalysisTable).filter(AnalysisTable.user_id == user_id).all()

    def get_analysis_by_id(self, analysis_id: str):
        return self.db_session.query(AnalysisTable).filter(AnalysisTable.analysis_id == analysis_id).first()

    def delete_analysis_by_id(self, analysis_id: str):
        analysis = self.get_analysis_by_id(analysis_id)
        self.db_session.delete(analysis)
        self.db_session.commit()
        return analysis_id
    
    def delete_analysis_by_user_id(self, user_id: str):
        analysis = self.get_analysis_by_user_id(user_id)
        self.db_session.delete(analysis)
        self.db_session.commit()
        return user_id

analysisQuery = AnalysisManager(get_db())