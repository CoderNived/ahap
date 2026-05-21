from fastapi import APIRouter, HTTPException, UploadFile, File
from services.forecast_service import run_forecasting_pipeline

router = APIRouter()

# ─── Forecast Route ────────────────────────────────────────
@router.post("/analyze")
async def forecast_vitals(
    file: UploadFile = File(...),
    steps: int = 3
):
    # Validate file type
    allowed_types = [
    "text/csv",
    "application/vnd.ms-excel",
    "application/csv",
    "text/plain",
    "application/octet-stream",
    "application/x-csv",
]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Only CSV files allowed."
        )

    # Validate file size (max 5MB)
    file_bytes = await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 5MB."
        )

    # Validate steps
    if steps < 1 or steps > 10:
        raise HTTPException(
            status_code=400,
            detail="Forecast steps must be between 1 and 10."
        )

    try:
        result = run_forecasting_pipeline(file_bytes, forecast_steps=steps)

        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )

        return {
            "status": "success",
            "filename": file.filename,
            "data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Forecasting failed: {str(e)}"
        )