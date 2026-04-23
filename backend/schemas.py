from pydantic import BaseModel
from typing import Optional

class LogIngest(BaseModel):
    ip_address: str
    endpoint: str
    method: str
    payload: Optional[str] = None
    headers: Optional[str] = None

class ThreatAnalysis(BaseModel):
    threat_type: str
    severity: str
