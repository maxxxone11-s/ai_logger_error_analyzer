from app.db.session import AsyncSessionLocal

async def get_db(): # каждый запрос получает свою session -> work -> closed
    async with AsyncSessionLocal() as session:
        yield session