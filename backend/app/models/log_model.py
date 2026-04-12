"""Log model definitions."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.models.db import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    path = Column(String)
    method = Column(String)
    payload = Column(Text)
    attack_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)