from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.db_connector import Base

class Rulebook(Base):
    __tablename__ = "rulebook"

    rulebook_id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plan.plan_id"))
    
    # 새로 추가할 9개 필드
    title = Column(String(255))
    intro = Column(Text)
    components = Column(Text)
    age = Column(String(50))
    setup = Column(Text)
    rule_set = Column(Text)
    progress = Column(Text)
    win_condition = Column(Text)
    turn_order = Column(Text)

    created_at = Column(DateTime)

    plan = relationship("Plan")
