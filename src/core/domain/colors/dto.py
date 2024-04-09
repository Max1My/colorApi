from pydantic import Field, BaseModel

from src.common.base_dto import PydanticBaseModel
from src.core.domain.palettes.dto import PaletteView


class Color(PydanticBaseModel):
    name: str
    hex_color: str
    palette_id: int


class ColorView(Color):
    palette: PaletteView | None = Field(exclude=True, example="")


class ColorCreate(BaseModel):
    name: str
    hex_color: str
    palette_id: int


class ColorUpdate(BaseModel):
    name: str
    hex_color: str
