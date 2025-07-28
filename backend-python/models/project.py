# 예시: models/project.py
from sqlalchemy import Column, Integer, String
from db.db_connector import Base

class Project(Base):
    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
