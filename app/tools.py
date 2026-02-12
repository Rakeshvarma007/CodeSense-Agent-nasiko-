import radon.complexity as radon_cc
import os

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def analyze_complexity(code: str) -> dict:
    """Calculates Cyclomatic Complexity using Radon."""
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
        
        # Grading Scale
        if avg_complexity <= 5:
            return {"score": round(avg_complexity, 1), "rank": "A", "label": "Clean Code"}
        elif avg_complexity <= 10:
            return {"score": round(avg_complexity, 1), "rank": "B", "label": "Maintainable"}
        elif avg_complexity <= 20:
            return {"score": round(avg_complexity, 1), "rank": "C", "label": "Complex"}
        else:
            return {"score": round(avg_complexity, 1), "rank": "F", "label": "Spaghetti"}
            
    except Exception:
        return {"score": 0, "rank": "?", "label": "Syntax Error"}