
import random
from pathlib import Path

import pandas as pd

from src.problem_bank import PROBLEMS
from src.feature_extractor import extract_features
from src.execution_engine import execute_submission


CATEGORIES = [
    "No Error",
    "Wrong Answer",
    "Runtime Error",
    "Syntax Error"
]

WEIGHTS = [0.40, 0.30, 0.15, 0.15]


def vary_code(code, rng):
    """Add harmless formatting variations."""

    prefix = ""

    if rng.random() < 0.35:
        prefix = "# generated student submission\n"

    suffix = ""

    if rng.random() < 0.35:
        suffix = f"\n# harmless variation {rng.randrange(100000)}\n"

    return prefix + code + suffix



def create_runtime_code(problem, rng):
    """
    Generate runtime errors inside the original function.
    """

    entry = problem["entry_point"]

    runtime_bodies = [
        "return 1 / 0",
        "return int('not_a_number')",
        "return [][0]",
        "return {}['missing_key']"
    ]

    body = rng.choice(runtime_bodies)

    original_code = rng.choice(problem["correct"])

    # Replace the original function body with a runtime fault.
    lines = original_code.splitlines()

    function_line = lines[0]

    code = function_line + "\n    " + body

    return code



def create_syntax_error(problem, rng):
    """Generate different syntax-error patterns."""

    code = rng.choice(problem["correct"])

    syntax_errors = [
        "\n\ndef broken_function(:\n    pass",
        "\nif True\n    pass",
        "\ndef broken_function()\n    return 10"
    ]

    return code + rng.choice(syntax_errors)


def create_code(problem, requested, rng):

    if requested == "No Error":
        code = rng.choice(problem["correct"])

    elif requested == "Wrong Answer":
        code = rng.choice(problem["wrong"])

    elif requested == "Runtime Error":
        code = create_runtime_code(problem, rng)

    elif requested == "Syntax Error":
        code = create_syntax_error(problem, rng)

    else:
        raise ValueError(f"Unsupported category: {requested}")

    return vary_code(code, rng)


def validate_problem_bank():
    """
    Check that every correct template passes and
    every wrong template fails the supplied tests.
    """

    print("\nValidating problem bank...")

    errors = []

    for pid, problem in PROBLEMS.items():

        for index, code in enumerate(problem["correct"]):

            result = execute_submission(
                code,
                problem["entry_point"],
                problem["tests"]
            )

            if result != "No Error":
                errors.append(
                    f"{pid}: correct template {index} returned {result}"
                )

        for index, code in enumerate(problem["wrong"]):

            result = execute_submission(
                code,
                problem["entry_point"],
                problem["tests"]
            )

            if result != "Wrong Answer":
                errors.append(
                    f"{pid}: wrong template {index} returned {result}"
                )

        # Validate generated runtime-error examples
        for seed in range(3):

            rng = random.Random(seed)

            code = create_runtime_code(problem, rng)

            result = execute_submission(
                code,
                problem["entry_point"],
                problem["tests"]
            )

            if result != "Runtime Error":
                errors.append(
                    f"{pid}: runtime template returned {result}"
                )

        # Validate generated syntax-error examples
        for seed in range(3):

            rng = random.Random(seed)

            code = create_syntax_error(problem, rng)

            result = execute_submission(
                code,
                problem["entry_point"],
                problem["tests"]
            )

            if result != "Syntax Error":
                errors.append(
                    f"{pid}: syntax template returned {result}"
                )

    if errors:

        print("\nPROBLEM BANK VALIDATION FAILED:")

        for error in errors:
            print("-", error)

        raise ValueError(
            "Fix the problem bank before generating the dataset."
        )

    print("Problem bank validation successful!")


def generate(total=10000, seed=42):

    rng = random.Random(seed)

    Path("data").mkdir(exist_ok=True)

    validate_problem_bank()

    ids = list(PROBLEMS.keys())

    submissions = []
    feature_rows = []
    labels = []

    requested_counts = {category: 0 for category in CATEGORIES}

    for i in range(total):

        pid = ids[i % len(ids)]

        problem = PROBLEMS[pid]

        requested = rng.choices(
            CATEGORIES,
            weights=WEIGHTS,
            k=1
        )[0]

        code = create_code(problem, requested, rng)

        actual = execute_submission(
            code,
            problem["entry_point"],
            problem["tests"]
        )

        sid = i + 1

        requested_counts[requested] += 1

        submissions.append({
            "submission_id": sid,
            "problem_id": pid,
            "requested_category": requested,
            "code": code
        })

        feature_rows.append({
            "submission_id": sid,
            "problem_id": pid,
            **extract_features(code)
        })

        labels.append({
            "submission_id": sid,
            "will_pass": int(actual == "No Error"),
            "error_category": actual,
            "requested_category": requested,
            "is_simulated": True
        })

    submissions_df = pd.DataFrame(submissions)
    features_df = pd.DataFrame(feature_rows)
    results_df = pd.DataFrame(labels)

    # Save generated files
    submissions_df.to_csv(
        "data/synthetic_submissions.csv",
        index=False
    )

    features_df.to_csv(
        "data/synthetic_features.csv",
        index=False
    )

    results_df.to_csv(
        "data/synthetic_execution_results.csv",
        index=False
    )

    # Report results
    print("\nDataset generation completed.")

    print("\nTotal records:", len(results_df))

    print("\nRequested category distribution:")
    print(results_df["requested_category"].value_counts())

    print("\nActual execution category distribution:")
    print(results_df["error_category"].value_counts())

    # Verify requested and actual labels match
    mismatches = results_df[
        results_df["requested_category"]
        != results_df["error_category"]
    ]

    print("\nLabel mismatches:", len(mismatches))

    if len(mismatches) > 0:
        print("\nMismatched examples:")
        print(mismatches.head(10))

        raise ValueError(
            "Some generated labels do not match requested categories."
        )

    print("\nUnique code snippets:",
          submissions_df["code"].nunique())

    print("\nAll generated labels match their requested categories.")


if __name__ == "__main__":
    generate()
