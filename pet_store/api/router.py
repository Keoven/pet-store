from fastapi import APIRouter

from .endpoints import pet_router


api_router = APIRouter()
api_router.include_router(pet_router, prefix='/pet', tags=['pet'])
