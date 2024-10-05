from application.get_specific.get_specific_query import GetSpecificQuery
from domain.repositories.pokemon_repository import PokemonRepository


class GetSpecificHandler:
    """
    Manejador encargado de procesar las consultas para obtener un Pokémon específico.

    Esta clase utiliza el repositorio de Pokémon para realizar la búsqueda de un Pokémon específico
    basado en el nombre o número de Pokédex proporcionado en la consulta.
    """

    def __init__(self, pokemon_repository: PokemonRepository) -> None:
        """
        Inicializa el manejador con una instancia de `PokemonRepository`.

        Args:
            pokemon_repository (PokemonRepository): El repositorio que maneja el acceso a los datos de Pokémon.
        """
        self.__pokemon_repository = pokemon_repository

    async def handler(self, query: GetSpecificQuery):
        """
        Maneja la solicitud para obtener un Pokémon específico.

        Utiliza el repositorio de Pokémon para realizar la búsqueda basándose en el nombre o número de Pokédex
        proporcionado en la consulta `GetSpecificQuery`.

        Args:
            query (GetSpecificQuery): La consulta que contiene el nombre o número de Pokédex del Pokémon a buscar.

        Returns:
            List[SpecificPokemonDto]: Lista con la información del Pokémon encontrado, o una lista vacía si no se encuentra.
        """
        return await self.__pokemon_repository.get_specific(query.data_to_search)
