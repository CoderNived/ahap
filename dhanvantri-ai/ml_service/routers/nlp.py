from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.nlp_service import extract_medical_entities

router = APIRouter()

# ─── Request Model ─────────────────────────────────────────
class TextInput(BaseModel):
    text: str

# ─── NLP Analysis Route ────────────────────────────────────
@router.post("/analyze")
async def analyze_text(input: TextInput):
    if not input.text or len(input.text.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Text input is required"
        )

    if len(input.text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Please provide more detail — minimum 10 characters"
        )

    try:
        result = extract_medical_entities(input.text)

        return {
            "status": "success",
            "data": {
                "input": input.text,
                "entities": result,
                "disclaimer": "⚠️ This is not a medical diagnosis. Please consult a healthcare professional.",
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"NLP processing failed: {str(e)}"
        )