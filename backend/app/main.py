from fastapi import FastAPI, Request
import time

# Routers
from app.routes import auth, logs

# Detection
from app.services.detector import detect_attack

# Database
from app.models.db import SessionLocal, engine, Base
from app.models import log_model
from app.models.log_model import Log

# Create tables (run once, safe to keep for now)
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Include routes
app.include_router(auth.router)
app.include_router(logs.router)


@app.get("/")
def home():
    return {"message": "AutoSec AI Running 🚀"}


#Middleware: Logging + Detection + Storage
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Read request body
    body = await request.body()
    payload = body.decode(errors="ignore")

    # Detect attack
    attack_type = detect_attack(payload)

    # Prepare log data
    log_data = {
        "ip": request.client.host if request.client else "unknown",
        "path": request.url.path,
        "method": request.method,
        "payload": payload,
        "attack_type": attack_type
    }

    print("LOG:", log_data)

    # Store in DB
    try:
        db = SessionLocal()

        log_entry = Log(
            ip=log_data["ip"],
            path=log_data["path"],
            method=log_data["method"],
            payload=log_data["payload"],
            attack_type=log_data["attack_type"]
        )

        db.add(log_entry)
        db.commit()

    except Exception as e:
        print("DB ERROR:", e)

    finally:
        db.close()

    # Continue request
    response = await call_next(request)

    # Timing
    process_time = time.time() - start_time
    print(f"Processed in {process_time:.4f} sec")

    return response