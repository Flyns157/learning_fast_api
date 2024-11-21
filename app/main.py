from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Union
import json
import math

#===== Structure de données : Dictionnaire indexé par pokemon id =====#
with open("app/pokemons.json", "r") as f:
    pokemons_list = json.load(f)

list_pokemons = {k+1: v for k, v in enumerate(pokemons_list)}
#======================================================================
class Pokemon(BaseModel):
    id: int
    name: str
    types: List[str]
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    evolution_id: Union[int, None] = None
#======================================================================

app = FastAPI()

#===========================GET============================
@app.get("/total_pokemons")
def get_total_pokemons() -> dict:
    return {"total": len(list_pokemons)}

@app.get("/pokemons", response_model=List[Pokemon])
def get_all_pokemons1() -> List[Pokemon]:
    return [Pokemon(**list_pokemons[id]) for id in list_pokemons]

@app.get("/pokemon/{id}", response_model=Pokemon)
def get_pokemon_by_id(id: int = Path(ge=1)) -> Pokemon:
    if id not in list_pokemons:
        raise HTTPException(status_code=404, detail="Ce pokemon n'existe pas")
    
    return Pokemon(**list_pokemons[id])

#===========================POST============================
@app.post("/pokemon/", response_model=Pokemon)
def create_pokemon(pokemon: Pokemon) -> Pokemon:
    if pokemon.id in list_pokemons:
        raise HTTPException(status_code=404, detail=f"Le pokemon {pokemon.id} existe déjà !")
    
    list_pokemons[pokemon.id] = pokemon.dict()
    return pokemon

#===========================PUT============================
@app.put("/pokemon/{id}", response_model=Pokemon)
def update_pokemon(pokemon: Pokemon, id: int = Path(ge=1)) -> Pokemon:
    if id not in list_pokemons:
        raise HTTPException(status_code=404, detail=f"Le pokemon {id} n'existe pas.")
    
    list_pokemons[id] = pokemon.dict()
    return pokemon

#===========================DELETE============================
@app.delete("/pokemon/{id}", response_model=Pokemon)
def delete_pokemon(id: int = Path(ge=1)) -> Pokemon:
    if id in list_pokemons:
        pokemon = Pokemon(**list_pokemons[id])
        del list_pokemons[id]
        return pokemon
    
    raise HTTPException(status_code=404, detail=f"Le pokemon {id} n'existe pas.")

#===========================GET============================
@app.get("/types")
def get_all_types() -> List[str]:
    types = set()
    for pokemon in pokemons_list:
        types.update(pokemon["types"])
    return sorted(types)

@app.get("/pokemons/search/", response_model=Union[List[Pokemon], None])
def search_pokemons(
    types: Union[str, None] = None,
    evo: Union[str, None] = None,
    totalgt: Union[int, None] = None,
    totallt: Union[int, None] = None,
    sortby: Union[str, None] = None,
    order: Union[str, None] = None,
) -> Union[List[Pokemon], None]:
    
    filtered_list = []

    #On filtre les types
    if types is not None :
        for pokemon in pokemons_list :
            if set(types.split(",")).issubset(pokemon["types"]) :
                filtered_list.append(pokemon)

    #On filtre les evolutions
    if evo is not None :
        tmp = filtered_list if filtered_list else pokemons_list
        new = []

        for pokemon in tmp :
            if evo == "true" and "evolution_id" in pokemon:
                new.append(pokemon)
            if evo == "false" and "evolution_id" not in pokemon:
                new.append(pokemon)

        filtered_list = new

    #On filtre sur greater than total
    if totalgt is not None :
        tmp = filtered_list if filtered_list else pokemons_list
        new = []

        for pokemon in tmp :
            if pokemon["total"] > totalgt:
                new.append(pokemon)

        filtered_list = new

    #On filtre sur less than total
    if totallt is not None :
        tmp = filtered_list if filtered_list else pokemons_list
        new = []

        for pokemon in tmp :
            if pokemon["total"] < totallt:
                new.append(pokemon)

        filtered_list = new

    #On gére le tri
    if sortby is not None and sortby in ["id","name","total"] :
        filtered_list = filtered_list if filtered_list else pokemons_list
        sorting_order = False
        if order == "asc" : sorting_order = False
        if order == "desc" : sorting_order = True

        filtered_list = sorted(filtered_list, key=lambda d: d[sortby], reverse=sorting_order)

    if filtered_list:
        return [Pokemon(**pokemon) for pokemon in filtered_list]
    
    raise HTTPException(status_code=404, detail="Aucun Pokemon ne répond aux critères de recherche")

#=====Tous les Pokémons avec la pagination=====
@app.get("/pokemons2/", response_model=List[Pokemon])
def get_all_pokemons(page: int = 1, items: int = 10) -> List[Pokemon]:
    items = min(items, 20)
    max_page = math.ceil(len(list_pokemons) / items)
    current_page = min(page, max_page)
    start = (current_page - 1) * items
    stop = start + items
    sublist = list(list_pokemons)[start:stop]

    return [Pokemon(**list_pokemons[id]) for id in sublist]
