from database import SessionLocal, engine
import models
import os

# Create tables
print("Creating tables for SQLite database...")
models.Base.metadata.create_all(bind=engine)

# Inject Dummy API Key
db = SessionLocal()
try:
    existing_key = db.query(models.APIKey).filter(models.APIKey.key == "test_api_key").first()
    if not existing_key:
        print("Injecting test_api_key for simulated traffic...")
        # create a dummy user
        user = models.User(username="admin", hashed_password="not_needed_for_mvp")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        api_key = models.APIKey(user_id=user.id, key="test_api_key")
        db.add(api_key)
        db.commit()
        print("API Key injected successfully.")
    else:
        print("API Key already exists.")
finally:
    db.close()
