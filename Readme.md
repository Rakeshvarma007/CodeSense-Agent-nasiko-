#  Nasiko Docstring Agent + Code Health Analyzer

This AI agent, built for the **Epoch X Nasiko Hackathon**, goes beyond simple documentation. It acts as an intelligent consultant that automatically generates professional Google-style docstrings *and* grades the maintainability of your Python code in real-time.

##  Features
### Intelligent Documentation
- **Context Aware:** Understands classes, methods, and complex logic to write meaningful descriptions.
- **Google Style:** Generates standard `Args`, `Returns`, and `Raises` sections automatically.
- **Robust:** Handles edge cases like empty files or incomplete code snippets without crashing.

### Code Health Engine (The "Wow" Factor)
- **Complexity Analysis:** Uses the **Radon** library to calculate Cyclomatic Complexity.
- **Grading System:** Assigns a "Health Grade" from **A (Clean Code)** to **F (Spaghetti Code)**.
- **Visual Badges:** Displays dynamic, color-coded badges in the UI to give instant feedback on code quality.

## Tech Stack
- **Framework:** FastAPI (Async REST API)
- **LLM Orchestration:** LangChain
- **Model:** Google Gemini (`gemini-flash-latest`)
- **Analysis Engine:** Radon (Cyclomatic Complexity)
- **Frontend:** HTML5/JS with Multi-Theme support (Aurora, Cyberpunk, SaaS)

## Agent Design
The agent operates as a dual-process microservice:
1.  **Input:** Accepts raw Python code via the `/generate-docs/` endpoint.
2.  **Parallel Processing:**
    * **Generation:** A prompt template directs Google Gemini to document the code without altering logic.
    * **Analysis:** The `radon` library computes the complexity score mathematically.
3.  **Output:** Returns a JSON object containing the `documented_code` and a `health` report (Score, Rank, and Label).

## Usage Instructions

### 1. Setup
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt