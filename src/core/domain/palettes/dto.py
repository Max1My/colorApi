from pydantic import Field, BaseModel

from src.common.base_dto import PydanticBaseModel
from src.core.domain.users.dto import UserView


class Palette(PydanticBaseModel):
    name: str
    user_id: int


class PaletteView(Palette):
    user: UserView | None = Field(exclude=True, example="")


class PaletteCreate(BaseModel):
    name: str
    user_id: int | None = None


class PaletteUpdate(BaseModel):
    name: str
