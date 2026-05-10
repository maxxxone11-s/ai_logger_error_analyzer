# AI Logger & Error Analyzer

AI-powered система для логирования и анализа ошибок backend-приложений.

Demo client отправляет ошибки в основной FastAPI-сервис. Сервис валидирует данные через Pydantic-схемы, определяет проект по API key, группирует похожие ошибки по signature, создаёт embeddings через OpenRouter Embeddings API и сохраняет данные в PostgreSQL с использованием pgvector.

При анализе ошибки система выполняет semantic similarity search через cosine distance, фильтрует релевантные ошибки по threshold и передаёт их как RAG-context в LLM. Модель возвращает структурированный JSON-ответ с:
- summary
- possible_reason
- suggested_fix

Проект также включает lightweight dashboard на Jinja2 для просмотра ошибок и AI-анализа.

---

## Основные возможности

- Логирование ошибок через FastAPI API
- Группировка ошибок по signature
- Генерация embeddings через OpenRouter API
- Semantic search через pgvector
- RAG-анализ ошибок через LLM
- Dashboard на Jinja2
- Async архитектура
- PostgreSQL + SQLAlchemy + Alembic
- Docker support

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- pgvector
- OpenRouter API
- httpx
- Jinja2
- Docker
- Pydantic