from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional
from services.nlp_service import extract_medical_entities
from services.forecast_service import run_forecasting_pipeline
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
    }# ─── Model Router ─────────────────────────────────────────
async def route_to_model(
        intent: str,
        text: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
        vitals_bytes: Optional[bytes] = None) -> Dict[str, Any]:

    results = {}

    try:
        # Route to NLP
        if intent == INTENT_TEXT_SYMPTOM and text:
            nlp_result = extract_medical_entities(text)
            results["nlp"] = {
                "success": True,
                "data": nlp_result
            }

        # Route to CV
        elif intent == INTENT_IMAGE_ANALYSIS and image_bytes:
            from services.cv_service import analyze_medical_image
            cv_result = analyze_medical_image(image_bytes)
            results["cv"] = cv_result

        # Route to Forecasting
        elif intent == INTENT_VITALS_FORECAST and vitals_bytes:
            forecast_result = run_forecasting_pipeline(vitals_bytes)
            results["forecast"] = forecast_result

        # General health — NLP only if text provided
        elif intent == INTENT_GENERAL_HEALTH and text:
            nlp_result = extract_medical_entities(text)
            results["nlp"] = {
                "success": True,
                "data": nlp_result
            }

        # Unknown intent
        else:
            results["error"] = "Could not route to appropriate model"

        return {
            "success": True,
            "intent": intent,
            "results": results
        }

    except Exception as e:
        return {
            "success": False,
            "intent": intent,
            "error": str(e),
            "results": {}
        }
# ─── Medical Reasoning Agent ──────────────────────────────
async def medical_reasoning_agent(
        intent: str,
        user_input: str,
        model_results: Dict[str, Any]) -> Dict[str, Any]:

    try:
        llm = get_llm()

        # Build context from model results
        context_parts = []

        if "nlp" in model_results and model_results["nlp"]["success"]:
            nlp_data = model_results["nlp"]["data"]
            context_parts.append(f"""
NLP Analysis:
- Symptoms detected: {', '.join(nlp_data.get('symptoms', [])) or 'none'}
- Body parts: {', '.join(nlp_data.get('body_parts', [])) or 'none'}
- Duration: {nlp_data.get('duration', 'not specified')}
- Severity: {nlp_data.get('severity', 'not specified')}
- Confidence: {nlp_data.get('confidence', 0)}
""")

        if "cv" in model_results and model_results["cv"].get("success"):
            cv_data = model_results["cv"]
            risk = cv_data.get("risk_signal", {})
            context_parts.append(f"""
Image Analysis:
- Risk level: {risk.get('risk_level', 'unknown')}
- Top confidence: {risk.get('top_confidence', 0)}
- Recommendation: {risk.get('recommendation', 'none')}
""")

        if "forecast" in model_results and model_results["forecast"].get("success"):
            forecast_data = model_results["forecast"]
            context_parts.append(f"""
Vitals Forecast:
- Overall risk: {forecast_data.get('overall_risk', 'unknown')}
- Risk assessment: {forecast_data.get('risk_assessment', {})}
- Rows analyzed: {forecast_data.get('data_summary', {}).get('rows_analyzed', 0)}
""")

        context = "\n".join(context_parts) if context_parts else "No model results available."

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Dhanvantri, a careful and empathetic AI health assistant.

STRICT RULES — NEVER VIOLATE:
1. NEVER provide a medical diagnosis
2. NEVER prescribe medications or treatments
3. ALWAYS recommend consulting a healthcare professional
4. Only provide general health observations and information
5. Be empathetic and clear in your communication
6. Always include a disclaimer

Your response must be a JSON object with this exact structure:
{{
    "observations": "2-3 sentences describing what the data suggests",
    "key_findings": ["finding 1", "finding 2", "finding 3"],
    "general_advice": "1-2 sentences of general wellness advice only",
    "urgency_level": "low|medium|high",
    "when_to_seek_help": "specific signs that warrant immediate medical attention",
    "confidence": 0.0,
    "disclaimer": "This analysis is for informational purposes only and does not constitute medical advice."
}}"""),
            ("human", """User reported: {user_input}

