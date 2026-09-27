<div align="center">

# 🤖 AI Autonomous Dev Team

### A self-correcting, multi-agent LangGraph pipeline that writes, reviews, QA-checks, fixes, and reports on Python code — available as both a CLI and a Streamlit app

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://www.langchain.com/langgraph)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat&logo=groq&logoColor=white)](https://groq.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

</div>

---

## 📖 Overview

**AI Autonomous Dev Team** simulates a real software engineering team using a graph of specialized AI agents built with **LangGraph**. Give it a plain-English requirement, and it will:

1. 👨‍💻 **Write** the code
2. 🔍 **Review** it for bugs, style, and best practices
3. ✅ **QA-check** it against the review
4. 🔧 **Fix** it automatically if issues are found
5. 📄 **Report** a final engineering summary

The entire workflow is self-correcting — if QA flags an issue, the graph routes back through a **Fix** node and re-reviews before finalizing, instead of blindly returning the first draft.

Two ways to use it, both powered by the same LangGraph pipeline:
- 🖥️ **CLI** (`main.py`) — quick terminal-based runs
- 🌐 **Streamlit app** (`streamlit_app.py`) — full interactive UI with live results and function testing

---

## 🏗️ Architecture

```mermaid
flowchart TD
    S([📝 User Requirement]) --> D[👨‍💻 Developer Node]
    D --> R[🔍 Review Node]
    R --> Q[✅ QA Node]
    Q -->|Needs Fix & iterations < 1| F[🔧 Fix Node]
    Q -->|Passed / Max Iterations| P[📄 Report Node]
    F --> R
    P --> E([🎯 Final Report + Code])

    style S fill:#2b2f36,stroke:#fff,color:#fff
    style D fill:#F55036,stroke:#fff,color:#fff
    style R fill:#FBBC05,stroke:#fff,color:#000
    style Q fill:#34A853,stroke:#fff,color:#fff
    style F fill:#EA4335,stroke:#fff,color:#fff
    style P fill:#F55036,stroke:#fff,color:#fff
    style E fill:#2b2f36,stroke:#fff,color:#fff
```

### Self-correction loop

```mermaid
sequenceDiagram
    participant U as 📝 Requirement
    participant Dev as 👨‍💻 Developer
    participant Rev as 🔍 Reviewer
    participant QA as ✅ QA
    participant Fix as 🔧 Fix
    participant Rep as 📄 Report

    U->>Dev: Send requirement
    Dev->>Rev: Generated code
    Rev->>QA: Review feedback
    QA->>QA: needs_fix?
    alt Needs Fix (iteration < 1)
        QA->>Fix: Route to Fix
        Fix->>Rev: Improved code
        Rev->>QA: Re-review
    end
    QA->>Rep: Route to Report
    Rep->>U: Final engineering report
```

---

## 🧠 The Agent Team

| Node | Role |
|---|---|
| 👨‍💻 **Developer** | Writes the initial Python implementation from the requirement |
| 🔍 **Reviewer** | Critiques the code for bugs, performance, and style |
| ✅ **QA** | Decides pass/fail and whether a fix is needed |
| 🔧 **Fix** | Improves the code based on review + QA feedback (max 1 iteration) |
| 📄 **Report** | Summarizes the full engineering process into a final report |

---

## 📂 Project Structure

```text
langgraph_software_dev-agent/
│
├── app/
│   ├── graph.py            # LangGraph wiring — nodes, edges, routing logic
│   ├── nodes.py            # Agent logic (Developer/Review/QA/Fix/Report) + LLM setup
│   ├── prompts.py          # Prompt templates for each agent
│   └── state.py            # Shared LangGraph state schema
│
├── main.py                 # CLI entry point
├── streamlit_app.py         # Streamlit UI entry point
│
├── output_main_cli/         # Auto-created — CLI run outputs
├── output_streamlit/         # Auto-created — Streamlit run outputs
│
├── requirements.txt
├── pyproject.toml
├── .env                     # Your API key (not committed)
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/atharvwagh23/langgraph_software_dev-agent.git
cd langgraph_software_dev-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Set up your `.env` file

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

Get a free key from [console.groq.com](https://console.groq.com/keys).

### 5. Run the CLI version

```bash
.venv\Scripts\python.exe main.py
```

### 6. Run the Streamlit version

```bash
.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

The UI opens at `http://localhost:8501`.

---

## 🖥️ Output — CLI (`main.py`)

### 1️⃣ Running the workflow

The CLI walks through the full agent pipeline — **Developer → Review → QA → Fix (if needed) → Report** — printing each stage as it runs, and clearly shows the self-correction loop in action when QA flags an issue.

![CLI Full Run](photos_output/cli-full-run.jpg)

### 2️⃣ The payoff — final engineering report

Once QA passes (or the fix-iteration limit is reached), the graph produces a structured final report along with an execution summary.

![CLI Final Report](photos_output/cli-final-report.jpg)

### 3️⃣ Proof it's real, runnable code

The generated code is saved to `output_main_cli/generated_code.py`. Importing and running it confirms the AI-written function actually works correctly:

```bash
cd output_main_cli
python -c "from generated_code import is_palindrome; print('racecar:', is_palindrome('racecar')); print('hello:', is_palindrome('hello'));"
```

![Generated Code Output](photos_output/generated_code_output.jpg)

---

## 🌐 Output — Streamlit App

### 1️⃣ The interface

A clean, tabbed UI to enter a requirement and kick off the full agent workflow with one click.

![Streamlit Input](photos_output/streamlit-input.jpg)

### 2️⃣ Full demo video

See the complete workflow live — requirement submission, real-time agent progress, results across tabs, and interactively testing the generated function.

https://github.com/user-attachments/photos_output/langgraph-dev-team-demo.mp4

---

## ✅ Features

| Feature | CLI | Streamlit |
|---|:---:|:---:|
| Full agent pipeline (Dev → Review → QA → Fix → Report) | ✅ | ✅ |
| Self-correcting fix loop | ✅ | ✅ |
| Saves generated code + execution JSON | ✅ | ✅ |
| Interactive results view (tabs, metrics) | ❌ | ✅ |
| Live testing of generated functions | ❌ | ✅ |
| Separate output folders per interface | ✅ `output_main_cli/` | ✅ `output_streamlit/` |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| LLM Provider | Groq |
| Frontend (optional) | Streamlit |
| Language | Python 3.10+ |

<div align="center">

🚀 Built with **LangGraph**, **LangChain**, **Groq**, and **Streamlit**

</div>
