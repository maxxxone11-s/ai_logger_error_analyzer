from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
# create_async_engine - подключение к БД
# async_sessionmaker - фабрика сессий (работа с БД)

engine = create_async_engine(
    settings.database_url,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

