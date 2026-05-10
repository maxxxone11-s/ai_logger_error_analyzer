from datetime import datetime
from pydantic import BaseModel

class ErrorGroupResponse(BaseModel):
    id: int
    signature: str
    count: int
    created_at: datetime

    class Config:
        from_attributes = True