import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import io
from typing import Dict, Any, List

# ─── Load Pretrained Model ─────────────────────────────────
def load_model():
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
    model.eval()
    return model

# Load model once at startup
model = load_model()

# ─── ImageNet Classes (Top Medical-Relevant) ───────────────
IMAGENET_CATEGORIES = {
    "normal_tissue": list(range(0, 100)),
    "abnormal_pattern": list(range(100, 300)),
    "structural_anomaly": list(range(300, 500)),
    "other": list(range(500, 1000)),
}

# ─── Image Preprocessing Pipeline ─────────────────────────
def preprocess_image(image_bytes: bytes) -> torch.Tensor:
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    tensor = transform(image).unsqueeze(0)
    return tensor

# ─── Run Inference ─────────────────────────────────────────
def run_inference(image_tensor: torch.Tensor) -> torch.Tensor:
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    return probabilities

# ─── Get Top Predictions ───────────────────────────────────
def get_top_predictions(probabilities: torch.Tensor, top_k: int = 5) -> List[Dict]:
    top_probs, top_indices = torch.topk(probabilities, top_k)
    predictions = []
    for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
        predictions.append({
            "class_index": idx,
            "confidence": round(prob, 4),
            "confidence_percent": f"{round(prob * 100, 2)}%"
        })
    return predictions

# ─── Calculate Overall Risk Signal ────────────────────────
def calculate_risk_signal(predictions: List[Dict]) -> Dict[str, Any]:
    top_confidence = predictions[0]["confidence"] if predictions else 0

    if top_confidence > 0.8:
        risk_level = "high_confidence_detection"
        recommendation = "Strong pattern detected. Please consult a specialist."
    elif top_confidence > 0.5:
        risk_level = "moderate_confidence_detection"
        recommendation = "Pattern detected with moderate confidence. Medical review recommended."
    else:
        risk_level = "low_confidence_detection"
        recommendation = "Low confidence detection. Image quality may be affecting results."

    return {
        "risk_level": risk_level,
        "top_confidence": top_confidence,
        "recommendation": recommendation,
    }

# ─── Main CV Pipeline ──────────────────────────────────────
def analyze_medical_image(image_bytes: bytes) -> Dict[str, Any]:
    try:
        # Preprocess
        tensor = preprocess_image(image_bytes)

        # Run inference
        probabilities = run_inference(tensor)

        # Get predictions
        predictions = get_top_predictions(probabilities, top_k=5)

        # Calculate risk signal
        risk_signal = calculate_risk_signal(predictions)

        return {
            "success": True,
            "predictions": predictions,
            "risk_signal": risk_signal,
            "disclaimer": "⚠️ This is not a medical diagnosis. These are pattern detection results only. Please consult a qualified healthcare professional.",
            "model": "EfficientNet-B0 (ImageNet pretrained)",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }