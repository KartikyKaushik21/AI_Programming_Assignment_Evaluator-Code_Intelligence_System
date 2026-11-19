
import ast
import json
import os
import subprocess
import sys
import tempfile


# --------------------------------------------------
# DATASET GENERATION
# Use ONLY with trusted synthetic templates.
# --------------------------------------------------

def execute_submission(code, entry_point, tests, timeout_seconds=None):
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError, TypeError):
        return "Syntax Error"

    namespace = {"__builtins__": __builtins__}

    try:
        exec(
            compile(tree, "<synthetic-submission>", "exec"),
            namespace
        )

        function = namespace.get(entry_point)

        if not callable(function):
            return "Runtime Error"

        for case in tests:
            actual = function(*case["args"])
            expected = case["expected"]

            if actual != expected:
                return "Wrong Answer"

        return "No Error"

    except Exception:
        return "Runtime Error"


# --------------------------------------------------
# HELPER: CREATE TEST RESULT
# --------------------------------------------------

def create_test_result(
    index,
    test_input,
    expected,
    actual,
    passed,
    error
):
    return {
        "test": index,
        "input": test_input,
        "status": "Passed" if passed else "Failed",
        "passed": passed,
        "expected": expected,
        "actual": actual,
        "error": error if error else "—"
    }


# --------------------------------------------------
# STREAMLIT APP EXECUTION
# Local prototype only. NOT a security sandbox.
# --------------------------------------------------

def execute_code(code, problem, timeout_seconds=3):

    tests = problem.get("tests", [])

    result = {
        "passed": 0,
        "failed": 0,
        "error_category": "None",
        "stderr": "",
        "tests": []
    }

    # Validate problem configuration.
    entry_point = problem.get("entry_point")

    if not entry_point or not tests:
        result["error_category"] = "Runtime Error"
        result["stderr"] = (
            "Problem configuration is missing entry_point or tests."
        )
        return result

    # Validate syntax before execution.
    try:
        ast.parse(code)

    except SyntaxError as error:

        result["error_category"] = "Syntax Error"
        result["stderr"] = str(error)
        result["failed"] = len(tests)

        for index, case in enumerate(tests, start=1):
            result["tests"].append(
                create_test_result(
                    index,
                    case.get("args", []),
                    case.get("expected"),
                    "Not executed",
                    False,
                    f"Syntax Error: {error}"
                )
            )

        return result

    # Execute student code in a subprocess.
    try:

        with tempfile.TemporaryDirectory() as temp_dir:

            code_path = os.path.join(
                temp_dir, "student_code.py"
            )

            test_path = os.path.join(
                temp_dir, "tests.json"
            )

            runner_path = os.path.join(
                temp_dir, "runner.py"
            )

            output_path = os.path.join(
                temp_dir, "result.json"
            )

            with open(code_path, "w", encoding="utf-8") as file:
                file.write(code)

            with open(test_path, "w", encoding="utf-8") as file:
                json.dump({
                    "entry_point": entry_point,
                    "tests": tests
                }, file)

            # ------------------------------------------
            # RUNNER CODE
            # ------------------------------------------

            runner_code = r'''
import json
import runpy
import sys

code_path, test_path, output_path = sys.argv[1:4]

result = {
    "passed": 0,
    "failed": 0,
    "error_category": "None",
    "stderr": "",
    "tests": []
}

try:
    with open(test_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    namespace = runpy.run_path(code_path)
    function = namespace.get(config["entry_point"])

    for index, case in enumerate(config["tests"], start=1):

        expected = case.get("expected")
        test_input = case.get("args", [])

        # Required function not found.
        if not callable(function):

            actual = "Not executed"
            passed = False

            error = (
                "Runtime Error: Required function "
                "was not found."
            )

            result["error_category"] = "Runtime Error"

        else:

            try:
                actual = function(*test_input)
                passed = actual == expected

                if passed:
                    error = "—"

                else:
                    error = (
                        f"Wrong Answer: Expected {expected!r}, "
                        f"but got {actual!r}"
                    )

                    result["error_category"] = "Wrong Answer"

            except Exception as exception:

                actual = f"Runtime Error: {exception}"
                passed = False

                error = (
                    f"Runtime Error: {type(exception).__name__}: "
                    f"{exception}"
                )

                result["error_category"] = "Runtime Error"
                result["stderr"] = str(exception)

        if passed:
            result["passed"] += 1

        else:
            result["failed"] += 1

        result["tests"].append({
            "test": index,
            "input": test_input,
            "status": "Passed" if passed else "Failed",
            "passed": passed,
            "expected": expected,
            "actual": actual,
            "error": error
        })

except Exception as exception:

    result["error_category"] = "Runtime Error"
    result["stderr"] = str(exception)

    # Record remaining test cases if runner fails.
    if not result["tests"]:

        for index, case in enumerate(
            config.get("tests", []) if "config" in locals() else [],
            start=1
        ):

            result["tests"].append({
                "test": index,
                "input": case.get("args", []),
                "status": "Failed",
                "passed": False,
                "expected": case.get("expected"),
                "actual": "Not executed",
                "error": (
                    f"Runtime Error: {type(exception).__name__}: "
                    f"{exception}"
                )
            })

        result["failed"] = len(result["tests"])

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(result, file, default=str)
'''

            with open(
                runner_path, "w", encoding="utf-8"
            ) as file:
                file.write(runner_code)

            # ------------------------------------------
            # RUN SUBPROCESS
            # ------------------------------------------

            try:

                process = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        runner_path,
                        code_path,
                        test_path,
                        output_path
                    ],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds
                )

            except subprocess.TimeoutExpired:

                result["error_category"] = "Timeout"
                result["stderr"] = (
                    "Execution time limit exceeded."
                )
                result["failed"] = len(tests)

                for index, case in enumerate(tests, start=1):
                    result["tests"].append(
                        create_test_result(
                            index,
                            case.get("args", []),
                            case.get("expected"),
                            "Not executed",
                            False,
                            "Timeout: Execution time limit exceeded."
                        )
                    )

                return result

            # Check whether result file was created.
            if not os.path.exists(output_path):

                error_message = (
                    process.stderr
                    or "Execution process stopped unexpectedly."
                )

                result["error_category"] = "Runtime Error"
                result["stderr"] = error_message
                result["failed"] = len(tests)

                for index, case in enumerate(tests, start=1):
                    result["tests"].append(
                        create_test_result(
                            index,
                            case.get("args", []),
                            case.get("expected"),
                            "Not executed",
                            False,
                            f"Runtime Error: {error_message}"
                        )
                    )

                return result

            # Read execution results.
            with open(
                output_path, "r", encoding="utf-8"
            ) as file:
                result = json.load(file)

            # Ensure every test has an Error Details value.
            for test in result.get("tests", []):

                if not test.get("error"):
                    if test.get("passed"):
                        test["error"] = "—"

                    else:
                        test["error"] = (
                            f"Test failed. Expected "
                            f"{test.get('expected')!r}, but got "
                            f"{test.get('actual')!r}"
                        )

            if process.stderr:
                result["stderr"] = process.stderr

            return result

    except Exception as error:

        result["error_category"] = "Runtime Error"
        result["stderr"] = str(error)
        result["failed"] = len(tests)

        if not result["tests"]:

            for index, case in enumerate(tests, start=1):
                result["tests"].append(
                    create_test_result(
                        index,
                        case.get("args", []),
                        case.get("expected"),
                        "Not executed",
                        False,
                        f"Runtime Error: {error}"
                    )
                )

        return result
