class Pokemon:
    def __init__(self, name: str, pokedex_number: int, abilities: list, sprites: dict, types: list):
        self.name = name
        self.pokedex_number = pokedex_number
        self.abilities = abilities
        self.sprites = sprites
        self.types = types

    def __repr__(self):
        return f"<Pokemon(name={self.name}, pokedex_number={self.pokedex_number})>"

    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario para que pueda ser enviada como respuesta.
        """
        return {
            "name": self.name,
            "pokedex_number": self.pokedex_number,
            "abilities": self.abilities,
            "sprites": self.sprites,
            "types": self.types
        }

    def update(self, name: str = None, abilities: list = None, sprites: dict = None, types: list = None):
        """
        Actualiza los atributos del Pokémon, excepto el número de la Pokédex.
        """
        if name:
            self.name = name
        if abilities:
            self.abilities = abilities
        if sprites:
            self.sprites = sprites
        if types:
            self.types = types

        return self
