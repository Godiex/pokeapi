import os
import sqlite3
from typing import List
from domain.dto.general_pokemon_dto import GeneralPokemonDto
from domain.dto.specific_pokemon_dto import SpecificPokemonDto
from domain.entities.pokemon import Pokemon
from infrastructure.adapters.general_pokemon_query_repository import GeneralPokemonQueryRepository
from infrastructure.adapters.specific_pokemon_query_repository import SpecificPokemonQueryRepository


class PokemonRepositoryImplementation:
    """
    Clase que implementa las operaciones generales y específicas para obtener y actualizar información de Pokémon,
    combinando los datos de una base de datos local y una API externa.
    """

    def __init__(self):
        """
        Inicializa el repositorio con los repositorios de consulta general y específica.
        """
        self.db_path = os.getenv('DB_PATH', 'pokemon.db')
        self.api_url = os.getenv('POKEAPI_URL', 'https://pokeapi.co/api/v2/pokemon/')
        self.general_query_repo = GeneralPokemonQueryRepository(self.db_path, self.api_url)
        self.specific_query_repo = SpecificPokemonQueryRepository(self.db_path, self.api_url)

    async def get_general(self, data_to_search: str = None) -> List[GeneralPokemonDto]:
        """
        Obtiene la información general de los Pokémon. Si `data_to_search` está presente,
        busca en la base de datos y luego en la API si no encuentra resultados.
        Si no se proporciona `data_to_search`, combina los resultados de la API y la base de datos.
        """
        if data_to_search:
            from_db = self.general_query_repo.get_single_from_db(data_to_search)
            if from_db:
                return [from_db]
            return await self.general_query_repo.get_single_from_api(data_to_search)

        from_db = self.general_query_repo.get_all_from_db()
        from_api = await self.general_query_repo.get_all_from_api()
        return self._merge_with_priority_db(from_db, from_api)

    async def get_specific(self, data_to_search: str = None) -> List[SpecificPokemonDto]:
        """
        Obtiene la información específica de los Pokémon. Si `data_to_search` está presente,
        busca en la base de datos y luego en la API si no encuentra resultados.
        Si no se proporciona `data_to_search`, combina los resultados de la API y la base de datos.
        """
        if data_to_search:
            from_db = self.specific_query_repo.get_single_from_db(data_to_search)
            if from_db:
                return [from_db]
            return await self.specific_query_repo.get_single_from_api(data_to_search)

        from_db = self.specific_query_repo.get_all_from_db()
        from_api = await self.specific_query_repo.get_all_from_api()
        return self._merge_with_priority_db_specific(from_db, from_api)

    @staticmethod
    def _merge_with_priority_db(db_data: List[GeneralPokemonDto], api_data: List[GeneralPokemonDto]) -> List[GeneralPokemonDto]:
        """
        Combina los datos de la base de datos con los de la API, priorizando los de la base de datos.
        """
        combined = {PokemonRepositoryImplementation._extract_pokedex_number(pokemon.resource): pokemon for pokemon in api_data}
        for db_pokemon in db_data:
            pokedex_number = PokemonRepositoryImplementation._extract_pokedex_number(db_pokemon.resource)
            combined[pokedex_number] = db_pokemon
        return list(combined.values())

    @staticmethod
    def _merge_with_priority_db_specific(db_data: List[SpecificPokemonDto], api_data: List[SpecificPokemonDto]) -> List[SpecificPokemonDto]:
        """
        Combina los datos de la base de datos con los de la API, priorizando los de la base de datos.
        """
        combined = {pokemon.pokedex_number: pokemon for pokemon in api_data}
        for db_pokemon in db_data:
            combined[db_pokemon.pokedex_number] = db_pokemon
        return list(combined.values())

    @staticmethod
    def _extract_pokedex_number(resource: str) -> int:
        """
        Extrae el número de la Pokédex desde la URL del recurso.
        """
        import re
        match = re.search(r'/pokemon/(\d+)/', resource)
        if match:
            return int(match.group(1))
        raise ValueError(f"Could not extract pokedex number from resource: {resource}")

    async def update(self, pokemon: Pokemon):
        """
        Actualiza la información de un Pokémon en la base de datos local.

        Args:
            pokemon: Objeto de tipo `Pokemon` que contiene la información a ser actualizada.
        """
        conn = sqlite3.connect(self.db_path)  # Usar db_path desde el .env
        cursor = conn.cursor()

        abilities_str = ','.join(pokemon.abilities)
        types_str = ','.join(pokemon.types)
        sprites_str = str(pokemon.sprites)

        cursor.execute('''
               INSERT OR REPLACE INTO pokemon (name, pokedex_number, abilities, sprites, types)
               VALUES (?, ?, ?, ?, ?)
           ''', (pokemon.name, pokemon.pokedex_number, abilities_str, sprites_str, types_str))

        conn.commit()
        conn.close()

    async def get_one(self, pokedex_number: int) -> Pokemon | None:
        """
        Obtiene un Pokémon específico por su número de Pokédex, priorizando los datos de la base de datos local.
        Si el Pokémon no se encuentra en la base de datos, realiza una consulta a la API.

        Args:
            pokedex_number: Número de Pokédex del Pokémon que se busca.

        Returns:
            Pokemon: Instancia de la entidad Pokémon con los datos obtenidos.
        """
        return await self.specific_query_repo.get_one(pokedex_number)
