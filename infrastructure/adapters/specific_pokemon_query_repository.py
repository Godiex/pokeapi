import sqlite3
import aiohttp
from typing import List
from domain.dto.specific_pokemon_dto import SpecificPokemonDto
from domain.entities.pokemon import Pokemon


class SpecificPokemonQueryRepository:
    def __init__(self, db_path: str, api_url: str):
        self.db_path = db_path
        self.api_url = api_url
        self.HTTP_OK = 200

    def get_single_from_db(self, data_to_search: str) -> SpecificPokemonDto | None:
        """
        Busca un Pokémon específico en la base de datos SQLite por nombre o número de Pokédex.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, pokedex_number, abilities, sprites, types FROM pokemon WHERE name LIKE ? OR pokedex_number=?",
            (f'%{data_to_search}%', data_to_search))
        result = cursor.fetchone()
        conn.close()

        if result:
            name, pokedex_number, abilities, sprites, types = result
            return SpecificPokemonDto(name=name, pokedex_number=pokedex_number, abilities=abilities.split(','),
                                      sprites=eval(sprites), types=types.split(','))
        return None

    def get_all_from_db(self) -> List[SpecificPokemonDto]:
        """
        Devuelve la lista de todos los Pokémon desde la base de datos.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, pokedex_number, abilities, sprites, types FROM pokemon")
        results = cursor.fetchall()
        conn.close()

        return [SpecificPokemonDto(name=name, pokedex_number=pokedex_number, abilities=abilities.split(','),
                                   sprites=eval(sprites), types=types.split(','))
                for name, pokedex_number, abilities, sprites, types in results]

    async def get_single_from_api(self, data_to_search: str) -> List[SpecificPokemonDto]:
        """
        Busca un Pokémon específico en la API de PokeAPI por nombre o número de Pokédex.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}{data_to_search}") as response:
                if response.status != self.HTTP_OK:
                    return []
                data = await response.json()
                return [SpecificPokemonDto(name=data["name"], pokedex_number=data["id"],
                                           abilities=[ability['ability']['name'] for ability in data['abilities']],
                                           sprites=data['sprites'],
                                           types=[ptype['type']['name'] for ptype in data['types']])]

    async def get_all_from_api(self) -> List[SpecificPokemonDto]:
        """
        Devuelve una lista con los detalles de todos los Pokémon desde la API (limitada a 100 resultados).
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}?limit=100") as response:
                if response.status != self.HTTP_OK:
                    return []
                data = await response.json()
                results = []
                for item in data["results"]:
                    async with session.get(item["url"]) as detail_response:
                        if detail_response.status != self.HTTP_OK:
                            continue
                        details = await detail_response.json()
                        results.append(SpecificPokemonDto(name=details["name"], pokedex_number=details["id"],
                                                          abilities=[ability['ability']['name'] for ability in
                                                                     details['abilities']],
                                                          sprites=details['sprites'],
                                                          types=[ptype['type']['name'] for ptype in details['types']]))
                return results

    async def get_one(self, pokedex_number: int) -> Pokemon | None:
        """
        Obtiene un Pokémon específico por su número de Pokédex, priorizando los datos de la base de datos local.
        Si el Pokémon no se encuentra en la base de datos, realiza una consulta a la API.

        Args:
            pokedex_number: Número de Pokédex del Pokémon que se busca.

        Returns:
            Pokemon: Instancia de la entidad Pokémon con los datos obtenidos.
        """
        pokemon = self._get_from_database(pokedex_number)
        if pokemon:
            return pokemon

        return await self._get_from_api(pokedex_number)

    def _get_from_database(self, pokedex_number: int) -> Pokemon | None:
        """
        Busca un Pokémon en la base de datos local por su número de Pokédex.

        Args:
            pokedex_number: Número de Pokédex del Pokémon que se busca.

        Returns:
            Pokemon: Instancia de la entidad Pokémon si se encuentra en la base de datos; None si no se encuentra.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name, pokedex_number, abilities, sprites, types FROM pokemon WHERE pokedex_number=?',
                       (pokedex_number,))
        result = cursor.fetchone()
        conn.close()

        if result:
            name, pokedex_number, abilities, sprites, types = result
            return Pokemon(
                name=name,
                pokedex_number=pokedex_number,
                abilities=abilities.split(','),
                sprites=eval(sprites),
                types=types.split(',')
            )
        return None

    async def _get_from_api(self, pokedex_number: int) -> Pokemon | None:
        """
        Busca un Pokémon en la API de PokeAPI por su número de Pokédex.

        Args:
            pokedex_number: Número de Pokédex del Pokémon que se busca.

        Returns:
            Pokemon: Instancia de la entidad Pokémon si se encuentra en la API; None si no se encuentra.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}{pokedex_number}") as response:
                if response.status == 200:
                    data = await response.json()
                    return Pokemon(
                        name=data["name"],
                        pokedex_number=data["id"],
                        abilities=[ability['ability']['name'] for ability in data['abilities']],
                        sprites=data['sprites'],
                        types=[ptype['type']['name'] for ptype in data['types']]
                    )
        return None
