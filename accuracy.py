import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib

# 1. Load your trained models
try:
    pass_model = joblib.load('models/pass_fail_model.joblib')
    error_model = joblib.load('models/error_classifier.joblib')
except FileNotFoundError:
    print("Error: Could not find model files. Please check your model paths.")
    exit()

# 2. Load both features and labels
try:
    X_test = pd.read_csv('data/synthetic_features.csv') 
    results_df = pd.read_csv('data/synthetic_execution_results.csv')
except FileNotFoundError:
    print("Error: Could not find CSV files in the data/ folder.")
    exit()

# Drop IDs and any target labels accidentally saved in the features file
unwanted_columns = ['submission_id', 'is_correct', 'error_category', 'will_pass']
for col in unwanted_columns:
    if col in X_test.columns:
        X_test = X_test.drop(columns=[col])

# Safely identify the exact column names used in your generated results file
pass_col = 'will_pass' if 'will_pass' in results_df.columns else 'passed'
error_col = 'error_category' if 'error_category' in results_df.columns else 'error_type'

# Assign the true labels and force consistent data types
y_pass_true = results_df[pass_col]
y_error_true = results_df[error_col].astype(str)

# 3. Generate Predictions
y_pass_pred = pass_model.predict(X_test)
y_error_pred = error_model.predict(X_test)

# 4. Calculate and Print Metrics for the Pass/Fail Model
print("========================================")
print("📈 PASS/FAIL MODEL EVALUATION")
print("========================================")
print(f"Accuracy:  {accuracy_score(y_pass_true, y_pass_pred):.4f}")
print(f"Precision: {precision_score(y_pass_true, y_pass_pred, average='weighted'):.4f}")
print(f"Recall:    {recall_score(y_pass_true, y_pass_pred, average='weighted'):.4f}")
print(f"F1-Score:  {f1_score(y_pass_true, y_pass_pred, average='weighted'):.4f}")
print("\nDetailed Classification Report:")
print(classification_report(y_pass_true, y_pass_pred))

# 5. Calculate and Print Metrics for the Error Categorization Model
print("\n========================================")
print("📊 ERROR CATEGORY MODEL EVALUATION")
print("========================================")
print(f"Accuracy:  {accuracy_score(y_error_true, y_error_pred):.4f}")
# Using 'weighted' average for multi-class classification
print(f"Precision: {precision_score(y_error_true, y_error_pred, average='weighted', zero_division=0):.4f}")
print(f"Recall:    {recall_score(y_error_true, y_error_pred, average='weighted', zero_division=0):.4f}")
print(f"F1-Score:  {f1_score(y_error_true, y_error_pred, average='weighted', zero_division=0):.4f}")
print("\nDetailed Classification Report:")
print(classification_report(y_error_true, y_error_pred, zero_division=0))