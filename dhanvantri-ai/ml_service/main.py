from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.cv import router as cv_router
from routers.nlp import router as nlp_router
from routers.forecast import router as forecast_router
from dotenv import load_dotenv
from routers.orchestrate import router as orchestrate_router
import os

load_dotenv('../.env')

app = FastAPI(
    title="Dhanvantri AI - ML Service",
    description="ML microservice for NLP, Computer Vision, and Forecasting",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Register Routers ──────────────────────────────────────
app.include_router(nlp_router, prefix="/api/nlp", tags=["NLP"])
app.include_router(cv_router, prefix="/api/cv", tags=["Computer Vision"])
app.include_router(forecast_router, prefix="/api/forecast", tags=["Forecasting"])
app.include_router(orchestrate_router, prefix="/api/orchestrate", tags=["Orchestration"])
# ─── Health Route ──────────────────────────────────────────
@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "service": "dhanvantri-ml",
        "environment": os.getenv("NODE_ENV", "development")
    }

@app.get("/")
async def root():
    return {
        "message": "Dhanvantri ML Service is running"
    }