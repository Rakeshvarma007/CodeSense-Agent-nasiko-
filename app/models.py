from pydantic import BaseModel

class CodeInput(BaseModel):
    code: str
    style: str = "Google"