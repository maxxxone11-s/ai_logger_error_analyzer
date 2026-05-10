from pydantic import BaseModel

class StatsResponse(BaseModel):
    projects_count: int
    errors_count: int
    groups_count: int
    errors_without_embedding: int