from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.error import Error
from app.models.project import Project
from app.schemas.error import ErrorCreate, ErrorResponse
from app.models.error_group import ErrorGroup
from app.services.embedding_service import get_embedding
from app.schemas.similar_error import SimilarErrorResponse

router = APIRouter(prefix="/errors", tags=["errors"])

@router.post("/", response_model=ErrorResponse)
async def create_error(
    error_data: ErrorCreate,
    db: AsyncSession = Depends(get_db)
):
    # Найти проект
    result = await db.execute(
        select(Project).where(Project.api_key == error_data.api_key)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # Формируем signature
    signature = f"{error_data.message}:{error_data.source}"
    # Найти группу
    result = await db.execute(
        select(ErrorGroup).where(ErrorGroup.signature == signature)
    )
    group = result.scalar_one_or_none()

    # Если есть - увеличить
    if group:
        group.count += 1
        await db.commit()
    else:
        group = ErrorGroup(
            signature=signature,
            count=1
        )
        db.add(group)
        await db.commit()
        await db.refresh(group)

    embedding_text = f"""
    Message: {error_data.message}
    Stack trace: {error_data.stack_trace}
    Source: {error_data.source}
    """

    embedding = await get_embedding(embedding_text)

    # Создаем ошибку
    error = Error(
        project_id=project.id,
        message=error_data.message,
        level=error_data.level,
        stack_trace=error_data.stack_trace,
        source=error_data.source,
        embedding=embedding,
        group_id=group.id
    )

    db.add(error)
    await db.commit()
    await db.refresh(error)

    return error

@router.get("/", response_model=list[ErrorResponse])
async def get_errors(
    level: str | None = Query(default=None),
    source: str | None = Query(default=None),
    limit: int = Query(default=10, le=100),
    offset: int = Query(default= 0),
    db: AsyncSession = Depends(get_db)
):
    query = select(Error)

    if level:
        query = query.where(Error.level == level)

    if source:
        query = query.where(Error.source == source)

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    errors = result.scalars().all()

    return errors

@router.get("/{error_id}", response_model=ErrorResponse)
async def get_error(
    error_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Error).where(Error.id == error_id)
    )
    error = result.scalar_one_or_none()

    if not error:
        raise HTTPException(status_code=404, detail="Error not found")
    return error

@router.get("/{error_id}/similar", response_model=list[SimilarErrorResponse])
async def errors_similar(
    error_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Error).where(Error.id == error_id)
    )

    error = result.scalar_one_or_none()

    if not error:
        raise HTTPException(status_code=404, detail="Error not found")
    
    if error.embedding is None:
        raise HTTPException(
            status_code=400,
            detail="This error has no similar error"
        )

    query_embedding = error.embedding
    distance = Error.embedding.cosine_distance(query_embedding).label("distance")

    result = await db.execute(
        select(Error, distance)
        .where(Error.id != error.id)
        .where(Error.embedding.is_not(None))
        .order_by(distance)
        .limit(5)
    )

    rows = result.all()

    MAX_DISTANCE = 0.35

    return [
        {"id": item.id, "message": item.message, "source": item.source, "distance": float(distance)} 
        for item, distance in rows
        if float(distance) <= MAX_DISTANCE
    ]   