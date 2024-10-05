import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from domain.entities.pokemon import Pokemon
from domain.dto.general_pokemon_dto import GeneralPokemonDto
from domain.dto.specific_pokemon_dto import SpecificPokemonDto

client = TestClient(app)


@pytest.mark.asyncio
@patch("infrastructure.adapters.pokemon_repository_implementation.PokemonRepositoryImplementation.get_specific")
async def test_get_pokemon_by_pokedex_number_found(mock_get_specific):
    """
    Test de integración que verifica que se puede encontrar un Pokémon por su número de Pokédex (endpoint /specific/{id}).
    """
    mock_get_specific.return_value = [
        SpecificPokemonDto(
            name="Pikachu",
            pokedex_number=25,
            abilities=["static", "lightning-rod"],
            sprites={"front_default": "https://pokeapi.co/sprites/pokemon/25.png"},
            types=["electric"]
        )
    ]

    response = client.get("/pokemon/specific?data_to_search=25")
    response_data = response.json()  # Convertimos la respuesta a JSON
    assert response.status_code == 200
    assert response_data[0]["name"] == "Pikachu"
    assert response_data[0]["pokedex_number"] == 25


@pytest.mark.asyncio
@patch("infrastructure.adapters.pokemon_repository_implementation.PokemonRepositoryImplementation.get_specific")
async def test_get_pokemon_by_pokedex_number_not_found(mock_get_specific):
    """
    Test de integración para un Pokémon que no existe por número de Pokédex (endpoint /specific/{id}).
    """
    mock_get_specific.return_value = []

    response = client.get("/pokemon/specific?data_to_search=9999")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == []


@pytest.mark.asyncio
@patch("infrastructure.adapters.pokemon_repository_implementation.PokemonRepositoryImplementation.get_general")
async def test_get_pokemon_by_name_found(mock_get_general):
    """
    Test de integración que verifica que se puede encontrar un Pokémon por su nombre (endpoint /general?data_to_search).
    """
    mock_get_general.return_value = [
        GeneralPokemonDto(
            name="Pikachu",
            resource="https://pokeapi.co/api/v2/pokemon/25/"
        )
    ]

    response = client.get("/pokemon/general?data_to_search=Pikachu")
    response_data = response.json()  # Convertimos la respuesta a JSON
    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["name"] == "Pikachu"


@pytest.mark.asyncio
@patch("infrastructure.adapters.pokemon_repository_implementation.PokemonRepositoryImplementation.get_general")
async def test_get_pokemon_by_name_not_found(mock_get_general):
    """
    Test de integración para un Pokémon que no existe por nombre (endpoint /general?data_to_search).
    """
    mock_get_general.return_value = []  # No se encontró el Pokémon

    response = client.get("/pokemon/general?data_to_search=Unknown")
    response_data = response.json()  # Convertimos la respuesta a JSON
    assert response.status_code == 200
    assert len(response_data) == 0  # No debe haber resultados


@pytest.mark.asyncio
@patch("infrastructure.adapters.pokemon_repository_implementation.PokemonRepositoryImplementation.get_one")
@patch("infrastructure.adapters.pokemon_repository_implementation.PokemonRepositoryImplementation.update")
async def test_update_pokemon_success(mock_update, mock_get_one):
    """
    Test de integración que verifica que un Pokémon puede actualizarse correctamente (endpoint /specific/{id}).
    """
    # Simular que el Pokémon se encuentra en la base de datos
    mock_get_one.return_value = Pokemon(
        name="Pikachu",
        pokedex_number=25,
        abilities=["static", "lightning-rod"],
        sprites={"front_default": "https://pokeapi.co/sprites/pokemon/25.png"},
        types=["electric"]
    )

    update_data = {
        "name": "Raichu",
        "abilities": ["static", "lightning-rod"],
        "sprites": {"front_default": "https://pokeapi.co/sprites/pokemon/26.png"},
        "types": ["electric"]
    }

    response = client.put("/pokemon/25", json=update_data)
    assert response.status_code == 200
    mock_update.assert_called_once()


@pytest.mark.asyncio
@patch("infrastructure.adapters.pokemon_repository_implementation.PokemonRepositoryImplementation.get_one")
@patch("infrastructure.adapters.pokemon_repository_implementation.PokemonRepositoryImplementation.update")
async def test_update_pokemon_not_found(mock_update, mock_get_one):
    """
    Test de integración para cuando no se encuentra el Pokémon a actualizar (endpoint /specific/{id}).
    """
    mock_get_one.return_value = None  # El Pokémon no existe

    update_data = {
        "name": "Raichu",
        "abilities": ["static", "lightning-rod"],
        "sprites": {"front_default": "https://pokeapi.co/sprites/pokemon/26.png"},
        "types": ["electric"]
    }

    response = client.put("/pokemon/9999", json=update_data)
    response_data = response.json()  # Convertimos la respuesta a JSON
    assert response.status_code == 400
    assert response_data == {'ExceptionType': 'Exception', 'message': 'Pokemon not found'}
