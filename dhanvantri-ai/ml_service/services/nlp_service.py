import spacy
from typing import List, Dict, Any

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ─── Expanded Medical Keywords ─────────────────────────────
SYMPTOM_KEYWORDS = [
    # General
    "pain", "ache", "fever", "cough", "headache", "dizziness",
    "nausea", "vomit", "fatigue", "weakness", "swelling",
    "rash", "itch", "bleeding", "bruising", "numbness",
    "tingling", "shortness", "breath", "palpitation",
    "anxiety", "depression", "insomnia", "diarrhea", "constipation",
    "bloating", "cramp", "inflammation", "infection", "discharge",
    # Expanded
    "blur", "vision", "sneeze", "congestion", "runny",
    "sore", "stiff", "burn", "pressure", "tightness",
    "tremor", "seizure", "faint", "syncope", "confusion",
    "memory", "concentration", "appetite", "weight", "thirst",
    "urination", "dehydration", "pallor", "jaundice", "edema",
    "wheeze", "phlegm", "mucus", "abscess", "ulcer", "lesion"
]

BODY_PARTS = [
    # Core
    "head", "neck", "chest", "back", "stomach", "abdomen",
    "arm", "leg", "knee", "ankle", "shoulder", "elbow", "wrist",
    "hand", "foot", "eye", "ear", "nose", "throat", "skin",
    "heart", "lung", "liver", "kidney", "spine", "muscle", "joint",
    # Expanded
    "brain", "temple", "forehead", "jaw", "tooth", "teeth",
    "tongue", "lip", "gum", "chin", "cheek", "scalp",
    "hip", "thigh", "calf", "heel", "toe", "finger", "thumb",
    "nail", "groin", "pelvis", "bladder", "bowel", "colon",
    "pancreas", "thyroid", "adrenal", "ovary", "uterus", "prostate"
]

DURATION_KEYWORDS = [
    "day", "days", "week", "weeks", "month", "months",
    "hour", "hours", "morning", "night", "since", "ago",
    "yesterday", "today", "recently", "chronic", "acute",
    "sudden", "gradual", "intermittent", "constant", "persistent"
]

SEVERITY_KEYWORDS = {
    "mild": ["mild", "slight", "minor", "little", "small", "barely", "occasionally"],
    "moderate": ["moderate", "medium", "some", "considerable", "noticeable", "frequent"],
    "severe": ["severe", "intense", "extreme", "terrible", "worst",
               "unbearable", "excruciating", "sharp", "strong",
               "acute", "critical", "serious", "alarming"]
}

# ─── Extract Symptoms ──────────────────────────────────────
def extract_symptoms(text: str) -> List[str]:
    doc = nlp(text.lower())
    symptoms = []
    for token in doc:
        if token.lemma_ in SYMPTOM_KEYWORDS and token.lemma_ not in symptoms:
            symptoms.append(token.lemma_)
    return symptoms

# ─── Extract Body Parts ────────────────────────────────────
def extract_body_parts(text: str) -> List[str]:
    doc = nlp(text.lower())
    body_parts = []
    for token in doc:
        if token.lemma_ in BODY_PARTS and token.lemma_ not in body_parts:
            body_parts.append(token.lemma_)
    return body_parts

# ─── Extract Duration ──────────────────────────────────────
def extract_duration(text: str) -> str:
    doc = nlp(text.lower())
    duration_tokens = []
    for token in doc:
        if token.lemma_ in DURATION_KEYWORDS:
            start = max(0, token.i - 2)
            end = min(len(doc), token.i + 2)
            context = doc[start:end].text
            duration_tokens.append(context)
    return duration_tokens[0] if duration_tokens else "not specified"

# ─── Extract Severity ──────────────────────────────────────
def extract_severity(text: str) -> str:
    text_lower = text.lower()
    for level, keywords in SEVERITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return level
    return "not specified"

# ─── Calculate Confidence Score ────────────────────────────
def calculate_confidence(
    symptoms: List[str],
    body_parts: List[str],
    duration: str,
    severity: str,
    word_count: int
) -> float:
    score = 0.0

    # Symptoms found — most important signal
    if len(symptoms) >= 3:
        score += 0.4
    elif len(symptoms) == 2:
        score += 0.3
    elif len(symptoms) == 1:
        score += 0.2

    # Body parts found
    if len(body_parts) >= 2:
        score += 0.2
    elif len(body_parts) == 1:
        score += 0.1

    # Duration specified
    if duration != "not specified":
        score += 0.2

    # Severity specified
    if severity != "not specified":
        score += 0.1

    # Sufficient detail
    if word_count >= 20:
        score += 0.1

    return round(min(score, 1.0), 2)

# ─── Main Extraction Pipeline ─────────────────────────────
def extract_medical_entities(text: str) -> Dict[str, Any]:
    symptoms = extract_symptoms(text)
    body_parts = extract_body_parts(text)
    duration = extract_duration(text)
    severity = extract_severity(text)
    word_count = len(text.split())

    confidence = calculate_confidence(
        symptoms, body_parts, duration, severity, word_count
    )

    return {
        "symptoms": symptoms,
        "body_parts": body_parts,
        "duration": duration,
        "severity": severity,
        "word_count": word_count,
        "has_medical_content": len(symptoms) > 0 or len(body_parts) > 0,
        "confidence": confidence,
    }