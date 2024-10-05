from application.get_general.get_general_query import GetGeneralQuery
from domain.repositories.pokemon_repository import PokemonRepository


class GetGeneralHandler:
    """
    Manejador encargado de procesar las consultas generales para obtener una lista de Pokémon.

    Esta clase utiliza el repositorio de Pokémon para realizar consultas generales,
    ya sea buscando un Pokémon específico o devolviendo una lista de todos los Pokémon disponibles.
    """

    def __init__(self, pokemon_repository: PokemonRepository) -> None:
        """
        Inicializa el manejador con una instancia de `PokemonRepository`.

        Args:
            pokemon_repository (PokemonRepository): El repositorio que maneja el acceso a los datos de Pokémon.
        """
        self.__pokemon_repository = pokemon_repository

    async def handler(self, query: GetGeneralQuery):
        """
        Maneja la solicitud para obtener una lista general de Pokémon.

        Si la consulta contiene un valor en `data_to_search`, se realiza una búsqueda específica.
        De lo contrario, se devuelve una lista con todos los Pokémon disponibles.

        Args:
            query (GetGeneralQuery): La consulta que puede contener un nombre o número de Pokédex para la búsqueda,
            o estar vacía para obtener una lista general.

        Returns:
            List[GeneralPokemonDto]: Lista de los Pokémon encontrados o una lista vacía si no se encuentran resultados.
        """
        return await self.__pokemon_repository.get_general(query.data_to_search)
