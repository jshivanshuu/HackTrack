import time

from fastapi import FastAPI, Request

from app.routes import auth, logs
from app.services.detector import detect_attack

app = FastAPI(title="HackTrack API")

app.include_router(auth.router)
app.include_router(logs.router)

@app.get("/")
def home():
    return {"message": "AutoSec AI Running"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    body = await request.body()

    payload = body.decode(errors="ignore")

    attack_type: str = detect_attack(payload)
    log_data = {
        "ip": request.client.host,
        "path": request.url.path,
        "method": request.method,
        "payload": payload,
        "attack_type": attack_type,
        "body": body.decode(errors="ignore"),
        "headers": dict(request.headers),
    }


    print("LOG:", log_data)

    response = await call_next(request)

    process_time = time.time() - start_time
    print(f"Time taken: {process_time}")

    return response
