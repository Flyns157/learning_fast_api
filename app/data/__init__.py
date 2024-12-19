import json
import os

from ..models import Pokemon, User


# ====== User data ===== #
def get_users() -> dict[User]:
    with open(os.path.join(os.path.dirname(__file__), "users.json"), "r") as f:
        return json.load(f)


# ====== Pokemon data ===== #
def get_data() -> list[Pokemon]:
    #===== Structure de données : Dictionnaire indexé par pokemon id =====#
    with open(os.path.join(os.path.dirname(__file__), "pokemons.json"), "r") as f:
        return [Pokemon(**pokemon) for pokemon in json.load(f)]

def set_data(new_data: list[Pokemon]) -> None:
    with open(os.path.join(os.path.dirname(__file__), "pokemons.json"), "w") as f:
        json.dump([pokemon.model_dump() for pokemon in new_data], f)

def get_pokemon(pokemon_id) -> Pokemon | None:
    with open(os.path.join(os.path.dirname(__file__), "pokemons.json"), "r") as f:
        for pokemon in json.load(f):
            if pokemon["id"] == pokemon_id:
                return Pokemon(**pokemon)

def put_pokemon(pokemon_data: Pokemon) -> bool:
    data = get_data()
    i = 0
    while i < len(data):
        if data[i].id == pokemon_data.id:
            data[i] = pokemon_data
            set_data(data)
            return True
        i += 1
    return False

def add_pokemon(pokemon_data: Pokemon) -> bool:
    data = get_data()
    if all(pokemon.id != pokemon_data.id for pokemon in data):
        data.append(pokemon_data)
        set_data(data)
        return True
    return False

def del_pokemon(pokemon_id: int | str) -> Pokemon | None:
    data = get_data()
    i = 0
    while i < len(data):
        if data[i].id == pokemon_id:
            tmp = data.pop(i)
            set_data(data)
            return tmp
        i += 1
