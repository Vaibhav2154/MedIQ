from fastapi import FastAPI
from .routers import consent
from .db.session import engine, Base

# Create tables if they don't exist (MVP approach)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MedIQ Consent Ingestion Service")

app.include_router(consent.router)

@app.get("/")
def read_root():
    return {"message": "MedIQ Consent Ingestion Service is running"}
