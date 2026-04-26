from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers.nlp import router as nlp_router
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