# backend-python/models/concept.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db_connector import Base

class Concept(Base):
    __tablename__ = "concept"

    concept_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey("plan.plan_id"), nullable=False)
    concept_text = Column(String(2000), nullable=False)

