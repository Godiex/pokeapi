import pytest
from unittest.mock import AsyncMock
from domain.entities.pokemon import Pokemon
from domain.dto.pokemon_to_update_dto import PokemonToUpdateDto
from domain.services.pokemon_service import PokemonService
from domain.repositories.pokemon_repository import PokemonRepository

# Data fake para las pruebas
FAKE_POKEMON_DATA = Pokemon(
    name="Pikachu",
    pokedex_number=25,
    abilities=["static", "lightning-rod"],
    sprites={"front_default": "fake_url"},
    types=["electric"]
)

FAKE_POKEMON_TO_UPDATE = PokemonToUpdateDto(
    name="Pikachu Updated",
    pokedex_number=25,
    abilities=["static", "lightning-rod"],
    sprites={"front_default": "fake_url_updated"},
    types=["electric"]
)


@pytest.mark.asyncio
async def test_update_pokemon_success():
    """Prueba un caso exitoso de actualización de Pokémon"""
    mock_repo = AsyncMock(PokemonRepository)
    # Simular que el Pokémon se encuentra en la base de datos
    mock_repo.get_one.return_value = FAKE_POKEMON_DATA

    # Crear el servicio
    pokemon_service = PokemonService(mock_repo)

    # Ejecutar la actualización
    await pokemon_service.update(FAKE_POKEMON_TO_UPDATE)

    # Verificar que el método update fue llamado una vez con los datos actualizados
    mock_repo.update.assert_called_once()
    assert mock_repo.update.call_args[0][0].name == "Pikachu Updated"
    assert mock_repo.update.call_args[0][0].sprites["front_default"] == "fake_url_updated"


@pytest.mark.asyncio
async def test_update_pokemon_not_found():
    """Prueba cuando el Pokémon no se encuentra en la base de datos"""
    mock_repo = AsyncMock(PokemonRepository)
    # Simular que no se encuentra el Pokémon
    mock_repo.get_one.return_value = None

    pokemon_service = PokemonService(mock_repo)

    with pytest.raises(Exception, match="Pokemon not found"):
        await pokemon_service.update(FAKE_POKEMON_TO_UPDATE)

    # Asegurarse de que el método update no fue llamado
    mock_repo.update.assert_not_called()

