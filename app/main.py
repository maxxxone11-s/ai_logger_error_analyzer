from fastapi import FastAPI
from app.core.config import settings
from sqlalchemy import text
from app.db.session import engine
from app.api.routes import projects, errors, error_groups, analysis, ai_embedding, stats, dashboard

app = FastAPI()

app.include_router(projects.router)
app.include_router(errors.router)
app.include_router(error_groups.router)
app.include_router(analysis.router)
app.include_router(ai_embedding.router)
app.include_router(stats.router)
app.include_router(dashboard.router)

@app.get("/health")
async def health():
    try:
        async with engine.begin() as conn: # engine.begin - открываем соединение 
            result = await conn.execute(text("SELECT 1")) # conn.execute - выполняем sql
            value = result.scalar()

        return {
            "status": "ok",
            "db_connection": value == 1
        }

    except Exception as e:
        return {
            "status": "error",
            "db_connection": False,
            "error": str(e)
        }