Analysis results:
{context}

Provide a careful, non-diagnostic health observation.""")
        ])

        chain = prompt | llm
        result = await chain.ainvoke({
            "user_input": user_input,
            "context": context
        })

        # Parse JSON response
        import json
        response_text = result.content.strip()
        clean = response_text.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean)

        return {
            "success": True,
            "reasoning": parsed
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "reasoning": {
                "observations": "Analysis could not be completed at this time.",
                "key_findings": [],
                "general_advice": "Please consult a healthcare professional.",
                "urgency_level": "unknown",
                "when_to_seek_help": "If you feel unwell, seek medical attention.",
                "confidence": 0.0,
                "disclaimer": "This analysis is for informational purposes only."
            }
        }
# ─── Explainability Agent ─────────────────────────────────
def build_explainability_output(
        intent_result: Dict[str, Any],
        model_results: Dict[str, Any],
        reasoning: Dict[str, Any]) -> Dict[str, Any]:

    # ── Confidence Calculation ─────────────────────────────
    confidence_scores = []

    # Intent confidence
    confidence_scores.append(intent_result.get("confidence", 0.5))

    # NLP confidence
    if "nlp" in model_results and model_results["nlp"].get("success"):
        nlp_confidence = model_results["nlp"]["data"].get("confidence", 0.5)
        confidence_scores.append(nlp_confidence)

    # Reasoning confidence
    if reasoning.get("success"):
        reasoning_confidence = reasoning["reasoning"].get("confidence", 0.5)
        confidence_scores.append(reasoning_confidence)

    overall_confidence = round(
        sum(confidence_scores) / len(confidence_scores), 2
    ) if confidence_scores else 0.0

    # ── Urgency Color Mapping ──────────────────────────────
    urgency_level = reasoning.get("reasoning", {}).get("urgency_level", "unknown")
    urgency_colors = {
        "low":     "#22c55e",   # green
        "medium":  "#f59e0b",   # yellow
        "high":    "#ef4444",   # red
        "unknown": "#94a3b8",   # gray
    }

    # ── Build Explanation Sections ────────────────────────
    sections = []

    # Observations section
    if reasoning.get("success"):
        r = reasoning["reasoning"]
        sections.append({
            "type": "observations",
            "title": "Health Observations",
            "content": r.get("observations", ""),
        })

        if r.get("key_findings"):
            sections.append({
                "type": "findings",
                "title": "Key Findings",
                "content": r.get("key_findings", []),
            })

        sections.append({
            "type": "advice",
            "title": "General Advice",
            "content": r.get("general_advice", ""),
        })

        sections.append({
            "type": "seek_help",
            "title": "When to Seek Medical Help",
            "content": r.get("when_to_seek_help", ""),
        })

    # NLP findings section
    if "nlp" in model_results and model_results["nlp"].get("success"):
        nlp_data = model_results["nlp"]["data"]
        if nlp_data.get("symptoms"):
            sections.append({
                "type": "symptoms_detected",
                "title": "Symptoms Detected",
                "content": nlp_data["symptoms"],
            })
        if nlp_data.get("body_parts"):
            sections.append({
                "type": "body_parts",
                "title": "Body Parts Mentioned",
                "content": nlp_data["body_parts"],
            })

    # Forecast section
    if "forecast" in model_results and model_results["forecast"].get("success"):
        forecast_data = model_results["forecast"]
        sections.append({
            "type": "vitals_risk",
            "title": "Vitals Risk Assessment",
            "content": forecast_data.get("risk_assessment", {}),
        })

    return {
        "intent": intent_result.get("intent"),
        "intent_method": intent_result.get("method"),
        "overall_confidence": overall_confidence,
        "urgency_level": urgency_level,
        "urgency_color": urgency_colors.get(urgency_level, "#94a3b8"),
        "sections": sections,
        "disclaimer": "⚠️ This analysis is for informational purposes only and does not constitute medical advice. Always consult a qualified healthcare professional.",
    }