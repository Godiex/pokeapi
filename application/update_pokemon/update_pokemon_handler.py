from application.update_pokemon.update_pokemon_command import UpdatePokemonDto
from domain.dto.pokemon_to_update_dto import PokemonToUpdateDto
from domain.services.pokemon_service import PokemonService


class UpdatePokemonHanlder:
    """
    Manejador encargado de procesar los comandos para actualizar los datos de un Pokémon.

    Esta clase convierte los datos recibidos en un formato adecuado y delega la lógica de actualización al
    servicio `PokemonService`. Recibe un número de Pokédex y los datos actualizados del Pokémon, y utiliza
    el servicio de Pokémon para ejecutar la operación de actualización.
    """

    def __init__(self, pokemon_service: PokemonService) -> None:
        """
        Inicializa el manejador con una instancia de `PokemonService`.

        Args:
            pokemon_service (PokemonService): El servicio que maneja la lógica de negocio para los Pokémon.
        """
        self.__pokemon_service = pokemon_service

    async def handler(self, pokedex_number: int, command: UpdatePokemonDto) -> None:
        """
        Maneja la solicitud de actualización de un Pokémon.

        Convierte los datos recibidos en una instancia de `PokemonToUpdateDto` y delega la actualización
        al servicio de Pokémon.

        Args:
            pokedex_number (int): El número de la Pokédex del Pokémon a actualizar.
            command (UpdatePokemonDto): El comando que contiene los datos del Pokémon que se deben actualizar.

        Raises:
            Exception: Si el Pokémon no es encontrado, se lanzará una excepción en el servicio de Pokémon.
        """
        pokemon_to_update: PokemonToUpdateDto = PokemonToUpdateDto(
            command.name,
            pokedex_number,
            command.abilities,
            command.sprites,
            command.types
        )
        await self.__pokemon_service.update(pokemon_to_update)
