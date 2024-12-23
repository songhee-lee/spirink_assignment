from pydantic import BaseModel

class ChatResponse(BaseModel):
    status_code : int
    generated_text : str | None = None
    error : str | None = None