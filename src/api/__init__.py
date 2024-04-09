from fastapi import APIRouter

from .users import user_router
from .palettes import palette_router
from .colors import color_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(router=user_router, prefix="/user")
api_router.include_router(router=palette_router, prefix="/palette")
api_router.include_router(router=color_router, prefix="/color")
