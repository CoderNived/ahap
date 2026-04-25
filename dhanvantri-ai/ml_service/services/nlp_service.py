import spacy
from typing import List, Dict, Any

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ─── Medical Keywords Dictionary ──────────────────────────
SYMPTOM_KEYWORDS = [
    "pain", "ache", "fever", "cough", "headache", "dizziness",
    "nausea", "vomiting", "fatigue", "weakness", "swelling",
    "rash", "itching", "bleeding", "bruising", "numbness",
    "tingling", "shortness", "breath", "chest", "palpitations",
    "anxiety", "depression", "insomnia", "diarrhea", "constipation",
    "bloating", "cramps", "inflammation", "infection", "discharge"
]

BODY_PARTS = [
    "head", "neck", "chest", "back", "stomach", "abdomen",
    "arm", "leg", "knee", "ankle", "shoulder", "elbow", "wrist",
    "hand", "foot", "eye", "ear", "nose", "throat", "skin",
    "heart", "lung", "liver", "kidney", "spine", "muscle", "joint"
]

DURATION_KEYWORDS = [
    "day", "days", "week", "weeks", "month", "months",
    "hour", "hours", "morning", "night", "since", "ago"
]

SEVERITY_KEYWORDS = {
    "mild": ["mild", "slight", "minor", "little", "small"],
    "moderate": ["moderate", "medium", "some", "considerable"],
    "severe": ["severe", "intense", "extreme", "terrible", "worst",
               "unbearable", "excruciating", "sharp", "strong"]
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

# ─── Main Extraction Pipeline ─────────────────────────────
def extract_medical_entities(text: str) -> Dict[str, Any]:
    symptoms = extract_symptoms(text)
    body_parts = extract_body_parts(text)
    duration = extract_duration(text)
    severity = extract_severity(text)

    return {
        "symptoms": symptoms,
        "body_parts": body_parts,
        "duration": duration,
        "severity": severity,
        "word_count": len(text.split()),
        "has_medical_content": len(symptoms) > 0 or len(body_parts) > 0,
    }