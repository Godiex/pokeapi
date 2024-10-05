from domain.dto.pokemon_to_update_dto import PokemonToUpdateDto
from domain.entities.pokemon import Pokemon
from domain.repositories.pokemon_repository import PokemonRepository


class PokemonService:
    """
    Servicio para gestionar las operaciones relacionadas con los Pokémon, tales como actualizaciones y consultas.

    Este servicio actúa como una capa entre los repositorios y la lógica de negocio, permitiendo realizar
    operaciones como la actualización de la información de un Pokémon.
    """

    def __init__(self, pokemon_repository: PokemonRepository) -> None:
        """
        Inicializa la instancia del servicio con el repositorio de Pokémon.

        :param pokemon_repository: El repositorio de Pokémon para realizar las operaciones de almacenamiento y consulta.
        """
        self.__pokemon_repository = pokemon_repository

    async def update(self, pokemon_to_update: PokemonToUpdateDto) -> None:
        """
        Actualiza la información de un Pokémon existente en el repositorio.

        Busca el Pokémon por su número de Pokédex. Si se encuentra, actualiza sus propiedades (nombre, habilidades, sprites, tipos).
        Si no se encuentra, lanza una excepción.

        :param pokemon_to_update: Objeto DTO que contiene los datos a actualizar para el Pokémon.
        :raises Exception: Si el Pokémon no es encontrado en el repositorio.
        :return: None
        """
        pokemon_searched: Pokemon = await self.__pokemon_repository.get_one(pokemon_to_update.pokedex_number)
        if pokemon_searched is None:
            raise Exception("Pokemon not found")
        pokemon_searched.update(
            name=pokemon_to_update.name,
            abilities=pokemon_to_update.abilities,
            sprites=pokemon_to_update.sprites,
            types=pokemon_to_update.types
        )
        await self.__pokemon_repository.update(pokemon_searched)
