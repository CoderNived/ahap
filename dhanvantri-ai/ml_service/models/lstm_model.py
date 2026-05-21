import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, List, Dict, Any

# ─── LSTM Model Definition ─────────────────────────────────
class VitalsLSTM(nn.Module):
    def __init__(self, input_size: int = 5, hidden_size: int = 64,
                 num_layers: int = 2, output_size: int = 5):
        super(VitalsLSTM, self).__init__()

        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )

        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

# ─── Prepare Sequences ─────────────────────────────────────
def create_sequences(data: np.ndarray,
                     seq_length: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

# ─── Train Model ───────────────────────────────────────────
def train_lstm(scaled_data: np.ndarray,
               epochs: int = 50,
               seq_length: int = 5) -> Tuple[VitalsLSTM, List[float]]:

    # Need at least seq_length + 1 rows
    if len(scaled_data) < seq_length + 1:
        raise ValueError(
            f"Need at least {seq_length + 1} rows of data. Got {len(scaled_data)}."
        )

    X, y = create_sequences(scaled_data, seq_length)

    X_tensor = torch.FloatTensor(X)
    y_tensor = torch.FloatTensor(y)

    input_size = scaled_data.shape[1]
    model = VitalsLSTM(
        input_size=input_size,
        hidden_size=64,
        num_layers=2,
        output_size=input_size
    )

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    losses = []
    model.train()

    for epoch in range(epochs):
        optimizer.zero_grad()
        output = model(X_tensor)
        loss = criterion(output, y_tensor)
        loss.backward()
        optimizer.step()
        losses.append(round(loss.item(), 6))

    model.eval()
    return model, losses

# ─── Generate Forecast ─────────────────────────────────────
def generate_forecast(model: VitalsLSTM,
                      scaled_data: np.ndarray,
                      steps: int = 3,
                      seq_length: int = 5) -> np.ndarray:

    model.eval()
    predictions = []
    current_seq = scaled_data[-seq_length:].copy()

    with torch.no_grad():
        for _ in range(steps):
            x = torch.FloatTensor(current_seq).unsqueeze(0)
            pred = model(x).numpy()[0]
            predictions.append(pred)
            current_seq = np.vstack([current_seq[1:], pred])

    return np.array(predictions)

# ─── Calculate Confidence Intervals ───────────────────────
def calculate_confidence_intervals(
        predictions: np.ndarray,
        noise_factor: float = 0.05) -> Dict[str, np.ndarray]:

    noise = np.abs(predictions) * noise_factor
    return {
        'lower': predictions - noise,
        'upper': predictions + noise,
    }