from domain.entities.pokemon import Pokemon


def test_pokemon_update_name():
    """
    Prueba que el método update actualice solo el nombre.
    """
    pokemon = Pokemon(
        name="Pikachu",
        pokedex_number=25,
        abilities=["static"],
        sprites={"front_default": "some_url"},
        types=["electric"]
    )

    pokemon.update(name="Raichu")

    assert pokemon.name == "Raichu"
    assert pokemon.pokedex_number == 25
    assert pokemon.abilities == ["static"]
    assert pokemon.sprites == {"front_default": "some_url"}
    assert pokemon.types == ["electric"]


def test_pokemon_update_abilities():
    """
    Prueba que el método update actualice solo las habilidades.
    """
    pokemon = Pokemon(
        name="Pikachu",
        pokedex_number=25,
        abilities=["static"],
        sprites={"front_default": "some_url"},
        types=["electric"]
    )

    pokemon.update(abilities=["static", "lightning-rod"])

    assert pokemon.name == "Pikachu"
    assert pokemon.pokedex_number == 25
    assert pokemon.abilities == ["static", "lightning-rod"]
    assert pokemon.sprites == {"front_default": "some_url"}
    assert pokemon.types == ["electric"]


def test_pokemon_update_sprites():
    """
    Prueba que el método update actualice solo los sprites.
    """
    pokemon = Pokemon(
        name="Pikachu",
        pokedex_number=25,
        abilities=["static"],
        sprites={"front_default": "some_url"},
        types=["electric"]
    )

    pokemon.update(sprites={"front_default": "new_url"})

    assert pokemon.name == "Pikachu"
    assert pokemon.pokedex_number == 25
    assert pokemon.abilities == ["static"]
    assert pokemon.sprites == {"front_default": "new_url"}
    assert pokemon.types == ["electric"]


def test_pokemon_update_types():
    """
    Prueba que el método update actualice solo los tipos.
    """
    pokemon = Pokemon(
        name="Pikachu",
        pokedex_number=25,
        abilities=["static"],
        sprites={"front_default": "some_url"},
        types=["electric"]
    )

    pokemon.update(types=["electric", "fairy"])

    assert pokemon.name == "Pikachu"
    assert pokemon.pokedex_number == 25
    assert pokemon.abilities == ["static"]
    assert pokemon.sprites == {"front_default": "some_url"}
    assert pokemon.types == ["electric", "fairy"]


def test_pokemon_update_all_fields():
    """
    Prueba que el método update actualice todos los atributos simultáneamente.
    """
    pokemon = Pokemon(
        name="Pikachu",
        pokedex_number=25,
        abilities=["static"],
        sprites={"front_default": "some_url"},
        types=["electric"]
    )

    pokemon.update(
        name="Raichu",
        abilities=["static", "lightning-rod"],
        sprites={"front_default": "new_url"},
        types=["electric", "fairy"]
    )

    assert pokemon.name == "Raichu"
    assert pokemon.pokedex_number == 25
    assert pokemon.abilities == ["static", "lightning-rod"]
    assert pokemon.sprites == {"front_default": "new_url"}
    assert pokemon.types == ["electric", "fairy"]
