from fastapi import FastAPI
from .routers import interpret

app = FastAPI(title="MedIQ Consent Intelligence Service")

app.include_router(interpret.router)

@app.get("/")
def read_root():
    return {"message": "MedIQ Consent Intelligence Service is running"}
