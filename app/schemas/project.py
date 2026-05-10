from datetime import datetime
from pydantic import BaseModel

class ProjectCreate(BaseModel): # входящие данные
    name: str

class ProjectResponse(BaseModel): # возврат клиенту
    id: int
    name: str
    api_key: str
    created_at: datetime

    class Config:
        from_attributes = True # можно превращать ORM-объект в JSON