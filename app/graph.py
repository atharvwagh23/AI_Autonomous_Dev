from langgraph.graph import StateGraph, END
from app.state import AgentState

from app.nodes import (developer_node, review_node, qa_node, fix_node, report_node)

## Step 1: Create graph builder
workflow = StateGraph(AgentState)

## Step 2: Register nodes
workflow.add_node("developer", developer_node)
workflow.add_node("review", review_node)
workflow.add_node("qa", qa_node)
workflow.add_node("fix", fix_node)
workflow.add_node("report", report_node)

## Step 3: Define the sequence of the nodes

## Step 3.a. Define entry point
workflow.set_entry_point("developer")

## 3.b. Define normal edges
workflow.add_edge("developer", "review")
workflow.add_edge("review", "qa")

## 3.c. Define conditional edges

def qa_router(state: AgentState) -> str:
    """
    DEfine what happens after QA, There are 2 possibilities:
    QA -> FIX
    QA -> Report
    and all of the fix is only with 1 iteration
    """
    print("\n=====================================================")
    print("QA router")
    print("=====================================================\n")
    print("Needs fix: ", state["needs_fix"])
    print("Iteration count: ", state["iteration_count"])

    if (state["needs_fix"] and state["iteration_count"] < 1
        ):
        print("Routing to FIX")
        return "fix"
    print("Routing to Report")
    return "report"

workflow.add_conditional_edges("qa", qa_router)

workflow.add_edge("fix", "review")

workflow.add_edge("report", END)

## Step 4: Compile Graph
graph = workflow.compile()