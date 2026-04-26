from fastapi import APIRouter, HTTPException, UploadFile, File
from services.cv_service import analyze_medical_image

router = APIRouter()

# ─── CV Analysis Route ─────────────────────────────────────
@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/tiff", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Only JPEG, PNG, TIFF, BMP allowed."
        )

    # Validate file size (max 20MB)
    image_bytes = await file.read()
    if len(image_bytes) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 20MB."
        )

    try:
        result = analyze_medical_image(image_bytes)

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"CV analysis failed: {result['error']}"
            )

        return {
            "status": "success",
            "data": {
                "filename": file.filename,
                "content_type": file.content_type,
                "size_bytes": len(image_bytes),
                "analysis": result,
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )