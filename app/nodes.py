import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.prompts import (DEVELOPER_PROMPT, REVIEW_PROMPT, QA_PROMPT, REPORT_PROMPT, FIX_PROMPT)
from app.state import AgentState

## Step 1: load env variables
load_dotenv()

## Step 2: Create the llm

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ API KEY is missing. Please add it to your .env file")

## Step 3: Create chatGroq model
llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature=0.2,
    api_key=groq_api_key
)


## Helper function
def invoke_llm(prompt: str) -> str:
    """
    Send a prompt to the llm and return plain text. this is done because our state stores only strings
    """
    response = llm.invoke(prompt)
    return response.content

## DEVELOPER Node
def developer_node(state: AgentState) -> dict:
    print("\n =====================================")
    print("INSIDE DEVELOPER NODE")
    print("\n =====================================")

    prompt = DEVELOPER_PROMPT.format(
        requirement = state["requirement"]
    )

    generated_code = invoke_llm(prompt)
    print("\nCODE GENERATED SUCCESSFULLY")

    return {
        "generated_code": generated_code
    }

## REVIEW NODE
def review_node(state: AgentState)-> dict:
    ## READ: generated_code: str
    ## UPDATE: review_feedback: str
    print("\n =====================================")
    print("INSIDE REVIEWER NODE")
    print("\n =====================================")

    prompt = REVIEW_PROMPT.format(
        generated_code = state["generated_code"]
    )

    review_feedback = invoke_llm(prompt)

    print("\nCODE REVIEWED SUCCESSFULLY")

    return {
        "review_feedback": review_feedback
    }

## QA Node
def qa_node(state: AgentState)-> dict:
    """
    READS:    generated_code: str, review_feedback: str
    UPDATES:    qa_feedback: str, needs_fix: bool
    """
    print("\n =====================================")
    print("INSIDE QA NODE")
    print("\n =====================================")
    prompt = QA_PROMPT.format(
        generated_code = state["generated_code"],
        review_feedback = state["review_feedback"]
    )

    qa_feedback = invoke_llm(prompt)

    needs_fix = "NEEDS_FIX = YES" in qa_feedback.upper()

    print("\nQA AGENT RUN SUCCESSFULLY")
    print("Needs fix:", needs_fix)

    return {
        "qa_feedback": qa_feedback,
        "needs_fix": needs_fix
    }
    
## FIX Node
def fix_node(state: AgentState)-> dict:
    """
    READS:    requirement: str, generated_code: str, review_feedback: str, qa_feedback: str, iteration_count: int
    UPDATES:    generated_code: str, iteration_count: int
    """
    print("\n =====================================")
    print("INSIDE FIX NODE")
    print("\n =====================================")
    prompt = FIX_PROMPT.format(
        requirement = state["requirement"],
        generated_code = state["generated_code"],
        review_feedback = state["review_feedback"],
        qa_feedback = state["qa_feedback"]
    )

    improved_code = invoke_llm(prompt)

    new_iteration_count = (state["iteration_count"]+ 1)

    print("\nFIX NODE: CODE IMPROVED SUCCESSFULLY")
    print("Current iteration: ", new_iteration_count )

    return {
        "generated_code": improved_code, 
        "iteration_count": new_iteration_count
    }

## REPORT NODE
def report_node(state: AgentState)-> dict:
    """
    READS:    requirement: str, review_feedback: str, qa_feedback: str
    UPDATES:    final_report: str
    """
    print("\n =====================================")
    print("INSIDE REPORT NODE")
    print("\n =====================================")
    prompt = REPORT_PROMPT.format(
        requirement = state["requirement"], 
        review_feedback = state["review_feedback"],
        qa_feedback = state["qa_feedback"]
    )

    final_report = invoke_llm(prompt)

    print("\n FINAL REPORT GENERATED SUCCESSFULLY")

    return {
        "final_report": final_report
    }