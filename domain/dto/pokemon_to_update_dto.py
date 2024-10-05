from typing import List, Dict


class PokemonToUpdateDto:
    def __init__(self, name: str, pokedex_number: int, abilities: List[str], sprites: Dict[str, str], types: List[str]):
        self.name = name
        self.pokedex_number = pokedex_number
        self.abilities = abilities
        self.sprites = sprites
        self.types = types
