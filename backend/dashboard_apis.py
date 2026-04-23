from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
import models, database

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(database.get_db)):
    total_logs = db.query(func.count(models.logEntry.id)).scalar()
    total_threats = db.query(func.count(models.ThreatEvent.id)).scalar()
    
    # Simple count by type
    threats_by_type = db.query(models.ThreatEvent.threat_type, func.count(models.ThreatEvent.id)).group_by(models.ThreatEvent.threat_type).all()
    threats_by_type_dict = [{"name": t[0], "value": t[1]} for t in threats_by_type]
    
    return {
        "total_requests": total_logs,
        "total_threats": total_threats,
        "threats_by_type": threats_by_type_dict
    }

@router.get("/timeline")
def get_threat_timeline(db: Session = Depends(database.get_db), limit: int = 100):
    # Returns recent threats for a timeline view
    recent_threats = db.query(models.ThreatEvent).order_by(models.ThreatEvent.timestamp.desc()).limit(limit).all()
    
    timeline = []
    for threat in recent_threats:
        log = db.query(models.logEntry).filter(models.logEntry.id == threat.log_id).first()
        timeline.append({
            "id": threat.id,
            "timestamp": threat.timestamp,
            "threat_type": threat.threat_type,
            "severity": threat.severity,
            "ip_address": log.ip_address if log else "Unknown",
            "endpoint": log.endpoint if log else "Unknown",
            "ai_analysis": threat.ai_analysis
        })
    return timeline
