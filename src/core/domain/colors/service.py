from src.core.domain.colors import requests, dto
from src.core.domain.colors.repository import ColorRepository
from src.core.domain.colors.utils import get_color_name


class ColorService:
    def __init__(
            self
    ) -> None:
        self._repository = ColorRepository()

    async def create(self, request: requests.CreateColor) -> dto.Color:
        request_data = request.model_dump()
        request_data["name"] = get_color_name(request.hex_color)
        create_data = dto.ColorCreate.model_validate(request_data)
        return await self._repository.create(create_data)

    async def get_all(
            self,
            palette_id: int
    ) -> list[dto.ColorView]:
        return await self._repository.get_all(palette_id=palette_id)

    async def get(self, color_id: int) -> dto.ColorView:
        return await self._repository.get_by_id(color_id=color_id)

    async def update(self, request: requests.UpdateColor, color_id: int) -> dto.ColorUpdate | None:
        color_model = await self._repository.get_by_id(color_id=color_id)
        if color_model is None:
            return None
        request_data = request.model_dump()
        request_data["name"] = get_color_name(request.hex_color)
        update_data = dto.ColorUpdate.model_validate(request_data)
        return await self._repository.update(update_data, color_model)

    async def delete(self, palette_id: int, color_id: int):
        return await self._repository.delete(palette_id=palette_id, color_ids=[color_id])
