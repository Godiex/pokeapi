from typing import List, Dict, Any
from pydantic import BaseModel


class SpecificPokemonDto(BaseModel):
    name: str
    pokedex_number: int
    abilities: List[str]
    sprites: Dict[str, Any]
    types: List[str]
