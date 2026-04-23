import os
import google.generativeai as genai
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import models

load_dotenv()

# Load key securely from the hidden .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=GEMINI_API_KEY)

def analyze_threat(threat_id: int, db: Session):
    try:
        threat = db.query(models.ThreatEvent).filter(models.ThreatEvent.id == threat_id).first()
        if not threat:
            return
            
        log_entry = db.query(models.logEntry).filter(models.logEntry.id == threat.log_id).first()
        if not log_entry:
            return
        
        prompt = f"""
        Analyze this security threat event for a web application and provide a short, human-readable explanation and suggested fix.
        Threat Type: {threat.threat_type}
        Severity: {threat.severity}
        Endpoint: {log_entry.endpoint}
        Method: {log_entry.method}
        Payload: {log_entry.payload}
        Headers: {log_entry.headers}
        IP Address: {log_entry.ip_address}
        
        Provide the response in 2-3 sentences. Identify why it is a threat and what the developer should do about it.
        """
        
        if GEMINI_API_KEY == "" or not GEMINI_API_KEY:
            # Mock response for testing
            analysis_text = f"Mock AI Analysis: This appears to be a {threat.threat_type} attack targeting the {log_entry.endpoint} endpoint. To fix this, validate and sanitize all inputs and use parameterized queries."
        else:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            analysis_text = response.text
            
        threat.ai_analysis = analysis_text
        db.commit()
    except Exception as e:
        error_msg = str(e)
        print(f"Failed to analyze threat: {error_msg}")
        try:
            # Let the user see exactly why it failed on the dashboard
            threat.ai_analysis = f"AI Error: {error_msg[:150]}..."
            db.commit()
        except:
            pass
