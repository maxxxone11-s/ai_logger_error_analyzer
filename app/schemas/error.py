from datetime import datetime
from pydantic import BaseModel

class ErrorCreate(BaseModel):
    api_key: str
    message: str
    level: str = "error"
    stack_trace: str | None = None
    source: str | None = None

class ErrorResponse(BaseModel):
    id: int
    project_id: int
    message: str
    level: str
    stack_trace: str | None
    source: str | None
    created_at: datetime

    class Config:
        from_attributes = True
        