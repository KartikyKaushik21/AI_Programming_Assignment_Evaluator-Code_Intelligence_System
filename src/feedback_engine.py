
def generate_feedback(
    execution_results,
    ast_features,
    error_cat_pred,
    error_conf,
    problem
):
    feedback = []

    passed = execution_results.get("passed", 0)
    failed = execution_results.get("failed", 0)
    total = passed + failed

    observed_error = execution_results.get(
        "error_category", "None"
    )

    # ======================================
    # 1. FINAL EXECUTION VERDICT
    # ======================================

    feedback.append("### 1. Execution Verdict")

    if observed_error == "Syntax Error":

        feedback.append(
            "🔴 **Syntax Error:** Python could not parse your code. "
            "Check indentation, brackets, colons, and spelling."
        )

    elif observed_error == "Timeout":

        feedback.append(
            "🔴 **Time Limit Exceeded:** Your program took too long. "
            "Check for infinite loops or inefficient algorithms."
        )

    elif observed_error == "Runtime Error":

        feedback.append(
            "🔴 **Runtime Error:** Your program encountered an exception "
            "during execution. Review the error trace below the results."
        )

    elif failed > 0:

        feedback.append(
            f"🟡 **Incorrect Output:** {failed} test case(s) failed. "
            "Your program executed, but some outputs did not match "
            "the expected results."
        )

    elif total > 0:

        feedback.append(
            "🟢 **All Test Cases Passed!** "
            "Your implementation produced the expected output "
            f"for all {passed} test cases."
        )

    else:

        feedback.append(
            "⚠️ No test cases were completed. "
            "Check the execution configuration."
        )

    if total > 0:
        feedback.append(
            f"**Test Summary:** {passed}/{total} passed, "
            f"{failed}/{total} failed. "
            f"Functional score: {(passed / total) * 100:.1f}%."
        )

    # ======================================
    # 2. ML MODEL ANALYSIS
    # ======================================

    feedback.append("\n### 2. ML Model Analysis")

    if error_cat_pred is None:

        feedback.append(
            "ML prediction is currently unavailable. "
            "The execution result remains the final evaluation."
        )

    else:

        confidence_percent = error_conf * 100

        if observed_error == "None" and failed == 0:

            if error_cat_pred == "No Error":

                feedback.append(
                    f"🤖 The ML model agrees with the execution result. "
                    f"Its predicted category is No Error "
                    f"({confidence_percent:.1f}% class probability)."
                )

            else:

                feedback.append(
                    f"⚠️ **Model disagreement:** The ML model predicts "
                    f"{error_cat_pred} ({confidence_percent:.1f}% "
                    f"class probability), but actual execution passed "
                    "all test cases. Therefore, the execution result "
                    "takes priority."
                )

        elif error_cat_pred == observed_error:

            feedback.append(
                f"🤖 The ML prediction matches the observed error category: "
                f"{error_cat_pred} ({confidence_percent:.1f}% "
                "class probability)."
            )

        else:

            feedback.append(
                f"⚠️ The ML model predicts {error_cat_pred} "
                f"({confidence_percent:.1f}% class probability), "
                f"while execution observed {observed_error}. "
                "The actual execution result takes priority."
            )

        feedback.append(
            "Note: This is an experimental model trained on synthetic "
            "code samples. Its confidence is not the same as its "
            "real-world prediction accuracy."
        )

    # ======================================
    # 3. CODE QUALITY ANALYSIS
    # ======================================

    feedback.append("\n### 3. Code Quality Analysis")

    complexity = ast_features.get(
        "cyclomatic_complexity", 1
    )

    loc = ast_features.get("loc", 0)
    functions = ast_features.get("num_functions", 0)
    loops = ast_features.get("num_loops", 0)
    conditions = ast_features.get("num_ifs", 0)

    feedback.append(f"- Lines of code: {loc}")
    feedback.append(f"- Functions: {functions}")
    feedback.append(f"- Loops: {loops}")
    feedback.append(f"- Conditional statements: {conditions}")
    feedback.append(f"- Cyclomatic complexity: {complexity}")

    if complexity <= 5:
        feedback.append(
            "🟢 Your code has relatively low control-flow complexity."
        )

    elif complexity <= 10:
        feedback.append(
            "🟡 Your code has moderate complexity. "
            "Consider simplifying nested conditions where possible."
        )

    else:
        feedback.append(
            "🔴 Your code has high control-flow complexity. "
            "Consider splitting the logic into smaller functions."
        )

    # ======================================
    # 4. IMPROVEMENT SUGGESTIONS
    # ======================================

    feedback.append("\n### 4. Improvement Suggestions")

    if observed_error == "None" and failed == 0 and total > 0:

        feedback.append(
            "- Test additional edge cases beyond the supplied tests."
        )
        feedback.append(
            "- Review time and space complexity for larger inputs."
        )
        feedback.append(
            "- Keep the implementation readable and maintainable."
        )

    elif observed_error == "Wrong Answer" or failed > 0:

        feedback.append(
            "- Compare your actual output with the expected output."
        )
        feedback.append(
            "- Check boundary conditions and empty inputs."
        )

        if problem.get("hint"):
            feedback.append(
                f"- **Problem hint:** {problem['hint']}"
            )

    elif observed_error == "Runtime Error":

        feedback.append(
            "- Inspect the exception message and identify the failing line."
        )
        feedback.append(
            "- Check input types, indexing, and variable initialization."
        )

    elif observed_error == "Syntax Error":

        feedback.append(
            "- Check indentation and Python syntax."
        )
        feedback.append(
            "- Verify that all brackets and parentheses are closed."
        )

    elif observed_error == "Timeout":

        feedback.append(
            "- Check loop termination conditions."
        )
        feedback.append(
            "- Consider a more efficient algorithm."
        )

    return "\n\n".join(feedback)
