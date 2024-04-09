from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.core.domain.colors.service import ColorService
from src.core.domain.palettes import requests
from src.core.domain.palettes.response import PaletteResponse, PaletteList
from src.core.domain.palettes.service import PaletteService
from src.core.domain.palettes import errors
from src.core.domain.users.auth import Auth
from src.core.domain.users.dto import UserView

palette_router = APIRouter()
service = PaletteService()
color_service = ColorService()


@palette_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Палитра'],
    name='Получить все палитры пользователя',
)
async def get_all_palettes(
        user: Annotated[UserView, Depends(Auth())]
):
    palettes = await service.get_all(user_id=user.id)
    if palettes is None:
        raise errors.PaletteHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось прочитать всех палитр'
        )
    return PaletteResponse(
        palettes=[PaletteList(
            id=palette.id,
            name=palette.name
        ) for palette in palettes]
    )


@palette_router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Палитра'],
    name='Получить палитру'
)
async def get_palette(
        id: int,
        user: Annotated[UserView, Depends(Auth())]
):
    palette_model = await service.get(user_id=user.id, palette_id=id)
    if palette_model is None:
        raise errors.PaletteHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Палитра не найдена'
        )
    return PaletteResponse(
        palettes=[PaletteList(
            id=palette_model.id,
            name=palette_model.name
        )]
    )


@palette_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    tags=['Палитра'],
    name='Создать палитру',
)
async def create_palette(
        request: requests.CreatePalette,
        user: Annotated[UserView, Depends(Auth())]
):
    palette_model = await service.create(request=request, user_id=user.id)
    if not palette_model:
        raise errors.PaletteHTTPError(
            status_code=status.HTTP_409_CONFLICT,
            detail='Не удалось создать палитру'
        )


@palette_router.put(
    path='/{id}',
    status_code=200,
    tags=['Палитра'],
    name='Обновить палитру'
)
async def update_palette(
        id: int,
        request: requests.UpdatePalette,
        user: Annotated[UserView, Depends(Auth())]
):
    updated_palette = await service.update(request=request, palette_id=id, user_id=user.id)
    if not updated_palette:
        raise errors.PaletteHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Палитра не найдена'
        )


@palette_router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Палитра'],
    name='Удалить палитру'
)
async def delete_palette(
        id: int,
        user: Annotated[UserView, Depends(Auth())]
):
    colors = await color_service.get_all(palette_id=id)
    deleted_palette = await service.delete(palette_id=id, user_id=user.id, colors=colors)
    if not deleted_palette:
        raise errors.PaletteHTTPError(
            status_code=status.HTTP_409_CONFLICT,
            detail='Не удалось удалить палитру'
        )
    return True
