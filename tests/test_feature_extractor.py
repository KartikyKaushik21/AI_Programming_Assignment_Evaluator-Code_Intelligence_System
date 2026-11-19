from src.feature_extractor import extract_features


def test_feature_extractor_valid():
    code = """
def add(a, b):
    for i in range(10):
        pass
    return a + b
"""

    features = extract_features(code)

    assert features["num_functions"] == 1
    assert features["num_loops"] == 1
    assert features["num_returns"] == 1
    assert features["cyclomatic_complexity"] >= 2


def test_feature_extractor_invalid():
    code = """
def add(a, b)
    return a + b
"""

    features = extract_features(code)

    assert features["num_functions"] == 0
    assert features["num_returns"] == 0
    assert features["cyclomatic_complexity"] == 1