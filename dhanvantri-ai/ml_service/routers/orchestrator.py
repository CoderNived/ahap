from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional
import os

# ─── Intent Types ─────────────────────────────────────────
INTENT_TEXT_SYMPTOM = "text_symptom"
INTENT_IMAGE_ANALYSIS = "image_analysis"
INTENT_VITALS_FORECAST = "vitals_forecast"
INTENT_GENERAL_HEALTH = "general_health"
INTENT_UNKNOWN = "unknown"

# ─── Grok LLM Client ──────────────────────────────────────
def get_llm():
    return ChatOpenAI(
        model="grok-3-mini",
        api_key=os.getenv("GROK_API_KEY"),
        base_url=os.getenv("GROK_BASE_URL"),
        temperature=0.1,
    )

# ─── Rule-Based Intent Detection ──────────────────────────
def detect_intent_rules(text: str) -> Optional[str]:
    text_lower = text.lower()

    # Vitals keywords
    vitals_keywords = [
        "heart rate", "blood pressure", "temperature", "spo2",
        "vitals", "csv", "ecg", "pulse", "oxygen"
    ]

    # Image keywords
    image_keywords = [
        "xray", "x-ray", "scan", "mri", "ct scan", "image",
        "photo", "picture", "upload image"
    ]

    # Symptom keywords
    symptom_keywords = [
        "pain", "ache", "fever", "cough", "headache", "dizziness",
        "nausea", "fatigue", "swelling", "rash", "bleeding",
        "symptom", "feel", "feeling", "hurt", "sore", "sick"
    ]

    for keyword in vitals_keywords:
        if keyword in text_lower:
            return INTENT_VITALS_FORECAST

    for keyword in image_keywords:
        if keyword in text_lower:
            return INTENT_IMAGE_ANALYSIS

    for keyword in symptom_keywords:
        if keyword in text_lower:
            return INTENT_TEXT_SYMPTOM

    return None

# ─── LLM-Based Intent Detection ───────────────────────────
async def detect_intent_llm(text: str) -> str:
    try:
        llm = get_llm()

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a medical intent classifier.
Classify the user input into exactly one of these intents:
- text_symptom: user describes symptoms or health complaints
- image_analysis: user mentions medical images, scans, xrays
- vitals_forecast: user mentions vitals data, heart rate, blood pressure
- general_health: general health questions or advice
- unknown: cannot determine intent

Respond with ONLY the intent label, nothing else."""),
            ("human", "{input}")
        ])

        chain = prompt | llm
        result = await chain.ainvoke({"input": text})
        intent = result.content.strip().lower()

        valid_intents = [
            INTENT_TEXT_SYMPTOM, INTENT_IMAGE_ANALYSIS,
            INTENT_VITALS_FORECAST, INTENT_GENERAL_HEALTH,
            INTENT_UNKNOWN
        ]

        return intent if intent in valid_intents else INTENT_UNKNOWN

    except Exception:
        return INTENT_UNKNOWN

# ─── Combined Intent Detection ────────────────────────────
async def detect_intent(text: str) -> Dict[str, Any]:
    # Try rule-based first (fast, free)
    rule_intent = detect_intent_rules(text)

    if rule_intent:
        return {
            "intent": rule_intent,
            "method": "rule_based",
            "confidence": 0.85
        }

    # Fall back to LLM (slower, costs tokens)
    llm_intent = await detect_intent_llm(text)

    return {
        "intent": llm_intent,
        "method": "llm_based",
        "confidence": 0.75 if llm_intent != INTENT_UNKNOWN else 0.0
    }