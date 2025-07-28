# backend-python/models/role.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.db_connector import Base

class Role(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    users = relationship("User", back_populates="role")
