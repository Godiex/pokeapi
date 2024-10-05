from abc import ABC, abstractmethod
from typing import List
from domain.dto.general_pokemon_dto import GeneralPokemonDto
from domain.dto.specific_pokemon_dto import SpecificPokemonDto
from domain.entities.pokemon import Pokemon


class PokemonRepository(ABC):

    @abstractmethod
    async def get_general(self, data_to_search: str = None) -> List[GeneralPokemonDto]:
        """
        Método para obtener una lista de consultas generales de Pokémon.
        Si no se pasa `data_to_search`, devuelve una lista de todos los Pokémon disponibles.
        """
        pass

    @abstractmethod
    async def get_specific(self, data_to_search: str = None) -> List[SpecificPokemonDto]:
        """
        Método para obtener una lista de consultas específicas de Pokémon.
        Si no se pasa `data_to_search`, devuelve una lista de todos los Pokémon disponibles.
        """
        pass

    @abstractmethod
    async def update(self, pokemon: Pokemon) -> None:
        """
        Método para actualizar los datos de un Pokémon.
        """
        pass

    @abstractmethod
    async def get_one(self, pokedex_number: int) -> Pokemon:
        """
        Método para obtener un Pokémon específico por su número de Pokédex.
        """
        pass
