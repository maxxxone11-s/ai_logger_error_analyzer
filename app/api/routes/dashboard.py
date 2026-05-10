from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

import httpx
import json

from app.api.deps import get_db
from app.models.error import Error

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def dashboards(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Error)
        .order_by(Error.created_at.desc())
        .limit(10)
    )

    errors = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "AI Error Analyzer Dashboard",
            "errors": errors
        }
    )

@router.get("/errors/{error_id}")
async def get_errors_id(
    error_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Error).where(Error.id == error_id)
    )
    
    error = result.scalar_one_or_none()

    if not error:
        raise HTTPException(status_code=404, detail="Error not found")
    
    return templates.TemplateResponse(
        request=request,
        name="error_detail.html",
        context={
            "error": error
        }
    )

@router.get("/errors/{error_id}/analyze")
async def analyze_error(
    error_id: int,
    request: Request
):
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"http://127.0.0.1:8000/errors/{error_id}/analyze"
            )

        data = response.json()

        return templates.TemplateResponse(
            request=request,
            name="analyze.html",
            context={
                "analysis": data
            }
        )
    except httpx.ReadTimeout:
        return templates.TemplateResponse(
            request=request,
            name="analyze.html",
            context={
                "analysis": {
                    "summary": "Analyze request timed out",
                    "possible_reason": "The AI model took too long to respond",
                    "suggested_fix": "Try again later or use another model"
                }
            }
        )

