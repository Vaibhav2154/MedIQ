from fastapi import FastAPI
from .routers import evaluate

app = FastAPI(title="MedIQ Policy Engine Service")

app.include_router(evaluate.router)

@app.get("/")
def read_root():
    return {"message": "MedIQ Policy Engine Service is running"}
