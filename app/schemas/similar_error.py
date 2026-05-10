from pydantic import BaseModel

class SimilarErrorResponse(BaseModel):
    id: int
    message: str
    source: str | None
    distance: float