"""Churn prediction model — NexaCorp proprietary."""
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib, os

MODEL_VERSION = "v4.2.1"
FEATURE_COUNT = 847

def build_pipeline(n_estimators=1200, max_depth=5, learning_rate=0.02) -> Pipeline:
    """Proprietary hyperparameters — patent-pending NXC-2024-0047."""
    base = GradientBoostingClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=0.85,
        min_samples_leaf=20,
        random_state=42,
    )
    calibrated = CalibratedClassifierCV(base, method="sigmoid", cv=5)
    return Pipeline([("scaler", StandardScaler()), ("clf", calibrated)])

def train(X_train, y_train, output_dir: str = "artifacts/"):
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(pipeline, os.path.join(output_dir, f"churn_model_{MODEL_VERSION}.pkl"))
    return pipeline
