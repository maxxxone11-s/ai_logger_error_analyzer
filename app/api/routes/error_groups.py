from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models.error_group import ErrorGroup
from app.models.error import Error
from app.schemas.error_group import ErrorGroupResponse
from app.schemas.error import ErrorResponse

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("/", response_model=list[ErrorGroupResponse])
async def get_groups(
    sort: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    query = select(ErrorGroup)

    if sort == "count":
        query = query.order_by(ErrorGroup.count.desc())

    result = await db.execute(query)
    groups = result.scalars().all()

    return groups

@router.get("/{group_id}/errors", response_model=list[ErrorResponse])
async def get_group_errors(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ErrorGroup).where(ErrorGroup.id == group_id)
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    result = await db.execute(
        select(Error).where(Error.group_id == group_id)
    )
    errors = result.scalars().all()

    return errors