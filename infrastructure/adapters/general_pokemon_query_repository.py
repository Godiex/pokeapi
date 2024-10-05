import sqlite3
import aiohttp
from typing import List
from domain.dto.general_pokemon_dto import GeneralPokemonDto


class GeneralPokemonQueryRepository:
    def __init__(self, db_path: str, api_url: str):
        self.db_path = db_path
        self.api_url = api_url
        self.HTTP_OK = 200

    def get_single_from_db(self, data_to_search: str) -> GeneralPokemonDto | None:
        """
        Busca un Pokémon en la base de datos SQLite por nombre o número de Pokédex.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, pokedex_number FROM pokemon WHERE name LIKE ? OR pokedex_number=?",
                       (f'%{data_to_search}%', data_to_search))
        result = cursor.fetchone()
        conn.close()

        if result:
            name, pokedex_number = result
            return GeneralPokemonDto(name=name, resource=f"{self.api_url}{pokedex_number}/")
        return None

    def get_all_from_db(self) -> List[GeneralPokemonDto]:
        """
        Devuelve la lista de todos los Pokémon desde la base de datos.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, pokedex_number FROM pokemon")
        results = cursor.fetchall()
        conn.close()

        return [GeneralPokemonDto(name=name, resource=f"{self.api_url}{pokedex_number}/")
                for name, pokedex_number in results]

    async def get_single_from_api(self, data_to_search: str) -> List[GeneralPokemonDto]:
        """
        Busca un Pokémon específico en la API de PokeAPI por nombre o número.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}{data_to_search}") as response:
                if response.status != self.HTTP_OK:
                    return []
                data = await response.json()
                return [GeneralPokemonDto(name=data["name"], resource=f"{self.api_url}{data['id']}/")]

    async def get_all_from_api(self) -> List[GeneralPokemonDto]:
        """
        Devuelve la lista de todos los Pokémon desde la API (limitada a 100 resultados).
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}?limit=100") as response:
                if response.status != self.HTTP_OK:
                    return []
                data = await response.json()
                return [GeneralPokemonDto(name=item["name"], resource=item["url"]) for item in data["results"]]
