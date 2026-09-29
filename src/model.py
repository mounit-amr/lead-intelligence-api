import joblib
from pathlib import Path

MODEL_PATH = Path("models/lead_model.pkl")

model = joblib.load(MODEL_PATH)

