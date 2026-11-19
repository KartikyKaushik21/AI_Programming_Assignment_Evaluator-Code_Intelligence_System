
import os
import json
import joblib
import pandas as pd


def load_models():
    base_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models"
    )

    model_path = os.path.join(base_dir, "error_classifier.joblib")
    columns_path = os.path.join(base_dir, "feature_columns.json")

    if not os.path.exists(model_path) or not os.path.exists(columns_path):
        return None, None

    model = joblib.load(model_path)

    with open(columns_path, "r") as file:
        feature_cols = json.load(file)

    return model, feature_cols


def predict_submission(features_dict, model, feature_cols):
    if model is None or feature_cols is None:
        return None, 0.0

    # Keep the same feature order used during training.
    df = pd.DataFrame([features_dict]).reindex(
        columns=feature_cols,
        fill_value=0
    )

    prediction = model.predict(df)[0]

    probabilities = model.predict_proba(df)[0]
    confidence = float(max(probabilities))

    return prediction, confidence
