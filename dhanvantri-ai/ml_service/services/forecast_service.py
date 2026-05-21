import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Dict, Any, Tuple, List
from models.lstm_model import train_lstm, generate_forecast, calculate_confidence_intervals
import io

# ─── Expected Columns ─────────────────────────────────────
REQUIRED_COLUMNS = [
    'timestamp', 'heart_rate', 'blood_pressure_sys',
    'blood_pressure_dia', 'temperature', 'spo2'
]

VITAL_RANGES = {
    'heart_rate':         {'min': 30,  'max': 220},
    'blood_pressure_sys': {'min': 60,  'max': 250},
    'blood_pressure_dia': {'min': 40,  'max': 150},
    'temperature':        {'min': 95,  'max': 107},
    'spo2':               {'min': 70,  'max': 100},
}

# ─── Parse CSV ─────────────────────────────────────────────
def parse_vitals_csv(file_bytes: bytes) -> Tuple[pd.DataFrame, List[str]]:
    warnings = []

    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Could not parse CSV file: {str(e)}")

    # Check required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Parse timestamp
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
    except Exception:
        warnings.append("Could not parse timestamps — using row order instead")

    # Handle missing values
    numeric_cols = [c for c in REQUIRED_COLUMNS if c != 'timestamp']
    missing_count = df[numeric_cols].isnull().sum().sum()
    if missing_count > 0:
        warnings.append(f"Found {missing_count} missing values — filled with column mean")
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Validate ranges
    for col, ranges in VITAL_RANGES.items():
        if col in df.columns:
            out_of_range = ((df[col] < ranges['min']) | (df[col] > ranges['max'])).sum()
            if out_of_range > 0:
                warnings.append(f"{col}: {out_of_range} readings outside normal range")

    return df, warnings

# ─── Calculate Vital Statistics ────────────────────────────
def calculate_vital_stats(df: pd.DataFrame) -> Dict[str, Any]:
    numeric_cols = [c for c in REQUIRED_COLUMNS if c != 'timestamp']
    stats = {}

    for col in numeric_cols:
        if col in df.columns:
            stats[col] = {
                'mean':    round(float(df[col].mean()), 2),
                'min':     round(float(df[col].min()), 2),
                'max':     round(float(df[col].max()), 2),
                'std':     round(float(df[col].std()), 2),
                'latest':  round(float(df[col].iloc[-1]), 2),
            }

    return stats

# ─── Normalize Data for LSTM ───────────────────────────────
def normalize_vitals(df: pd.DataFrame) -> Tuple[np.ndarray, MinMaxScaler]:
    numeric_cols = [c for c in REQUIRED_COLUMNS if c != 'timestamp']
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(df[numeric_cols])
    return scaled, scaler

# ─── Assess Risk Level ─────────────────────────────────────
def assess_vital_risks(stats: Dict[str, Any]) -> Dict[str, str]:
    risks = {}

    if 'heart_rate' in stats:
        hr = stats['heart_rate']['mean']
        if hr < 60 or hr > 100:
            risks['heart_rate'] = 'abnormal'
        else:
            risks['heart_rate'] = 'normal'

    if 'blood_pressure_sys' in stats:
        bp = stats['blood_pressure_sys']['mean']
        if bp >= 140:
            risks['blood_pressure'] = 'high'
        elif bp < 90:
            risks['blood_pressure'] = 'low'
        else:
            risks['blood_pressure'] = 'normal'

    if 'spo2' in stats:
        spo2 = stats['spo2']['mean']
        if spo2 < 95:
            risks['spo2'] = 'low'
        else:
            risks['spo2'] = 'normal'

    if 'temperature' in stats:
        temp = stats['temperature']['mean']
        if temp > 100.4:
            risks['temperature'] = 'fever'
        elif temp < 96.8:
            risks['temperature'] = 'hypothermia_risk'
        else:
            risks['temperature'] = 'normal'

    return risks
# ─── Main Forecasting Pipeline ────────────────────────────
def run_forecasting_pipeline(
        file_bytes: bytes,
        forecast_steps: int = 3) -> Dict[str, Any]:

    try:
        # Step 1 — Parse and validate CSV
        df, warnings = parse_vitals_csv(file_bytes)

        if len(df) < 6:
            return {
                "success": False,
                "error": "Need at least 6 rows of vitals data for forecasting."
            }

        # Step 2 — Calculate statistics
        stats = calculate_vital_stats(df)

        # Step 3 — Assess current risks
        risks = assess_vital_risks(stats)

        # Step 4 — Normalize data
        scaled_data, scaler = normalize_vitals(df)

        # Step 5 — Train LSTM
        model, losses = train_lstm(
            scaled_data,
            epochs=50,
            seq_length=min(5, len(df) - 1)
        )

        # Step 6 — Generate forecast
        seq_length = min(5, len(df) - 1)
        raw_predictions = generate_forecast(
            model, scaled_data,
            steps=forecast_steps,
            seq_length=seq_length
        )

        # Step 7 — Inverse transform predictions back to original scale
        predictions_original = scaler.inverse_transform(raw_predictions)
        intervals = calculate_confidence_intervals(predictions_original)

        # Step 8 — Format predictions
        numeric_cols = [c for c in REQUIRED_COLUMNS if c != 'timestamp']
        formatted_predictions = []

        for i, pred in enumerate(predictions_original):
            step = {}
            for j, col in enumerate(numeric_cols):
                step[col] = {
                    "predicted": round(float(pred[j]), 2),
                    "lower":     round(float(intervals['lower'][i][j]), 2),
                    "upper":     round(float(intervals['upper'][i][j]), 2),
                }
            formatted_predictions.append({
                "step": i + 1,
                "label": f"Next reading {i + 1}",
                "vitals": step
            })

        # Step 9 — Calculate overall trend
        overall_risk = "normal"
        if any(v in ["abnormal", "high", "low", "fever", "hypothermia_risk"]
               for v in risks.values()):
            overall_risk = "attention_needed"

        return {
            "success": True,
            "data_summary": {
                "rows_analyzed": len(df),
                "warnings": warnings,
            },
            "current_stats": stats,
            "risk_assessment": risks,
            "overall_risk": overall_risk,
            "forecast": formatted_predictions,
            "model_info": {
                "type": "LSTM",
                "epochs": 50,
                "final_loss": losses[-1] if losses else None,
                "forecast_steps": forecast_steps,
            },
            "disclaimer": "⚠️ These are statistical trend predictions only. Not a medical diagnosis. Please consult a healthcare professional.",
        }

    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Forecasting failed: {str(e)}"}