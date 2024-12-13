from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=['intro'])
async def root():
    return {"message": "Hello World"}