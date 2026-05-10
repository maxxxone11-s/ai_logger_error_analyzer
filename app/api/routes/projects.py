from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse

from app.models.error import Error
from app.schemas.error import ErrorResponse

import secrets

router = APIRouter(prefix="/projects", tags=["projects"])

def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db)
): 
    project = Project(
        name=project_data.name,
        api_key=generate_api_key()
    )
    try:
        db.add(project)
        await db.commit()
        await db.refresh(project)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Project with this name or API key already exists")

    return project

@router.get("/", response_model=list[ProjectResponse])
async def get_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@router.get("/{project_id}/errors", response_model=list[ErrorResponse])
async def get_project_errors(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = await db.execute(
        select(Error).where(Error.project_id == project_id)
    )
    errors = result.scalars().all()

    return errors