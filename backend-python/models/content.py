#설명 스크립트 저장 모델
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from db.db_connector import Base
from datetime import datetime


class Content(Base):
    __tablename__ = "content"
    content_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.project_id"))
    plan_id = Column(Integer, ForeignKey("plan.plan_id"))
    contentType = Column(String(50)) 
    data = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    submitted_at = Column(DateTime)