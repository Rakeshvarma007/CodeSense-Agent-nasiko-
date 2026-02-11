import os

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def save_file_content(file_path: str, content: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)