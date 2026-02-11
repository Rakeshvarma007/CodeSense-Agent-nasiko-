import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import radon.complexity as radon_cc

load_dotenv()

class DocstringAgent:
    def __init__(self):
        # Initialize Gemini Model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            temperature=0, 
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def analyze_health(self, code: str) -> dict:
        """Calculates Cyclomatic Complexity and assigns a grade."""
        try:
            if not code.strip():
                return {"score": 0, "rank": "N/A", "label": "Empty"}

            # Calculate Complexity
            results = radon_cc.cc_visit(code)
            
            # If no functions/classes, it's simple script code
            if not results:
                return {"score": 1, "rank": "A", "label": "Clean"}

            # Get average complexity
            avg_complexity = sum(r.complexity for r in results) / len(results)
            
            # Grading Scale (Standard CC scales)
            if avg_complexity <= 5:
                return {"score": round(avg_complexity, 1), "rank": "A", "label": "Clean Code"}
            elif avg_complexity <= 10:
                return {"score": round(avg_complexity, 1), "rank": "B", "label": "Maintainable"}
            elif avg_complexity <= 20:
                return {"score": round(avg_complexity, 1), "rank": "C", "label": "Complex"}
            else:
                return {"score": round(avg_complexity, 1), "rank": "F", "label": "Spaghetti"}
                
        except Exception:
            # Fallback for syntax errors
            return {"score": 0, "rank": "?", "label": "Syntax Error"}

    def generate_docstrings(self, code_content: str) -> str:
        # Edge Case: Empty file
        if not code_content.strip():
            return "Error: The provided code file is empty."

        template = """
        You are an expert Python documentation agent. Your task is to add high-quality Google-style docstrings to the following Python source code.
        
        INSTRUCTIONS:
        1. Analyze the code to understand classes, functions, and methods.
        2. Generate clear docstrings including:
           - Description of functionality
           - Args (with types if detectable)
           - Returns (with types)
           - Raises (if applicable)
        3. If the code is incomplete or syntactically incorrect, try to document what is visible but add a warning note at the top.
        4. OUTPUT FORMAT: Return ONLY the raw python code. Do not wrap it in markdown (no ```python blocks).

        SOURCE CODE:
        {code}

        MODIFIED CODE WITH DOCSTRINGS:
        """
        
        prompt = PromptTemplate(template=template, input_variables=["code"])
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({"code": code_content})
            content = response.content

            if isinstance(content, list):
                content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
            
            if "```python" in content:
                content = content.replace("```python", "").replace("```", "")
            elif "```" in content:
                content = content.replace("```", "")
                
            return content.strip()
            
        except Exception as e:
            return f"Error generating docstrings: {str(e)}"