from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from db.db_connector import Base
from datetime import datetime

class Rulebook(Base):
    __tablename__ = "rulebook"

    rulebook_id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plan.plan_id"))
    rule_set = Column(Text)
    win_condition = Column(Text)
    turn_order = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)