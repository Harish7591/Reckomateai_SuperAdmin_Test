
from fastapi import FastAPI

from app.routes.organisation import router as organisation_router
app = FastAPI(
    title="Reckomate Backend Automation Sample",
    description="Local organisation branch and Docker automation",
    version="1.0.0",
)

app.include_router(organisation_router)


@app.get("/")
def root():
    return {
        "message": "Reckomate Backend Automation API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "super-admin-backend",
    }
