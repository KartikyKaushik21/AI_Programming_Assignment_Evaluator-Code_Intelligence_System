
import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)


CATEGORIES = [
    "No Error",
    "Wrong Answer",
    "Runtime Error"
]


def evaluate():

    Path("reports").mkdir(exist_ok=True)

    # Load saved model
    model = joblib.load("models/error_classifier.joblib")

    with open("models/feature_columns.json", "r") as f:
        feature_cols = json.load(f)

    # Load unseen holdout records
    data = pd.read_csv("data/holdout_test.csv")

    X = data[feature_cols]
    actual_error = data["error_category"]

    # Predict error category
    predicted_error = model.predict(X)

    print("\nERROR CATEGORY EVALUATION")
    print("=" * 50)

    print("Accuracy:",
          round(accuracy_score(actual_error, predicted_error), 4))

    print("\nClassification Report:")
    print(classification_report(
        actual_error,
        predicted_error,
        labels=CATEGORIES,
        zero_division=0
    ))

    print("Confusion Matrix:")
    print(confusion_matrix(
        actual_error,
        predicted_error,
        labels=CATEGORIES
    ))

    # Derive pass/fail from error category
    actual_pass = (actual_error == "No Error").astype(int)
    predicted_pass = (
        pd.Series(predicted_error) == "No Error"
    ).astype(int)

    print("\nPASS / FAIL EVALUATION")
    print("=" * 50)

    print("Accuracy:",
          round(accuracy_score(actual_pass, predicted_pass), 4))

    print("Precision:",
          round(precision_score(actual_pass, predicted_pass, zero_division=0), 4))

    print("Recall:",
          round(recall_score(actual_pass, predicted_pass, zero_division=0), 4))

    print("F1 Score:",
          round(f1_score(actual_pass, predicted_pass, zero_division=0), 4))

    print("\nConfusion Matrix:")
    print(confusion_matrix(actual_pass, predicted_pass, labels=[0, 1]))

    # Save predictions
    data["predicted_error_category"] = predicted_error
    data["predicted_pass"] = predicted_pass

    data.to_csv(
        "reports/test_predictions.csv",
        index=False
    )

    print("\nPredictions saved to reports/test_predictions.csv")


if __name__ == "__main__":
    evaluate()
