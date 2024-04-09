from pydantic import BaseModel

from src.common.base_dto import PydanticBaseModel


class PaletteList(PydanticBaseModel):
    name: str
    id: int


class PaletteResponse(BaseModel):
    palettes: list[PaletteList]
