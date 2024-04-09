from pydantic import BaseModel


class CreateColor(BaseModel):
    hex_color: str
    palette_id: int


class UpdateColor(CreateColor):
    ...
