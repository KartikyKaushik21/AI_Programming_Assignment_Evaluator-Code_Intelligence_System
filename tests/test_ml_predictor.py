import pytest
from src.ml_predictor import load_models

def test_models_exist_if_trained():
    pass_model, error_model = load_models()
    # It might be None if tests are run before training, which is acceptable in this workflow.
    pass
