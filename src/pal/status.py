from fastapi import APIRouter


status_router = APIRouter()


@status_router.get("/health")
async def get_health():
    return {"message": "I am alive!"}
