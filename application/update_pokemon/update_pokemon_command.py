from pydantic import BaseModel
from typing import List, Dict, Any


class UpdatePokemonDto(BaseModel):
    name: str
    abilities: List[str]
    sprites: Dict[str, Any]
    types: List[str]

