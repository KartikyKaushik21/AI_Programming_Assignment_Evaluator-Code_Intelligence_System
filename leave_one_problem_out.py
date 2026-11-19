
from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)


CATEGORIES = [
    "No Error",
    "Wrong Answer",
    "Runtime Error"
]


def create_model():

    return RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )


def main():

    Path("reports").mkdir(exist_ok=True)

    features = pd.read_csv("data/synthetic_features.csv")
    results = pd.read_csv("data/synthetic_execution_results.csv")

    data = features.merge(
        results,
        on="submission_id",
        validate="one_to_one"
    )

    # Remove Syntax Error because AST handles it separately
    data = data[
        data["error_category"].isin(CATEGORIES)
    ].copy()

    feature_cols = [
        col for col in features.columns
        if col not in ["submission_id", "problem_id"]
    ]

    all_predictions = []
    fold_results = []

    problem_ids = sorted(data["problem_id"].unique())

    print("LEAVE-ONE-PROBLEM-OUT VALIDATION")
    print("=" * 55)

    for problem_id in problem_ids:

        train_data = data[
            data["problem_id"] != problem_id
        ]

        test_data = data[
            data["problem_id"] == problem_id
        ]

        X_train = train_data[feature_cols]
        y_train = train_data["error_category"]

        X_test = test_data[feature_cols]
        y_test = test_data["error_category"]

        model = create_model()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        # Derive pass/fail from error category
        actual_pass = (y_test == "No Error").astype(int)
        predicted_pass = (
            pd.Series(predictions, index=y_test.index) == "No Error"
        ).astype(int)

        error_accuracy = accuracy_score(y_test, predictions)
        pass_accuracy = accuracy_score(actual_pass, predicted_pass)

        error_f1 = f1_score(
            y_test,
            predictions,
            labels=CATEGORIES,
            average="macro",
            zero_division=0
        )

        pass_f1 = f1_score(
            actual_pass,
            predicted_pass,
            zero_division=0
        )

        print(f"\nProblem: {problem_id}")
        print("Test samples:", len(test_data))
        print("Error category accuracy:", round(error_accuracy, 4))
        print("Pass/fail accuracy:", round(pass_accuracy, 4))

        fold_results.append({
            "problem_id": problem_id,
            "test_submissions": len(test_data),
            "error_category_accuracy": error_accuracy,
            "error_category_macro_f1": error_f1,
            "pass_fail_accuracy": pass_accuracy,
            "pass_fail_f1": pass_f1
        })

        fold_output = test_data.copy()
        fold_output["predicted_error_category"] = predictions
        fold_output["predicted_pass"] = predicted_pass.values

        all_predictions.append(fold_output)

    # Combine all held-out predictions
    final_predictions = pd.concat(
        all_predictions,
        ignore_index=True
    )

    final_predictions.to_csv(
        "reports/lopo_predictions.csv",
        index=False
    )

    fold_df = pd.DataFrame(fold_results)

    fold_df.to_csv(
        "reports/lopo_fold_results.csv",
        index=False
    )

    # Overall metrics
    actual_error = final_predictions["error_category"]
    predicted_error = final_predictions["predicted_error_category"]

    actual_pass = (actual_error == "No Error").astype(int)
    predicted_pass = final_predictions["predicted_pass"]

    print("\n\nOVERALL LOPO RESULTS")
    print("=" * 55)

    print("\nERROR CATEGORY")
    print("Accuracy:", round(
        accuracy_score(actual_error, predicted_error), 4
    ))

    print("Macro F1:", round(
        f1_score(
            actual_error,
            predicted_error,
            labels=CATEGORIES,
            average="macro",
            zero_division=0
        ), 4
    ))

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

    print("\nPASS / FAIL")
    print("Accuracy:", round(
        accuracy_score(actual_pass, predicted_pass), 4
    ))

    print("F1 Score:", round(
        f1_score(actual_pass, predicted_pass, zero_division=0), 4
    ))

    print("\nAverage per-problem error accuracy:",
          round(fold_df["error_category_accuracy"].mean(), 4))

    print("Average per-problem pass/fail accuracy:",
          round(fold_df["pass_fail_accuracy"].mean(), 4))

    summary = {
        "total_test_submissions": len(final_predictions),
        "number_of_problems": len(problem_ids),
        "error_category_accuracy": float(
            accuracy_score(actual_error, predicted_error)
        ),
        "error_category_macro_f1": float(
            f1_score(
                actual_error,
                predicted_error,
                labels=CATEGORIES,
                average="macro",
                zero_division=0
            )
        ),
        "pass_fail_accuracy": float(
            accuracy_score(actual_pass, predicted_pass)
        ),
        "pass_fail_f1": float(
            f1_score(actual_pass, predicted_pass, zero_division=0)
        ),
        "average_problem_error_accuracy": float(
            fold_df["error_category_accuracy"].mean()
        ),
        "average_problem_pass_fail_accuracy": float(
            fold_df["pass_fail_accuracy"].mean()
        )
    }

    with open("reports/lopo_evaluation.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\nSaved:")
    print("reports/lopo_predictions.csv")
    print("reports/lopo_fold_results.csv")
    print("reports/lopo_evaluation.json")


if __name__ == "__main__":
    main()
