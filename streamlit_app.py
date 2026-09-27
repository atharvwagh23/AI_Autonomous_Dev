import streamlit as st
from pathlib import Path
import json
import inspect

from app.graph import graph

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI Autonomous Dev Team",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# OUTPUT DIRECTORY (separate from CLI outputs)
# ============================================================
OUTPUT_DIR = Path("output_streamlit")
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# CLEAN LLM CODE OUTPUT
# ============================================================
def clean_code_block(code: str) -> str:
    """Remove markdown code fences if the LLM wrapped its response in them."""
    code = code.strip()

    if code.startswith("```"):
        lines = code.split("\n")
        lines = lines[1:]  # drop opening ``` or ```python line

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # drop closing ``` line

        code = "\n".join(lines)

    return code


def save_generated_code(code: str):
    """Save the generated Python code into a .py file."""
    code = clean_code_block(code)  # strip markdown fences before saving

    output_file = OUTPUT_DIR / "generated_code.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(code)
    return output_file


def save_execution_result(result: dict):
    """Save the full LangGraph state as a JSON audit/debug file."""
    output_file = OUTPUT_DIR / "execution_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    return output_file


def load_functions_from_file(file_path: Path):
    """
    Dynamically import the generated code file and return a dict of
    {function_name: function_object} for every top-level function found.
    This lets us test whatever function name the LLM happened to generate.
    """
    namespace = {}
    code_text = file_path.read_text(encoding="utf-8")

    # Execute the generated code in an isolated namespace
    exec(code_text, namespace)

    # Collect only functions defined in this namespace (skip imports/classes)
    functions = {
        name: obj
        for name, obj in namespace.items()
        if inspect.isfunction(obj) and not name.startswith("_")
    }
    return functions


# ============================================================
# CUSTOM STYLING
# ============================================================
st.markdown(
    """
    <style>
        .main .block-container {
            padding-top: 2rem;
            max-width: 1100px;
        }
        .hero-title {
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        .hero-subtitle {
            color: #9aa0a6;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 16px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HERO / HEADER SECTION
# ============================================================
st.markdown('<div class="hero-title">🤖 AI Autonomous Dev Team</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Describe a requirement and let the AI team '
    '<b>write</b>, <b>review</b>, <b>QA-check</b>, <b>fix</b>, and <b>report</b> '
    'on the code — end to end.</div>',
    unsafe_allow_html=True
)
st.divider()

# ============================================================
# INPUT SECTION
# ============================================================
requirement = st.text_area(
    "📝 Enter your requirement",
    placeholder="e.g., Write a function to check if a number is prime",
    height=110
)

run_button = st.button("🚀 Run AI Dev Team", type="primary", use_container_width=True)

# ============================================================
# RUN THE LANGGRAPH WORKFLOW
# ============================================================
if run_button:
    if not requirement.strip():
        st.warning("⚠️ Please enter a requirement first.")
    else:
        initial_state = {
            "requirement": requirement,
            "generated_code": "",
            "review_feedback": "",
            "qa_feedback": "",
            "final_report": "",
            "needs_fix": False,
            "iteration_count": 0,
        }

        # Run the graph with a spinner while agents work
        with st.spinner("🧠 Running AI development workflow... this may take a minute."):
            try:
                result = graph.invoke(initial_state)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        # Save outputs to disk
        code_file = save_generated_code(result["generated_code"])
        result_file = save_execution_result(result)

        # Store everything in session_state so it survives reruns
        # (e.g. when the "Run Function" test button is clicked later)
        st.session_state["result"] = result
        st.session_state["code_file"] = code_file
        st.session_state["result_file"] = result_file

# ============================================================
# DISPLAY RESULTS (persists across reruns via session_state)
# ============================================================
if "result" in st.session_state:
    result = st.session_state["result"]
    code_file = st.session_state["code_file"]
    result_file = st.session_state["result_file"]

    st.success("✅ Workflow completed successfully!")
    st.divider()

    # --------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔁 Needs Fix", "Yes" if result["needs_fix"] else "No")
    with col2:
        st.metric("🔄 Iterations", result["iteration_count"])
    with col3:
        st.metric("📁 Output Folder", str(OUTPUT_DIR))

    st.divider()

    # --------------------------------------------------
    # RESULTS IN TABS
    # --------------------------------------------------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["💻 Generated Code", "🔍 Review Feedback", "✅ QA Feedback", "📄 Final Report"]
    )

    with tab1:
        st.code(result["generated_code"], language="python")
        st.caption(f"💾 Saved to: `{code_file}`")

    with tab2:
        st.markdown(result["review_feedback"])

    with tab3:
        st.markdown(result["qa_feedback"])

    with tab4:
        st.markdown(result["final_report"])

    st.divider()
    st.caption(f"📦 Full execution result saved to: `{result_file}`")

    # ============================================================
    # TEST THE GENERATED FUNCTION INTERACTIVELY
    # ============================================================
    st.divider()
    st.subheader("🧪 Test the Generated Function")

    try:
        functions = load_functions_from_file(code_file)
    except Exception as e:
        functions = {}
        st.warning(f"Could not load functions for testing: {e}")

    if not functions:
        st.info("No testable functions were found in the generated code.")
    else:
        # Let the user pick which function to test (usually just one)
        func_name = st.selectbox(
            "Select a function to test:",
            list(functions.keys()),
            key="test_func_selectbox"
        )
        selected_func = functions[func_name]

        test_input = st.text_input(
            f"Input for `{func_name}`:",
            placeholder="e.g., A man, a plan, a canal: Panama",
            key="test_func_input"
        )

        if st.button("▶️ Run Function", use_container_width=True, key="test_func_run_button"):
            try:
                output = selected_func(test_input)
                st.success(f"**Output:** `{output}`")
            except Exception as e:
                st.error(f"Error running `{func_name}`: {e}")