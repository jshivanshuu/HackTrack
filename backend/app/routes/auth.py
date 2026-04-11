"""Authentication routes."""
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/login")
async def fake_login(request: Request):
    data = await request.json()
    return {"status": "error", "message": "Invalid credentials"}