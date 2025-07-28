from sqlalchemy import Column, Integer, String, Text
from db.db_connector import Base

class Plan(Base):
    __tablename__ = "plan"

    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    text = Column(Text)  
