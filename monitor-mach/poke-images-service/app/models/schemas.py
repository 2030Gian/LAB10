from pydantic import BaseModel


class PokemonImageResponse(BaseModel):
    name: str
    image_url: str
    relative_path: str


class ErrorResponse(BaseModel):
    detail: str