from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.core.domain.colors import requests
from src.core.domain.colors.response import ColorResponse, ColorList
from src.core.domain.colors.service import ColorService
from src.core.domain.colors import errors
from src.core.domain.palettes.response import PaletteResponse, PaletteList
from src.core.domain.palettes.service import PaletteService
from src.core.domain.users.auth import Auth
from src.core.domain.users.dto import UserView

color_router = APIRouter()
service = ColorService()
palette_service = PaletteService()


@color_router.get(
    path='/palette/{palette_id}',
    status_code=status.HTTP_200_OK,
    tags=['Цвет'],
    name='Получить все цвета палитры',
)
async def get_all_palettes(
        palette_id: int,
        user: Annotated[UserView, Depends(Auth())]
):
    palette = await palette_service.get(user_id=user.id, palette_id=palette_id)
    if palette is None:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось прочитать всех палитр'
        )
    colors = await service.get_all(palette_id=palette_id)
    if colors is None:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось прочитать всех цветов'
        )
    return ColorResponse(
        colors=[ColorList(
            id=color.id,
            name=color.name,
            hex_color=color.hex_color
        ) for color in colors],
        palette=PaletteResponse(
            palettes=[PaletteList(
                id=palette.id,
                name=palette.name
            )]
        )
    )


@color_router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Цвет'],
    name='Получить цвет'
)
async def get_palette(
        id: int,
        user: Annotated[UserView, Depends(Auth())]
):
    color_model = await service.get(color_id=id)
    if color_model is None:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Цвет не найден'
        )
    palette = await palette_service.get(user_id=user.id, palette_id=color_model.palette_id)
    if palette is None:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось прочитать палитру'
        )
    return ColorResponse(
        colors=[ColorList(
            id=color_model.id,
            name=color_model.name,
            hex_color=color_model.hex_color
        )],
        palette=PaletteResponse(
            palettes=[PaletteList(
                id=palette.id,
                name=palette.name
            )]
        )
    )


@color_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    tags=['Цвет'],
    name='Создать цвет',
)
async def create_color(
        request: requests.CreateColor,
        user: Annotated[UserView, Depends(Auth())]
):
    palette = await palette_service.get(user_id=user.id, palette_id=request.palette_id)
    if palette is None:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось прочитать палитру'
        )
    color = await service.create(request=request)


@color_router.put(
    path='/{id}',
    status_code=200,
    tags=['Цвет'],
    name='Обновить цвет'
)
async def update_color(
        id: int,
        request: requests.UpdateColor,
        user: Annotated[UserView, Depends(Auth())]
):
    palette = await palette_service.get(user_id=user.id, palette_id=request.palette_id)
    if palette is None:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось прочитать палитру'
        )
    updated_color = await service.update(request=request, color_id=id)
    return updated_color


@color_router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Цвет'],
    name='Удалить цвет'
)
async def delete_color(
        id: int,
        user: Annotated[UserView, Depends(Auth())]
):
    color_model = await service.get(color_id=id)
    if not color_model:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось найти цвет'
        )
    palette = await palette_service.get(user_id=user.id, palette_id=color_model.palette_id)
    if palette is None:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось прочитать палитру'
        )
    deleted_color = await service.delete(palette_id=palette.id, color_id=color_model.id)
    if not deleted_color:
        raise errors.ColorHTTPError(
            status_code=status.HTTP_409_CONFLICT,
            detail='Не удалось удалить цвет'
        )
    return True
