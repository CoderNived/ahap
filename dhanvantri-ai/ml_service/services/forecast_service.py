import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Dict, Any, Tuple, List
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