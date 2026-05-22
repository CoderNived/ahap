from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
from services.orchestrator import run_orchestration_pipeline
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
router = APIRouter()

# ─── Unified Orchestration Route ──────────────────────────
@router.post("/analyze")
async def orchestrate(
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    vitals: Optional[UploadFile] = File(None),
):
    # Validate at least one input provided
    if not text and not image and not vitals:
        raise HTTPException(
            status_code=400,
            detail="At least one input required: text, image, or vitals CSV"
        )

    try:
        # Read file bytes if provided
        image_bytes = None
        vitals_bytes = None

        if image:
            allowed_image_types = [
                "image/jpeg", "image/png",
                "image/tiff", "image/bmp"
            ]
            if image.content_type not in allowed_image_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image type: {image.content_type}"
                )
            image_bytes = await image.read()

        if vitals:
            allowed_csv_types = [
                "text/csv", "text/plain",
                "application/csv", "application/vnd.ms-excel",
                "application/octet-stream"
            ]
            if vitals.content_type not in allowed_csv_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid vitals file type: {vitals.content_type}"
                )
            vitals_bytes = await vitals.read()

        # Run full orchestration pipeline
        result = await run_orchestration_pipeline(
            text=text,
            image_bytes=image_bytes,
            vitals_bytes=vitals_bytes
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Orchestration failed")
            )

        return {
            "status": "success",
            "data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Orchestration error: {str(e)}"
        )