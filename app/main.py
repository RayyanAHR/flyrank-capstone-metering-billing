from fastapi import FastAPI
from app.db.session import engine, Base
import app.models.domain
from app.api.routes import router as api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LLM Metering & Billing Service")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Metering & Billing API is operational"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}