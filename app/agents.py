from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.config import Config
from app.tools import analyze_complexity

class DocstringAgent:
    def __init__(self):
        # Initialize Gemini Model using Config
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            temperature=0, 
            google_api_key=Config.GOOGLE_API_KEY
        )

    def analyze_health(self, code: str) -> dict:
        # Delegate the math to the tools module
        return analyze_complexity(code)

    def generate_docstrings(self, code_content: str) -> str:
        if not code_content.strip():
            return "Error: The provided code file is empty."

        template = """
        You are an expert Python documentation agent. Your task is to add high-quality Google-style docstrings.
        
        INSTRUCTIONS:
        1. Analyze classes, functions, and methods.
        2. Generate clear docstrings (Description, Args, Returns, Raises).
        3. Do not wrap in markdown blocks. Return ONLY the code.

        SOURCE CODE:
        {code}

        MODIFIED CODE WITH DOCSTRINGS:
        """
        
        prompt = PromptTemplate(template=template, input_variables=["code"])
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({"code": code_content})
            content = response.content
            
            # --- FIX STARTS HERE ---
            # Handle cases where Gemini returns a list of content parts
            if isinstance(content, list):
                # Extract 'text' if it's a dict, otherwise stringify strictly
                cleaned_parts = []
                for part in content:
                    if isinstance(part, dict):
                        cleaned_parts.append(part.get("text", ""))
                    elif hasattr(part, "text"):  # Some objects have a .text attribute
                        cleaned_parts.append(part.text)
                    else:
                        cleaned_parts.append(str(part))
                content = "".join(cleaned_parts)
            # --- FIX ENDS HERE ---
            
            # Clean up Markdown backticks if the model ignores instructions
            clean_content = str(content).replace("```python", "").replace("```", "").strip()
            return clean_content
            
        except Exception as e:
            return f"Error generating docstrings: {str(e)}"