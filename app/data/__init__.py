import json
import os

from ..models import Pokemon, User


# ====== User data ===== #
def get_users() -> dict[User]:
    with open(os.path.join(os.path.dirname(__file__), "users.json"), "r") as f:
        return json.load(f)


# ====== Pokemon data ===== #
def get_data() -> dict[Pokemon]:
    #===== Structure de données : Dictionnaire indexé par pokemon id =====#
    with open(os.path.join(os.path.dirname(__file__), "pokemons.json"), "r") as f:
        return json.load(f)

def get_pokemon(pokemon_id) -> dict:
    return get_data().get(str(pokemon_id))

def put_pokemon(pokemon_id: int | str, pokemon_data: Pokemon) -> None:
    data = get_data()
    data[str(pokemon_id)] = pokemon_data
    with open(os.path.join(os.path.dirname(__file__), "pokemons.json"), "w") as f:
        json.dump(data, f)

def del_pokemon(pokemon_id: int | str) -> None:
    data = get_data()
    data.pop(str(pokemon_id))
    with open(os.path.join(os.path.dirname(__file__), "pokemons.json"), "w") as f:
        json.dump(data, f)
