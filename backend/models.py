from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class logEntry(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    ip_address = Column(String(50))
    endpoint = Column(String(255))
    method = Column(String(10))
    payload = Column(Text, nullable=True)
    headers = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ThreatEvent(Base):
    __tablename__ = "threat_events"
    
    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey("logs.id"))
    threat_type = Column(String(50)) # e.g., "SQLi", "XSS", "Brute Force"
    severity = Column(String(20)) # "Low", "Medium", "High", "Critical"
    ai_analysis = Column(Text, nullable=True) # Text populated by Gemini later
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
