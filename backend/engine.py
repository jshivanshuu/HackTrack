from sqlalchemy.orm import Session
import models, schemas, ai_service

def detect_threats(log_data: schemas.LogIngest, db: Session, log_id: int):
    try:
        is_threat = False
        threat_type = "None"
        severity = "Low"
        
        payload = log_data.payload or ""
        headers = log_data.headers or ""
        url = log_data.endpoint
        
        # 1. SQL Injection
        sqli_patterns = ["'", "SELECT", "UNION", "--", "DROP"]
        if any(p.lower() in payload.lower() for p in sqli_patterns) or any(p.lower() in url.lower() for p in sqli_patterns):
            is_threat = True
            threat_type = "SQL Injection"
            severity = "High"
        
        # 2. XSS
        xss_patterns = ["<script>", "javascript:", "onerror="]
        if any(p.lower() in payload.lower() for p in xss_patterns) or any(p.lower() in url.lower() for p in xss_patterns):
            is_threat = True
            threat_type = "XSS"
            severity = "Medium"
            
        if is_threat:
            threat = models.ThreatEvent(
                log_id=log_id,
                threat_type=threat_type,
                severity=severity,
                ai_analysis="To be analyzed"
            )
            db.add(threat)
            db.commit()
            db.refresh(threat)
            
            # Call AI Service sequentially since we're already in a background task
            ai_service.analyze_threat(threat.id, db)
    finally:
        db.close()
