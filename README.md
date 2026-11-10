# AI-Powered Programming Assignment Evaluation & Code Intelligence System

An intelligent, Streamlit-based educational platform that evaluates Python programming submissions using **static code analysis, supervised machine learning, and dynamic code execution**.

The system analyses submitted code, predicts common programming error categories, executes programs against predefined test cases, and provides detailed feedback to help students improve their programming skills.

---

## 1. Project Overview

The **AI-Powered Programming Assignment Evaluation & Code Intelligence System** combines three major techniques:

- **Static Code Analysis:** Uses Python's Abstract Syntax Tree (AST) to extract structural code features such as lines of code, functions, loops, conditions, and cyclomatic complexity.
- **Machine Learning:** Uses a supervised Random Forest Classifier to predict programming error categories based on extracted code features.
- **Dynamic Code Execution:** Executes submitted Python programs against predefined test cases to verify their functional correctness.

The platform also includes an AI-powered programming tutor that provides explanations, debugging guidance, and programming hints.

## 2. Main Features

- Student code submission through a Streamlit interface.
- Programming problem selection.
- Automated test-case execution.
- Syntax error detection using AST parsing.
- Runtime error and wrong-answer detection.
- Static code feature extraction.
- Random Forest-based error-category classification.
- Derived Pass/Fail prediction.
- Code structure and complexity analysis.
- Test-case-based feedback and error details.
- Student submission history.
- AI-powered programming tutor.
- Model evaluation reports and confusion matrices.

## 3. Machine Learning Model

### Algorithm: Random Forest Classifier

The project uses a Random Forest Classifier implemented with Scikit-learn.

The model predicts one of three error categories:

1. **No Error**
2. **Wrong Answer**
3. **Runtime Error**

Syntax errors are handled separately using Python AST parsing.

The Pass/Fail classification is derived from the predicted error category:

- No Error → Pass
- Wrong Answer → Fail
- Runtime Error → Fail

**Important:** The Random Forest model predicts an error category using static code features. Separately, the dynamic execution engine runs the submitted program against predefined test cases. The actual execution results determine whether the submission passes or fails. Therefore, the ML prediction and actual execution result may sometimes differ.

### Model Configuration

| Parameter | Value |
|---|---:|
| Algorithm | Random Forest Classifier |
| Number of estimators | 300 |
| Minimum samples per leaf | 2 |
| Class weight | Balanced |
| Random state | 42 |
| CPU parallel processing | All available cores |

### Extracted Features

The system extracts structural features from Python source code, including:

- Lines of code
- Number of functions
- Number of variables and assignments
- Number of loops
- Number of conditional statements
- Number of imports
- Number of return statements
- Number of function calls
- Number of exception-handling statements
- Number of classes
- Number of comparisons
- Number of Boolean operations
- Number of subscripts
- Number of constants
- Cyclomatic complexity
- Recursion-related features

### Model Evaluation Results

The model was evaluated using a random holdout test set.

**Error Category Classification**

| Metric | Result |
|---|---:|
| Accuracy | 88.26% |
| Macro Precision | 86% |
| Macro Recall | 90% |
| Macro F1-score | 87% |

**Derived Pass/Fail Classification**

| Metric | Result |
|---|---:|
| Accuracy | 93.34% |
| Precision | 98.05% |
| Recall | 87.58% |
| F1-score | 92.52% |

### Additional Generalisation Evaluation

An additional Leave-One-Problem-Out (LOPO) evaluation was performed to examine the model's ability to generalise to programming problems excluded from training.

| Metric | Result |
|---|---:|
| Error Category Accuracy | 77.06% |
| Error Category Macro F1-score | 76.92% |
| Derived Pass/Fail Accuracy | 83.82% |

The lower LOPO results indicate that generalising to unseen programming problems is more challenging than evaluation using a random holdout split.

**Dataset Limitation:** The dataset is synthetically generated. These results represent performance on the project's synthetic evaluation data and should not be interpreted as guaranteed performance on real-world student submissions.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| Scikit-learn | Machine learning |
| Random Forest | Error-category classification |
| Python AST | Static code analysis |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Joblib | Model persistence |
| Matplotlib | Performance visualisation |
| SQLite | Submission history storage |
| Groq API | AI-powered programming tutor |
| Pytest | Automated testing |

## 5. Project Structure

