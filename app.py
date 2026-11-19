
import streamlit as st
import pandas as pd

from src.problem_bank import PROBLEMS
from src.execution_engine import execute_code
from src.feature_extractor import extract_features
from src.ml_predictor import load_models, predict_submission
from src.feedback_engine import generate_feedback
from src.database import init_db, save_submission, get_history


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Code Evaluator",
    page_icon="💻",
    layout="wide"
)


# ==========================================
# 2. GLOBAL TYPOGRAPHY AND UI STYLING
# ==========================================

st.markdown("""
<style>

/* Professional font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global font */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
}

/* Fix sidebar Configuration heading */
.stSidebar h1 {
    font-size: 24px !important;
    white-space: nowrap !important;
    line-height: 1.3 !important;
}

/* Main heading */
.stApp h1 {
    font-family: 'Inter', sans-serif !important;
    font-size: 34px !important;
    font-weight: 800 !important;
}

/* Section headings */
.stApp h2 {
    font-size: 25px !important;
    font-weight: 700 !important;
}

/* Subheadings */
.stApp h3 {
    font-size: 21px !important;
    font-weight: 700 !important;
}

/* Normal text */
.stMarkdown p,
.stMarkdown li {
    font-size: 16px !important;
    font-weight: 400 !important;
    line-height: 1.7 !important;
}

/* Bold text */
.stMarkdown strong,
.stMarkdown b {
    font-weight: 700 !important;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-weight: 700 !important;
}

/* Widget labels */
[data-testid="stWidgetLabel"] p {
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    font-size: 15px !important;
}

/* Code editor */
.stTextArea textarea {
    font-family: 'Consolas', monospace !important;
}

/* Select box */
.stSelectbox div {
    font-size: 15px !important;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    font-size: 15px !important;
    font-weight: 600 !important;
}

/* Captions */
[data-testid="stCaptionContainer"] {
    font-size: 14px !important;
}

/* Feedback and alerts */
[data-testid="stAlert"] p {
    font-size: 16px !important;
    line-height: 1.7 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    font-size: 15px !important;
}

/* Popover */
[data-testid="stPopover"] button {
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. INITIALIZE DATABASE
# ==========================================

init_db()


# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Submit Code", "Submission History"]
)


# ==========================================
# 5. LOAD ML MODEL
# ==========================================

try:
    model, feature_cols = load_models()

except Exception as error:
    model, feature_cols = None, None
    st.sidebar.warning(
        f"ML model could not be loaded: {error}"
    )

if model is None:
    st.sidebar.warning(
        "ML model unavailable. Execution-based evaluation will still work."
    )


# ==========================================
# PAGE 1: SUBMIT CODE
# ==========================================

if page == "Submit Code":

    st.title("👨‍💻 Programming Assignment Evaluator")

    st.caption(
        "Automated code evaluation using execution, "
        "static analysis and machine learning."
    )

    # Student name
    student_name = st.text_input(
        "Student Name:",
        "Student 1"
    )

    # Problem selection
    prob_keys = list(PROBLEMS.keys())

    selected_prob_key = st.selectbox(
        "Select Problem:",
        prob_keys,
        format_func=lambda x: PROBLEMS[x]["title"]
    )

    problem = PROBLEMS[selected_prob_key]

    # Problem description
    st.markdown("### 📝 Problem Description")

    st.markdown(
        problem.get("description", problem["title"])
    )

    # Sample templates
    sample_options = {
        "(Empty)": ""
    }

    for i, sample in enumerate(
        problem.get("correct", []), start=1
    ):
        sample_options[f"Correct Template {i}"] = sample

    for i, sample in enumerate(
        problem.get("wrong", []), start=1
    ):
        sample_options[f"Incorrect Template {i}"] = sample

    sample_choice = st.selectbox(
        "Load Sample Template:",
        list(sample_options.keys())
    )

    default_code = sample_options[sample_choice]

    if sample_choice == "(Empty)":
        default_code = (
            f"def {problem['entry_point']}(*args):\n"
            "    pass"
        )

    # Code editor
    st.markdown("### 💻 Python Code Editor")

    code = st.text_area(
        "Write your solution:",
        value=default_code,
        height=280
    )

    st.markdown("---")

    # ======================================
    # SUBMIT AND EVALUATE
    # ======================================

    if st.button(
        "🚀 Submit & Evaluate",
        type="primary",
        use_container_width=True
    ):

        if not student_name.strip():

            st.warning("Please enter your name.")

        elif not code.strip():

            st.warning("Please enter your Python code.")

        else:

            with st.spinner(
                "Analyzing and executing your code..."
            ):

                # 1. Static Analysis
                features = extract_features(code)

                # 2. Actual Execution
                exec_results = execute_code(
                    code,
                    problem
                )

                # 3. ML Prediction
                error_cat_pred = None
                error_conf = 0.0

                if (
                    model is not None
                    and exec_results.get("error_category")
                    != "Syntax Error"
                ):

                    try:
                        error_cat_pred, error_conf = (
                            predict_submission(
                                features,
                                model,
                                feature_cols
                            )
                        )

                    except Exception as error:
                        st.warning(
                            f"ML prediction unavailable: {error}"
                        )

                # 4. Calculate Functional Score
                passed = exec_results.get("passed", 0)
                failed = exec_results.get("failed", 0)

                total_tests = passed + failed

                score = (
                    (passed / total_tests) * 100
                    if total_tests > 0
                    else 0
                )

                # Actual execution verdict
                observed_error = exec_results.get(
                    "error_category", "Error"
                )

                # 5. Save Submission
                ml_pred_str = (
                    f"{error_cat_pred} "
                    f"({error_conf * 100:.1f}%)"
                    if error_cat_pred is not None
                    else "N/A"
                )

                save_submission(
                    student_name,
                    selected_prob_key,
                    code,
                    score,
                    "Local",
                    observed_error,
                    ml_pred_str
                )

            # ==================================
            # 6. DISPLAY EVALUATION RESULTS
            # ==================================

            st.markdown("---")
            st.header("📊 Evaluation Results")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Functional Score",
                f"{score:.1f}%"
            )

            col2.metric(
                "Tests Passed",
                f"{passed}/{total_tests}"
            )

            col3.metric(
                "Observed Error",
                observed_error
            )

            # ==================================
            # 7. EXECUTION STATUS
            # ==================================

            st.markdown("### Execution Status")

            if (
                observed_error == "None"
                and failed == 0
                and total_tests > 0
            ):

                st.success(
                    "All test cases passed successfully!"
                )

            elif observed_error == "Syntax Error":

                st.error(
                    "Syntax Error: Please check your Python code."
                )

            elif observed_error == "Runtime Error":

                st.error(
                    "Runtime Error: Your program encountered an exception."
                )

            elif observed_error == "Timeout":

                st.error(
                    "Execution Timeout: Your program took too long."
                )

            elif failed > 0:

                st.warning(
                    f"{failed} test case(s) failed. "
                    "Review your implementation."
                )

            else:

                st.warning(
                    "No test cases were completed."
                )

            # ==================================
            # 8. DISPLAY ERROR TRACE
            # ==================================

            if exec_results.get("stderr"):

                with st.expander(
                    "View Execution Error Details"
                ):

                    st.code(
                        exec_results["stderr"],
                        language="text"
                    )

            # ==================================
            # 9. DISPLAY TEST CASES
            # ==================================

            if exec_results.get("tests"):

                st.markdown("### 🧪 Test Cases Summary")

                df_tests = pd.DataFrame(
                    exec_results["tests"]
                )

                df_display = df_tests.copy()

                # Test visibility
                if "visible" in df_display.columns:

                    df_display["Test Type"] = (
                        df_display["visible"].apply(
                            lambda value:
                            "Visible" if value else "Hidden"
                        )
                    )

                elif "test" in df_display.columns:

                    df_display["Test Type"] = "Test"

                # Test status
                if (
                    "status" not in df_display.columns
                    and "passed" in df_display.columns
                ):

                    df_display["status"] = (
                        df_display["passed"].apply(
                            lambda value:
                            "Passed" if value else "Failed"
                        )
                    )

                # Format values for readable table display
                def format_output(value):
                    if isinstance(value, bool):
                        return "True" if value else "False"

                    if value is None:
                        return "None"

                    if isinstance(value, (dict, list, tuple, set)):
                        return repr(value)

                    return str(value)

                # Convert values to text to prevent checkbox rendering
                for column in ["input", "expected", "actual", "error"]:
                    if column in df_display.columns:
                        df_display[column] = (
                            df_display[column].apply(format_output)
                        )

                # Select and order columns
                display_columns = [
                    column
                    for column in [
                        "Test Type",
                        "status",
                        "input",
                        "expected",
                        "actual",
                        "error"
                    ]
                    if column in df_display.columns
                ]

                # Display final evaluation table
                st.dataframe(
                    df_display[display_columns],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Test Type": "Test Type",
                        "status": "Status",
                        "input": "Test Input",
                        "expected": "Expected Output",
                        "actual": "Actual Output",
                        "error": "Error Details"
                    }
                )

            # ==================================
            # 10. ACTIONABLE FEEDBACK
            # ==================================

            st.markdown("---")

            st.header(
                "🤖 Actionable Feedback & Intelligence"
            )

            feedback = generate_feedback(
                exec_results,
                features,
                error_cat_pred,
                error_conf,
                problem
            )

            st.markdown(feedback)


# ==========================================
# PAGE 2: SUBMISSION HISTORY
# ==========================================

elif page == "Submission History":

    st.title("📚 Submission History")

    st.caption(
        "View previously evaluated programming submissions."
    )

    df = get_history()

    if df is not None and not df.empty:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No submissions yet.")


# ==========================================
# FLOATING AI CHATBOT
# ==========================================

st.markdown("""
<style>
/* Keep the Streamlit popover wrapper out of the page layout */
[data-testid="stPopover"] {
    position: static !important;
    width: 0 !important;
    height: 0 !important;
    min-width: 0 !important;
    min-height: 0 !important;
    overflow: visible !important;
}

/* Pin only the actual chatbot launcher to the bottom-right */
[data-testid="stPopover"] button {
    position: fixed !important;
    right: 28px !important;
    bottom: 26px !important;
    z-index: 999999 !important;
    width: auto !important;
    min-width: 158px !important;
    min-height: 54px !important;
    padding: 13px 22px !important;
    background: linear-gradient(135deg, #635BFF, #4338CA) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,.16) !important;
    border-radius: 999px !important;
    box-shadow: 0 8px 28px rgba(79, 70, 229, 0.42) !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    transition: transform .2s ease, box-shadow .2s ease !important;
}

[data-testid="stPopover"] button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 34px rgba(79, 70, 229, 0.55) !important;
}

/* Force the chatbot window to open above the launcher at bottom-right.
   Streamlit normally positions popovers beside their anchor; override that. */
[data-testid="stPopoverBody"],
div[data-testid="stPopoverBody"] {
    position: fixed !important;
    inset: auto 56px 112px auto !important;
    top: auto !important;
    right: 56px !important;
    bottom: 112px !important;
    left: auto !important;
    transform: none !important;
    translate: none !important;
    margin: 0 !important;
    width: min(400px, calc(100vw - 32px)) !important;
    min-width: min(400px, calc(100vw - 32px)) !important;
    max-width: min(400px, calc(100vw - 32px)) !important;
    max-height: min(620px, calc(100vh - 125px)) !important;
    overflow-y: auto !important;
    border: 1px solid rgba(148, 163, 184, .22) !important;
    border-radius: 18px !important;
    box-shadow: 0 18px 60px rgba(0, 0, 0, .48) !important;
    background: #171923 !important;
    z-index: 999998 !important;
}

/* Keep page content clear of the floating launcher */
.main .block-container { padding-bottom: 90px !important; }

/* Chat messages */
[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    padding: 10px 12px !important;
    margin-bottom: 9px !important;
}

/* Chat input and send button */
[data-testid="stPopoverBody"] [data-testid="stTextInput"] input {
    border-radius: 12px !important;
}

[data-testid="stPopoverBody"] [data-testid="stFormSubmitButton"] button {
    background: #635BFF !important;
    color: white !important;
    border: 0 !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
}

/* Animated three-dot thinking indicator */
.ai-thinking {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 13px;
    background: #292D3B;
    border-radius: 13px;
    color: #D1D5DB;
    font-size: 13px;
}
.ai-thinking span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #A5A1FF;
    animation: aiPulse 1.15s infinite ease-in-out;
}
.ai-thinking span:nth-child(2) { animation-delay: .15s; }
.ai-thinking span:nth-child(3) { animation-delay: .30s; }
@keyframes aiPulse {
    0%, 60%, 100% { opacity: .35; transform: translateY(0); }
    30% { opacity: 1; transform: translateY(-4px); }
}

