"""Log routes."""
from fastapi import APIRouter
from app.models.db import SessionLocal
from app.models.log_model import Log

router = APIRouter(prefix="/logs")

@router.get("/")
def get_logs():
    db = SessionLocal()
    logs = db.query(Log).all()
    db.close()
    return logs