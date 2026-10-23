from fastapi import FastAPI

from app.routes.incidents import router as incidents_router

app = FastAPI(
    title="AI Incident Analyzer",
    version="1.0.0"
)

app.include_router(incidents_router)