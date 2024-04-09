from src.core.domain.colors.dto import ColorView
from src.core.domain.colors.repository import ColorRepository
from src.core.domain.palettes import requests, dto
from src.core.domain.palettes.repository import PaletteRepository


class PaletteService:
    def __init__(
            self
    ) -> None:
        self._repository = PaletteRepository()
        self.color_repository = ColorRepository()

    async def create(self, request: requests.CreatePalette, user_id: int) -> dto.Palette:
        create_data = dto.PaletteCreate.model_validate(request.model_dump())
        create_data.user_id = user_id
        return await self._repository.create(create_data)

    async def get_all(
            self,
            user_id: int
    ) -> list[dto.PaletteView]:
        return await self._repository.get_all(user_id=user_id)

    async def get(self, palette_id: int, user_id: int) -> dto.PaletteView:
        return await self._repository.get_by_id(palette_id=palette_id, user_id=user_id)

    async def update(self, request: requests.UpdatePalette, palette_id: int, user_id: int) -> dto.PaletteUpdate | None:
        palette_model = await self._repository.get_by_id(palette_id=palette_id, user_id=user_id)
        if palette_model is None:
            return None
        update_data = dto.PaletteUpdate.model_validate(request.model_dump())
        return await self._repository.update(update_data, palette_model)

    async def delete(self, palette_id: int, user_id: int, colors: list[ColorView] | None = None):
        if colors:
            await self.color_repository.delete(palette_id=palette_id, color_ids=[color.id for color in colors])
        return await self._repository.delete(palette_id=palette_id, user_id=user_id)
