import httpx

from app.core.config import settings

EMBEDDING_MODEL = "openai/text-embedding-3-small"

async def get_embedding(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/embeddings",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": EMBEDDING_MODEL,
                "input": text
            }
        )

        response.raise_for_status()

        data = response.json()

        return data["data"][0]["embedding"]