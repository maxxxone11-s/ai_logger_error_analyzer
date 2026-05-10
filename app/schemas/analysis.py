from pydantic import BaseModel

class AnalyzeResponse(BaseModel):
    error_id: int
    summary: str
    possible_reason: str | None
    suggested_fix: str