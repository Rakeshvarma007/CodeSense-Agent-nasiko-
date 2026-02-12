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
        return analyze_complexity(code)

    def generate_docstrings(self, code_content: str, style: str = "Google") -> str:
        if not code_content.strip():
            return "Error: The provided code file is empty."

        # Dynamic Prompt Template
        template = """
        You are an expert Python documentation agent. Your task is to add high-quality docstrings following the {style} style.
        
        INSTRUCTIONS:
        1. Analyze classes, functions, and methods.
        2. Generate clear docstrings (Description, Args, Returns, Raises) using strictly {style} formatting.
        3. Do not wrap in markdown blocks. Return ONLY the code.
        4. if the code given is just random text , tell the user to input proper code for generating docstring.

        SOURCE CODE:
        {code}

        MODIFIED CODE WITH DOCSTRINGS:
        """
        
        # Pass both 'style' and 'code' to the prompt
        prompt = PromptTemplate(template=template, input_variables=["style", "code"])
        chain = prompt | self.llm
        
        try:
            # Invoke with both variables
            response = chain.invoke({"style": style, "code": code_content})
            content = response.content
            
            # Clean up response (Handle Gemini's list/dict responses)
            if isinstance(content, list):
                cleaned_parts = []
                for part in content:
                    if isinstance(part, dict):
                        cleaned_parts.append(part.get("text", ""))
                    elif hasattr(part, "text"):
                        cleaned_parts.append(part.text)
                    else:
                        cleaned_parts.append(str(part))
                content = "".join(cleaned_parts)
            
            clean_content = str(content).replace("```python", "").replace("```", "").strip()
            return clean_content
            
        except Exception as e:
            return f"Error generating docstrings: {str(e)}"