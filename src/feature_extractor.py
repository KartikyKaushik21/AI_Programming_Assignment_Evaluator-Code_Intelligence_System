
import ast

FEATURES = [
    "loc",
    "num_functions",
    "num_loops",
    "num_ifs",
    "num_imports",
    "num_returns",
    "num_calls",
    "num_raise",
    "num_try",
    "num_assignments",
    "num_comparisons",
    "num_boolean_ops",
    "num_subscripts",
    "num_constants",
    "num_classes",
    "cyclomatic_complexity",
    "is_recursive"
]


def extract_features(code):

    values = {k: 0 for k in FEATURES}

    values["loc"] = len(code.splitlines())
    values["cyclomatic_complexity"] = 1

    try:
        tree = ast.parse(code)

    except (SyntaxError, ValueError, TypeError):
        return values

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            values["num_functions"] += 1

        elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            values["num_loops"] += 1
            values["cyclomatic_complexity"] += 1

        elif isinstance(node, ast.If):
            values["num_ifs"] += 1
            values["cyclomatic_complexity"] += 1

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            values["num_imports"] += 1

        elif isinstance(node, ast.Return):
            values["num_returns"] += 1

        elif isinstance(node, ast.Call):
            values["num_calls"] += 1

        elif isinstance(node, ast.Raise):
            values["num_raise"] += 1

        elif isinstance(node, ast.Try):
            values["num_try"] += 1

        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            values["num_assignments"] += 1

        elif isinstance(node, ast.Compare):
            values["num_comparisons"] += 1
            values["cyclomatic_complexity"] += max(0, len(node.ops) - 1)

        elif isinstance(node, ast.BoolOp):
            values["num_boolean_ops"] += 1
            values["cyclomatic_complexity"] += max(0, len(node.values) - 1)

        elif isinstance(node, ast.Subscript):
            values["num_subscripts"] += 1

        elif isinstance(node, ast.Constant):
            values["num_constants"] += 1

        elif isinstance(node, ast.ClassDef):
            values["num_classes"] += 1

    # Correct direct-recursion detection
    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

            for child in ast.walk(node):

                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        if child.func.id == node.name:
                            values["is_recursive"] = 1
                            break

            if values["is_recursive"] == 1:
                break

    return values
