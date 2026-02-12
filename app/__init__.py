from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Import from within the app package
from app.models import CodeInput
from app.agents import DocstringAgent

# Initialize App
app = FastAPI(title="Nasiko Docstring Agent")

# Initialize Agent
agent = DocstringAgent()

# Mount Static Files (Ensure 'static' folder exists in root)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/generate-docs/")
async def generate_docs(input_data: CodeInput):
    # 1. Generate Docs (LLM)
    doc_code = agent.generate_docstrings(input_data.code)
    
    # 2. Analyze Health (Tool)
    health_stats = agent.analyze_health(input_data.code)
    
    return {
        "documented_code": doc_code,
        "health": health_stats
    }

@app.get("/")
async def serve_ui():
    # Helper to find index.html
    return FileResponse(os.path.join("static", "index.html"))