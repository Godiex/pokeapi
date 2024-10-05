from pydantic import BaseModel


class GeneralPokemonDto(BaseModel):
    name: str
    resource: str
