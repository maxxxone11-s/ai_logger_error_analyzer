from fastapi import APIRouter
from app.services.embedding_service import get_embedding

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/test-embedding")
async def test_embedding():
    embedding = await get_embedding(
        "TypeError: NoneType object is not iterable"
    )

    return {
        "embedding_size": len(embedding),
        "first_10_values": embedding[:10]
    }