from typing import Optional
from pydantic import BaseModel


class PokemonStatsResponse(BaseModel):
    pokedex_id: Optional[int] = None
    name: str
    type_1: Optional[str] = None
    type_2: Optional[str] = None
    total: Optional[int] = None
    hp: Optional[int] = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    sp_attack: Optional[int] = None
    sp_defense: Optional[int] = None
    speed: Optional[int] = None
    generation: Optional[int] = None
    legendary: Optional[bool] = None


class ErrorResponse(BaseModel):
    detail: str