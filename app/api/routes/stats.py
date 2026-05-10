from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_db
from app.schemas.stats import StatsResponse
from app.models.project import Project
from app.models.error_group import ErrorGroup
from app.models.error import Error

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    result_project = await db.execute(select(func.count(Project.id)))
    projects_count = result_project.scalar()

    result_errors = await db.execute(select(func.count(Error.id)))
    errors_count = result_errors.scalar()

    result_group = await db.execute(select(func.count(ErrorGroup.id)))
    group_count = result_group.scalar()

    result_without_embedding = await db.execute(select(func.count(Error.id)).where(Error.embedding.is_(None)))
    errors_without_embedding = result_without_embedding.scalar()
    
    return {
        "projects_count": projects_count,
        "errors_count": errors_count,
        "groups_count": group_count,
        "errors_without_embedding": errors_without_embedding
    }