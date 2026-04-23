from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database, engine, dashboard_apis

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="HackTrack API Gateway")

# Allow Frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_apis.router)

def verify_api_key(x_api_key: str = Header(...), db: Session = Depends(database.get_db)):
    db_key = db.query(models.APIKey).filter(models.APIKey.key == x_api_key).first()
    if not db_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return db_key

@app.post("/api/v1/ingest")
async def ingest_log(log_data: schemas.LogIngest, background_tasks: BackgroundTasks, api_key: models.APIKey = Depends(verify_api_key), db: Session = Depends(database.get_db)):
    # Save log
    db_log = models.logEntry(
        api_key_id=api_key.id,
        ip_address=log_data.ip_address,
        endpoint=log_data.endpoint,
        method=log_data.method,
        payload=log_data.payload,
        headers=log_data.headers
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    # Run detection engine in background
    # We pass a new db session for the background task to avoid concurrency issues with the current session
    background_tasks.add_task(engine.detect_threats, log_data, database.SessionLocal(), db_log.id)
    
    return {"status": "success", "log_id": db_log.id}

@app.get("/health")
def health_check():
    return {"status": "ok"}