@media (max-width: 640px) {
    [data-testid="stPopover"] {
        right: 14px !important;
        bottom: 14px !important;
    }
    [data-testid="stPopover"] > button {
        padding: 11px 16px !important;
        min-height: 48px !important;
    }
}
</style>
""", unsafe_allow_html=True)


# Keep chat history across Streamlit reruns
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Read Groq API key from Streamlit secrets
try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    GROQ_API_KEY = ""


with st.popover("💬  AI Tutor", help="Open your AI programming assistant"):

    # Chat header
    st.markdown(
        """
        <div style="
            display:flex; align-items:center; gap:12px;
            padding:4px 0 12px 0; border-bottom:1px solid #383B49;
            margin-bottom:12px;">
            <div style="
                width:42px;height:42px;border-radius:14px;
                display:flex;align-items:center;justify-content:center;
                background:linear-gradient(135deg,#635BFF,#4338CA);
                font-size:22px;">🤖</div>
            <div>
                <div style="font-size:17px;font-weight:750;color:#F8FAFC;">
                    AI Programming Assistant
                </div>
                <div style="font-size:12px;color:#22C55E;">
                    ● Online · Powered by Groq
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Ask about Python, debugging, data structures, algorithms, or your assignment.")

    header_col1, header_col2 = st.columns([3, 1])
    with header_col2:
        if st.button("Clear chat", key="clear_ai_chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    if not GROQ_API_KEY:
        st.warning(
            "AI Tutor is not configured. Add GROQ_API_KEY to "
            ".streamlit/secrets.toml and restart the app."
        )
    else:
        # Welcome message for a new conversation
        if not st.session_state.chat_history:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(
                    "Hi! I'm your AI programming tutor. 👋\n\n"
                    "Share a Python question or paste an error, and I'll help "
                    "you understand it step by step."
                )

        # Existing conversation
        for chat_message in st.session_state.chat_history:
            avatar = "🧑‍💻" if chat_message["role"] == "user" else "🤖"
            with st.chat_message(chat_message["role"], avatar=avatar):
                st.markdown(chat_message["content"])

        # Input form
        with st.form("floating_ai_chat_form", clear_on_submit=True):
            prompt = st.text_input(
                "Message",
                placeholder="Ask anything about programming...",
                label_visibility="collapsed"
            )
            send_col, hint_col = st.columns([1, 2])
            with send_col:
                submitted = st.form_submit_button(
                    "➤ Send",
                    use_container_width=True
                )
            with hint_col:
                st.caption("Press Send to ask the AI tutor.")

        if submitted and prompt.strip():
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt.strip()
            })

            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(prompt.strip())

            with st.chat_message("assistant", avatar="🤖"):
                status_placeholder = st.empty()
                answer_placeholder = st.empty()

                status_placeholder.markdown(
                    """
                    <div class="ai-thinking">
                        <span></span><span></span><span></span>
                        <b style="font-weight:600;margin-left:5px;">
                            Thinking and preparing your answer...
                        </b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                try:
                    from openai import OpenAI

                    client = OpenAI(
                        api_key=GROQ_API_KEY,
                        base_url="https://api.groq.com/openai/v1"
                    )

                    
                    system_prompt = {
                        "role": "system",
                        "content": (
                            "You are an expert AI Python programming tutor "
                            "designed to help beginner and intermediate students. "

                            "YOUR TEACHING STYLE: "
                            "Explain concepts in simple, clear, beginner-friendly language. "
                            "Teach step by step. Explain why something works, not just what "
                            "to write. Avoid unnecessary complicated terminology. "

                            "CODE ACCURACY RULES: "
                            "Accuracy is your highest priority. Never provide code examples, "
                            "syntax, formulas, or alternative solutions unless you have "
                            "carefully checked their logical correctness. "
                            "Mentally trace code examples with a simple input before "
                            "presenting them. Check slicing boundaries, indexing, loop "
                            "conditions, return values, and edge cases. "
                            "Never invent alternative syntax or claim that code works "
                            "without sufficient confidence. If unsure, explicitly say so. "
                            "Prefer simple, standard Python solutions over confusing "
                            "alternatives. "

                            "DEBUGGING: "
                            "When a student shares incorrect code, identify the likely "
                            "mistake, explain why it happens, and guide them towards fixing "
                            "it. Show corrected code when appropriate. "
                            "When explaining an error, distinguish between syntax errors, "
                            "runtime errors, and logical errors. "

                            "HINT-BASED LEARNING: "
                            "When the student asks for a hint, do not immediately reveal "
                            "the complete solution. Give progressive hints. "
                            "Explain the approach before showing the final code. "
                            "When asked for a complete solution, provide clean and "
                            "correct code with a simple explanation. "

                            "EDGE CASES: "
                            "Consider empty inputs, single elements, duplicate values, "
                            "negative numbers, and boundary conditions whenever relevant. "

                            "COMMUNICATION: "
                            "Use readable Python code blocks. Keep answers organized "
                            "and avoid unnecessary lengthy explanations. "
                            "Do not claim to execute code or search the web. "
                            "Politely redirect unrelated questions. "
                            "Never reveal private backend source code, API keys, "
                            "credentials, or secrets."
                        )
                    }


                    messages = (
                        [system_prompt]
                        + st.session_state.chat_history
                    )

                    stream = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=messages,
                        stream=True
                    )

                    ai_response = ""
                    status_placeholder.markdown(
                        """
                        <div class="ai-thinking">
                            <span></span><span></span><span></span>
                            <b style="font-weight:600;margin-left:5px;">
                                Generating response...
                            </b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    for chunk in stream:
                        if not chunk.choices:
                            continue
                        token = chunk.choices[0].delta.content
                        if token:
                            ai_response += token
                            answer_placeholder.markdown(
                                ai_response + "▌"
                            )

                    status_placeholder.empty()
                    answer_placeholder.markdown(ai_response or "I couldn't generate a response. Please try again.")

                except Exception as error:
                    status_placeholder.empty()
                    ai_response = (
                        "⚠️ I couldn't reach the AI service. "
                        "Please check your internet connection, Groq API key, "
                        "and model availability, then try again."
                    )
                    answer_placeholder.warning(ai_response)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_response
                })

            # Rerun so the completed exchange appears in chat history
            st.rerun()




