from pydantic import BaseModel

from src.common.base_dto import PydanticBaseModel
from src.core.domain.palettes.response import PaletteResponse


class ColorList(PydanticBaseModel):
    name: str
    hex_color: str
    id: int


class ColorResponse(BaseModel):
    colors: list[ColorList]
    palette: PaletteResponse
