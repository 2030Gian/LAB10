from typing import Any, Optional
from pydantic import BaseModel, Field


class PokemonSearchRequest(BaseModel):
    pokemon_name: str = Field(..., examples=["charizard"])


class PokemonSearchResponse(BaseModel):
    name: str
    pokedex_id: Optional[int] = None
    types: list[str] = []
    abilities: list[str] = []
    stats: dict[str, Any]
    image_url: str


class HealthResponse(BaseModel):
    service: str
    status: str


class ErrorResponse(BaseModel):
    detail: str