from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.error import Error
from app.schemas.analysis import AnalyzeResponse
from app.services.ai_analyzer import analyze_error

router = APIRouter(prefix="/errors", tags=["analyze"])

@router.post("/{error_id}/analyze", response_model=AnalyzeResponse)
async def create_analyze(
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
            detail="This error has no embedding yet"
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

    similar_errors = [
        f"Message: {item.message}\nSource: {item.source}\nStack trace: {item.stack_trace}"
        for item, distance in rows
        if float(distance) <= MAX_DISTANCE
    ]

    try:
        ai_result = await analyze_error(
            message=error.message,
            stack_trace=error.stack_trace,
            similar_errors=similar_errors
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return AnalyzeResponse(
        error_id=error.id,
        summary=ai_result["summary"],
        possible_reason=ai_result.get("possible_reason"),
        suggested_fix=ai_result["suggested_fix"]
    )
