from pydantic import BaseModel


class CreatePalette(BaseModel):
    name: str


class UpdatePalette(CreatePalette):
    ...
