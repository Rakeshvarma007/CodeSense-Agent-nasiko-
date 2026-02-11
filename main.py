from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import DocstringAgent
import uvicorn
import os

app = FastAPI(title="Nasiko Docstring Agent")

agent = DocstringAgent()

app.mount("/static", StaticFiles(directory="static"), name="static")

class CodeInput(BaseModel):
    code: str

@app.post("/generate-docs/")
async def generate_docs(input_data: CodeInput):
    # 1. Generate Docs (LLM)
    doc_code = agent.generate_docstrings(input_data.code)
    
    # 2. Analyze Health (Algorithmic) - We analyze the ORIGINAL code
    # (Documentation doesn't change logic complexity)
    health_stats = agent.analyze_health(input_data.code)
    
    return {
        "documented_code": doc_code,
        "health": health_stats
    }

@app.get("/")
async def serve_ui():
    return FileResponse(os.path.join("static", "index.html"))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)