from src.feedback_engine import generate_feedback


def test_generate_feedback():
    execution_results = {
        "error_category": "Syntax Error",
        "passed": 0,
        "failed": 1
    }

    ast_features = {
        "cyclomatic_complexity": 12,
        "loc": 10,
        "num_functions": 1,
        "num_loops": 3,
        "num_ifs": 2
    }

    feedback = generate_feedback(
        execution_results,
        ast_features,
        None,
        0.0,
        {}
    )

    assert "Syntax Error" in feedback
    assert "high control-flow complexity" in feedback