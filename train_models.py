
from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# Syntax Error is handled separately using AST.
# Timeout is not currently supported by the execution engine.
CATEGORIES = [
    "No Error",
    "Wrong Answer",
    "Runtime Error"
]


def show_report(title, y_true, predictions, labels):

    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)

    print("Accuracy:", round(accuracy_score(y_true, predictions), 4))

    print("Macro Precision:", round(
        precision_score(
            y_true, predictions,
            labels=labels,
            average="macro",
            zero_division=0
        ), 4
    ))

    print("Macro Recall:", round(
        recall_score(
            y_true, predictions,
            labels=labels,
            average="macro",
            zero_division=0
        ), 4
    ))

    print("Macro F1:", round(
        f1_score(
            y_true, predictions,
            labels=labels,
            average="macro",
            zero_division=0
        ), 4
    ))

    print("\nClassification Report:")
    print(classification_report(
        y_true,
        predictions,
        labels=labels,
        zero_division=0
    ))

    print("Confusion Matrix:")
    print(confusion_matrix(
        y_true,
        predictions,
        labels=labels
    ))


def show_pass_fail_report(title, actual_error, predicted_error):

    actual_pass = (actual_error == "No Error").astype(int)
    predicted_pass = (predicted_error == "No Error").astype(int)

    show_report(
        title,
        actual_pass,
        predicted_pass,
        [0, 1]
    )


def train():

    Path("models").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    # Load dataset
    features = pd.read_csv("data/synthetic_features.csv")
    results = pd.read_csv("data/synthetic_execution_results.csv")

    data = features.merge(
        results,
        on="submission_id",
        validate="one_to_one"
    )

    # Keep only categories handled by ML
    original_count = len(data)

    data = data[
        data["error_category"].isin(CATEGORIES)
    ].copy()

    excluded = original_count - len(data)

    print("Total records:", original_count)
    print("Records used for ML:", len(data))
    print("Syntax Error records excluded:", excluded)

    if data.empty:
        raise ValueError("No valid records available for training.")

    # Features must not contain labels or identifiers
    feature_cols = [
        col for col in features.columns
        if col not in ["submission_id", "problem_id"]
    ]

    X = data[feature_cols]
    y = data["error_category"]

    print("\nTraining category distribution:")
    print(y.value_counts())

    # ------------------------------------------------
    # 1. RANDOM HOLDOUT
    # ------------------------------------------------

    train_idx, test_idx = train_test_split(
        range(len(data)),
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X.iloc[train_idx],
        y.iloc[train_idx]
    )

    predictions = model.predict(X.iloc[test_idx])

    show_report(
        "RANDOM HOLDOUT - ERROR CATEGORY",
        y.iloc[test_idx],
        predictions,
        CATEGORIES
    )

    show_pass_fail_report(
        "RANDOM HOLDOUT - DERIVED PASS / FAIL",
        y.iloc[test_idx],
        predictions
    )

    # Save holdout data
    data.iloc[test_idx].to_csv(
        "data/holdout_test.csv",
        index=False
    )

    # Save final model
    joblib.dump(
        model,
        "models/error_classifier.joblib"
    )

    with open("models/feature_columns.json", "w") as f:
        json.dump(feature_cols, f, indent=2)

    # ------------------------------------------------
    # 2. GROUPED HOLDOUT - UNSEEN PROBLEMS
    # ------------------------------------------------

    print("\n\nTESTING GENERALIZATION ON UNSEEN PROBLEMS")

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=42
    )

    group_train_idx, group_test_idx = next(
        splitter.split(
            X,
            y,
            groups=data["problem_id"]
        )
    )

    group_model = RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    group_model.fit(
        X.iloc[group_train_idx],
        y.iloc[group_train_idx]
    )

    group_predictions = group_model.predict(
        X.iloc[group_test_idx]
    )

    show_report(
        "GROUPED HOLDOUT - ERROR CATEGORY",
        y.iloc[group_test_idx],
        group_predictions,
        CATEGORIES
    )

    show_pass_fail_report(
        "GROUPED HOLDOUT - DERIVED PASS / FAIL",
        y.iloc[group_test_idx],
        group_predictions
    )

    # Save grouped predictions
    grouped_results = data.iloc[group_test_idx].copy()

    grouped_results["predicted_error_category"] = group_predictions
    grouped_results["predicted_pass"] = (
        grouped_results["predicted_error_category"] == "No Error"
    ).astype(int)

    grouped_results.to_csv(
        "reports/grouped_predictions.csv",
        index=False
    )

    # Save grouped evaluation
    grouped_info = {
        "held_out_problem_ids": sorted(
            data.iloc[group_test_idx]["problem_id"].unique().tolist()
        ),
        "training_problem_ids": sorted(
            data.iloc[group_train_idx]["problem_id"].unique().tolist()
        ),
        "error_category_accuracy": float(
            accuracy_score(
                y.iloc[group_test_idx],
                group_predictions
            )
        ),
        "pass_fail_accuracy": float(
            accuracy_score(
                (y.iloc[group_test_idx] == "No Error").astype(int),
                (group_predictions == "No Error").astype(int)
            )
        ),
        "categories": CATEGORIES,
        "syntax_errors_handled_separately": True
    }

    with open("reports/grouped_evaluation.json", "w") as f:
        json.dump(grouped_info, f, indent=2)

    print("\nGrouped evaluation saved successfully.")
    print(grouped_info)


if __name__ == "__main__":
    train()
