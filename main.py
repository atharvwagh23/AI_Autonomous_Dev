# main.py

import json
from pathlib import Path

from app.graph import graph


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

# Create an "output_main_cli" directory in the project root.
#
# Example:
#
# ai-dev-team/
# ├── main.py
# └── output_main_cli/
#
OUTPUT_DIR = Path("output_main_cli")

# Create the directory if it does not already exist.
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# CLEAN LLM CODE OUTPUT
# ============================================================

def clean_code_block(code: str) -> str:
    """
    Remove markdown code fences (```python ... ```) if the LLM
    wrapped its response in them, so the saved file is valid Python.
    """
    code = code.strip()

    if code.startswith("```"):
        lines = code.split("\n")
        lines = lines[1:]  # drop opening ``` or ```python line

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # drop closing ``` line

        code = "\n".join(lines)

    return code


# ============================================================
# SAVE GENERATED CODE
# ============================================================

def save_generated_code(code: str):
    """
    Save the generated Python code into a .py file.

    The generated file will be:

        output_main_cli/generated_code.py
    """

    code = clean_code_block(code)  # strip markdown fences before saving

    output_file = OUTPUT_DIR / "generated_code.py"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(code)

    return output_file


# ============================================================
# SAVE COMPLETE EXECUTION RESULT
# ============================================================

def save_execution_result(result: dict):
    """
    Save the complete LangGraph state as JSON.

    This gives us an audit/debug file containing:

        - requirement
        - generated code
        - review feedback
        - QA feedback
        - final report
        - needs_fix
        - iteration count
    """

    output_file = OUTPUT_DIR / "execution_result.json"

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    return output_file


# ============================================================
# MAIN APPLICATION
# ============================================================

def run():

    print("\n===================================")
    print("      AI AUTONOMOUS DEV TEAM")
    print("===================================")

    print(
        "\nEnter a Python development requirement."
    )

    print(
        "Type 'exit' to stop the application."
    )


    # --------------------------------------------------------
    # CONTINUOUS USER INPUT
    # --------------------------------------------------------

    while True:

        requirement = input(
            "\nEnter Requirement: "
        )


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if requirement.lower().strip() == "exit":

            print("\nExiting application...")

            break


        # ----------------------------------------------------
        # INITIAL LANGGRAPH STATE
        # ----------------------------------------------------

        initial_state = {

            # Original user requirement
            "requirement": requirement,

            # These values will be populated by the nodes.
            "generated_code": "",
            "review_feedback": "",
            "qa_feedback": "",
            "final_report": "",

            # Initial QA decision
            "needs_fix": False,

            # No fix iterations have happened yet.
            "iteration_count": 0,
        }


        # ----------------------------------------------------
        # RUN LANGGRAPH
        # ----------------------------------------------------

        print("\nStarting AI development workflow...")

        result = graph.invoke(
            initial_state
        )


        # ====================================================
        # PRINT GENERATED CODE
        # ====================================================

        print("\n")
        print("===================================")
        print("       GENERATED PYTHON CODE")
        print("===================================\n")

        print(
            result["generated_code"]
        )


        # ====================================================
        # SAVE GENERATED CODE
        # ====================================================

        code_file = save_generated_code(
            result["generated_code"]
        )

        print("\n")
        print(
            f"Generated code saved to: {code_file}"
        )


        # ====================================================
        # PRINT REVIEW
        # ====================================================

        print("\n")
        print("===================================")
        print("          REVIEW FEEDBACK")
        print("===================================\n")

        print(
            result["review_feedback"]
        )


        # ====================================================
        # PRINT QA
        # ====================================================

        print("\n")
        print("===================================")
        print("            QA FEEDBACK")
        print("===================================\n")

        print(
            result["qa_feedback"]
        )


        # ====================================================
        # PRINT FINAL REPORT
        # ====================================================

        print("\n")
        print("===================================")
        print("        FINAL ENGINEERING REPORT")
        print("===================================\n")

        print(
            result["final_report"]
        )


        # ====================================================
        # SAVE COMPLETE RESULT
        # ====================================================

        result_file = save_execution_result(
            result
        )

        print("\n")
        print(
            f"Complete execution result saved to: "
            f"{result_file}"
        )


        # ====================================================
        # PRINT EXECUTION SUMMARY
        # ====================================================

        print("\n")
        print("===================================")
        print("        EXECUTION SUMMARY")
        print("===================================")

        print(
            "Needs Fix:",
            result["needs_fix"]
        )

        print(
            "Iterations:",
            result["iteration_count"]
        )

        print(
            "Code File:",
            code_file
        )

        print(
            "Execution File:",
            result_file
        )


# ============================================================
# PYTHON ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run()