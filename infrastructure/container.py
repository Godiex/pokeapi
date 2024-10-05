from dependency_injector import containers, providers

from api import Handlers
from application.get_general.get_general_handler import GetGeneralHandler
from application.get_specific.get_specific_handler import GetSpecificHandler
from application.update_pokemon.update_pokemon_handler import UpdatePokemonHanlder
from domain.services.pokemon_service import PokemonService
from infrastructure.adapters.pokemon_repository_implementation import PokemonRepositoryImplementation


class Container(containers.DeclarativeContainer):
    """
    Contenedor de dependencias para la aplicación, configurado con dependency_injector.

    Este contenedor proporciona las dependencias necesarias para la aplicación, incluyendo repositorios,
    servicios y manejadores. Se usa la configuración declarativa de dependency_injector para definir
    las relaciones entre las clases.
    """

    wiring_config = containers.WiringConfiguration(modules=Handlers.modules())
    """
    Configura el módulo de handlers para el wiring de dependencias automáticas. 
    Define cómo los módulos de la API recibirán las dependencias inyectadas automáticamente.
    """

    pokemon_repository = providers.Singleton(
        PokemonRepositoryImplementation
    )
    """
    Proveedor de una instancia singleton de `PokemonRepositoryImplementation`, que es el repositorio 
    encargado de manejar las operaciones relacionadas con Pokémon en la base de datos y en la API.
    """

    pokemon_service = providers.Factory(
        PokemonService,
        pokemon_repository=pokemon_repository
    )
    """
    Proveedor de una fábrica de instancias del servicio `PokemonService`. La fábrica inyecta 
    el repositorio de Pokémon como dependencia para realizar operaciones sobre los Pokémon.
    """

    get_specific_handler = providers.Factory(
        GetSpecificHandler,
        pokemon_repository=pokemon_repository
    )
    """
    Proveedor de una fábrica de instancias de `GetSpecificHandler`, que maneja las consultas específicas de Pokémon.
    El repositorio de Pokémon es inyectado como dependencia.
    """

    get_general_handler = providers.Factory(
        GetGeneralHandler,
        pokemon_repository=pokemon_repository
    )
    """
    Proveedor de una fábrica de instancias de `GetGeneralHandler`, que maneja las consultas generales de Pokémon.
    El repositorio de Pokémon es inyectado como dependencia.
    """

    update_pokemon_handler = providers.Factory(
        UpdatePokemonHanlder,
        pokemon_service=pokemon_service
    )
    """
    Proveedor de una fábrica de instancias de `UpdatePokemonHandler`, que maneja las actualizaciones de Pokémon.
    El servicio de Pokémon es inyectado como dependencia.
    """