```text
AI_code_evaluator_project/
│
├── src/
│   ├── problem_bank.py
│   ├── feature_extractor.py
│   ├── execution_engine.py
│   ├── ml_predictor.py
│   ├── feedback_engine.py
│   └── database.py
│
├── data/
│   └── Generated dataset files
│
├── models/
│   ├── error_classifier.joblib
│   └── feature_columns.json
│
├── reports/
│   ├── test_predictions.csv
│   └── Evaluation reports and graphs
│
├── tests/
│   ├── test_execution_engine.py
│   ├── test_feature_extractor.py
│   ├── test_feedback_engine.py
│   └── test_ml_predictor.py
│
├── generate_dataset.py
├── train_models.py
├── evaluate_models.py
├── leave_one_problem_out.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

Some dataset and evaluation files are generated when the corresponding scripts are executed.

## 6. Setup and Installation

### Prerequisites

- Python 3.10
- Visual Studio Code (recommended)
- Git
- Internet connection for installing dependencies and using the AI Tutor

### Step 1: Clone the Repository

```powershell
git clone https://github.com/KartikyKaushik21/AI-Programming-Assignment-Evaluation.git
```

Navigate into the project directory:

```powershell
cd AI-Programming-Assignment-Evaluation
```

### Step 2: Create a Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment

```powershell
.\venv\Scripts\activate
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Generate the Synthetic Dataset

```powershell
python generate_dataset.py
```

This generates the synthetic programming submission dataset used for model development.

### Step 6: Train the Machine Learning Model

```powershell
python train_models.py
```

This trains the Random Forest Classifier and saves the trained model and feature-column configuration in the `models/` directory.

### Step 7: Evaluate the Model

```powershell
python evaluate_models.py
```

This evaluates the trained model and generates evaluation results.

### Step 8: Run Additional Generalisation Evaluation (Optional)

```powershell
python leave_one_problem_out.py
```

This evaluates model performance on programming problems excluded from training.

### Step 9: Run Automated Tests

```powershell
python -m pytest
```

The current project test suite has passed **6 automated tests**.

### Step 10: Start the Streamlit Application

```powershell
streamlit run app.py
```

The application will open in your default web browser.

## 7. AI Tutor Configuration

The AI-powered programming tutor uses the Groq API.

To configure it, create the following directory and file in the project root:

```text
.streamlit/
└── secrets.toml
```

Add your Groq API key:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

Replace the placeholder with your own API key.

**Security Note:**
- Never upload `.streamlit/secrets.toml` to GitHub.
- Never expose API keys or credentials in source code.
- Keep API credentials private and use your own API key when running the application.

## 8. Execution and Security Limitations

The current prototype executes submitted Python code through a local subprocess with timeout handling.

**Important Security Limitation:** Local subprocess execution is not equivalent to a secure sandbox. It does not provide complete isolation from the host operating system.

Therefore:

- Use the application only for trusted educational testing.
- Do not expose it publicly for arbitrary code execution.
- Do not execute untrusted submissions on a personal or production machine.
- A properly isolated execution environment is required before public deployment.

Docker-based isolation is not implemented in the current version.

## 9. Testing

The project includes automated tests covering:

- Code execution.
- Static feature extraction.
- Feedback generation.
- Machine learning prediction.

**Current automated test result: 6 tests passed.**

Manual application testing also covers:

- Correct code submissions.
- Wrong-answer submissions.
- Runtime errors.
- Syntax errors.

The application displays the corresponding execution status, test-case results and error details.

## 10. Future Enhancements

Possible future improvements include:

- Secure sandboxed code execution.
- Support for additional programming languages.
- Training with larger real-world programming datasets.
- Improved model generalisation to unseen programming problems.
- More advanced code quality analysis.
- Detailed student performance analytics.
- Enhanced personalised learning recommendations.
- Improved AI-assisted debugging and tutoring.

## 11. Conclusion

The AI-Powered Programming Assignment Evaluation & Code Intelligence System demonstrates how static code analysis, supervised machine learning, dynamic code execution and AI-based tutoring can be combined to support programming education.

The system uses AST-based feature extraction to analyse Python code structure and a Random Forest Classifier to predict common programming error categories. Its execution engine independently verifies submitted programs using predefined test cases and provides detailed evaluation feedback.

The project achieved 88.26% error-category classification accuracy and 93.34% derived Pass/Fail classification accuracy on the synthetic random holdout evaluation. Additional Leave-One-Problem-Out evaluation highlights the challenges of generalising to unseen programming problems.

Overall, this project provides a foundation for an intelligent programming assignment evaluation platform that aims to make automated assessment more informative and support students in improving their programming skills.