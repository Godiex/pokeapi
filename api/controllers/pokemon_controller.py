from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.get_general.get_general_handler import GetGeneralHandler
from application.get_general.get_general_query import GetGeneralQuery
from application.get_specific.get_specific_handler import GetSpecificHandler
from application.update_pokemon.update_pokemon_command import UpdatePokemonDto
from application.update_pokemon.update_pokemon_handler import UpdatePokemonHanlder
from domain.dto.general_pokemon_dto import GeneralPokemonDto
from domain.dto.specific_pokemon_dto import SpecificPokemonDto
from infrastructure.container import Container

from application.get_specific.get_specific_query import GetSpecificQuery

router = APIRouter(
    prefix='/pokemon',
    tags=['pokemon']
)


@router.get('/specific')
@inject
async def get_specific(
        data_to_search: Optional[str] = None,
        get_specific_handler: GetSpecificHandler = Depends(Provide[Container.get_specific_handler])
) -> list[SpecificPokemonDto]:
    """
    Endpoint para obtener detalles específicos de un Pokémon.

    Args:
        data_to_search (Optional[str]): Nombre o número de Pokédex del Pokémon a buscar. Si no se proporciona,
        se devuelve una lista vacía.
        get_specific_handler (GetSpecificHandler): Dependencia inyectada para manejar la consulta específica.

    Returns:
        list[SpecificPokemonDto]: Lista de Pokémon específicos encontrados. Devuelve una lista vacía si no
        se encuentra ningún resultado.
    """
    result = await get_specific_handler.handler(GetSpecificQuery(data_to_search=data_to_search))
    if isinstance(result, list) and all(isinstance(item, SpecificPokemonDto) for item in result):
        return [item.dict() for item in result]

    return []


@router.get('/general')
@inject
async def get_general(
        data_to_search: Optional[str] = None,
        get_general_handler: GetGeneralHandler = Depends(Provide[Container.get_general_handler])
) -> list[GeneralPokemonDto]:
    """
    Endpoint para obtener una lista general de Pokémon.

    Args:
        data_to_search (Optional[str]): Nombre o número de Pokédex del Pokémon a buscar. Si no se proporciona,
        se devuelve la lista completa de Pokémon.
        get_general_handler (GetGeneralHandler): Dependencia inyectada para manejar la consulta general.

    Returns:
        list[GeneralPokemonDto]: Lista general de Pokémon encontrados. Si no se encuentra ningún resultado,
        se devuelve una lista vacía.
    """
    result = await get_general_handler.handler(GetGeneralQuery(data_to_search=data_to_search))
    if isinstance(result, list) and all(isinstance(item, GeneralPokemonDto) for item in result):
        return [item.dict() for item in result]

    return []


@router.put('/{pokedex_number}')
@inject
async def update_pokemon(
        pokedex_number: int,
        pokemon_data: UpdatePokemonDto,
        update_pokemon_handler: UpdatePokemonHanlder = Depends(Provide[Container.update_pokemon_handler])
) -> None:
    """
    Endpoint para actualizar los detalles de un Pokémon.

    Args:
        pokedex_number (int): Número de Pokédex del Pokémon a actualizar.
        pokemon_data (UpdatePokemonDto): Datos actualizados del Pokémon, incluyendo nombre, habilidades, sprites y tipos.
        update_pokemon_handler (UpdatePokemonHanlder): Dependencia inyectada para manejar la actualización.

    Returns:
        None: Si la actualización es exitosa, no se devuelve contenido.
    """
    await update_pokemon_handler.handler(pokedex_number, pokemon_data)
