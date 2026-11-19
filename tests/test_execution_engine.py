from src.execution_engine import execute_code
from src.problem_bank import PROBLEMS


def test_execute_code_correct_local():
    problem = PROBLEMS["q1"]
    code = problem["correct"][0]

    result = execute_code(code, problem)

    assert result["failed"] == 0
    assert result["passed"] == len(problem["tests"])
    assert result["error_category"] == "None"


def test_execute_code_syntax_error_local():
    problem = PROBLEMS["q1"]

    code = """
def find_max(arr)
    return max(arr)
"""

    result = execute_code(code, problem)

    assert result["error_category"] == "Syntax Error"